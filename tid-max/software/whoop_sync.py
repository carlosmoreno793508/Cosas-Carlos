#!/usr/bin/env python3
"""
whoop_sync.py — Paso 2 (repetible): jalar los datos de WHOOP con la API v2.

Qué hace:
  1. Usa el REFRESH TOKEN (de whoop_auth.py) para pedir un access token fresco.
  2. IMPORTANTE: WHOOP *rota* el refresh token en cada renovacion -> lo guarda de nuevo en .env.
  3. Descarga perfil, medidas, recovery, cycles, sueno y workouts (API v2).
  4. Guarda cada respuesta como JSON en ./datos/ e imprime un resumen legible.

Uso:
    python whoop_sync.py

Nota: WHOOP entrega METRICAS YA PROCESADAS (recovery, HRV diaria, sueno, strain),
NO la senal PPG/IBI cruda. Para DFA-alfa1 cruda se usa el Polar H10 / EVK (ver analisis/).
"""
import os
import sys
import json
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")

try:
    from dotenv import load_dotenv, set_key
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
API_BASE = "https://api.prod.whoop.com/developer"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
# TID_DATA_DIR permite al pipeline multiusuario (tid_multi.py) apuntar el crudo de
# WHOOP a la carpeta de un atleta (datos/atletas/<slug>/). Sin la env = como siempre.
DATA_DIR = os.environ.get("TID_DATA_DIR") or os.path.join(SCRIPT_DIR, "datos")

# Endpoints v2: (nombre_archivo, ruta, es_coleccion)
ENDPOINTS = [
    ("perfil", "/v2/user/profile/basic", False),
    ("medidas_cuerpo", "/v2/user/measurement/body", False),
    ("recovery", "/v2/recovery", True),
    ("cycles", "/v2/cycle", True),
    ("sueno", "/v2/activity/sleep", True),
    ("workouts", "/v2/activity/workout", True),
]


def refresh_access_token(client_id, client_secret, refresh_token):
    """Canjea el refresh token por un access token nuevo. Devuelve (access_token, nuevo_refresh)."""
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            # WHOOP requiere pedir 'offline' de nuevo para seguir recibiendo refresh tokens.
            "scope": "offline",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(
            f"\nNo pude renovar el access token ({resp.status_code}):\n{resp.text}\n"
            "Si dice 'invalid_grant', el refresh token expiro o se revoco: "
            "vuelve a correr  python whoop_auth.py"
        )
    data = resp.json()
    return data.get("access_token"), data.get("refresh_token", refresh_token)


def fetch(path, token, is_collection):
    """GET a un endpoint. Para colecciones pide hasta 25 registros recientes."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 25} if is_collection else None
    resp = requests.get(API_BASE + path, headers=headers, params=params, timeout=30)
    if resp.status_code != 200:
        return {"_error": resp.status_code, "_body": resp.text[:500]}
    return resp.json()


def save_json(name, payload, stamp):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{name}_{stamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def _records(payload):
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    return []


def print_summary(results):
    print("\n================= RESUMEN =================")

    perfil = results.get("perfil", {})
    if perfil and "_error" not in perfil:
        nombre = f"{perfil.get('first_name', '')} {perfil.get('last_name', '')}".strip()
        print(f"Atleta:            {nombre or '(sin nombre)'}")

    rec = _records(results.get("recovery", {}))
    if rec:
        score = (rec[0] or {}).get("score", {}) or {}
        print(f"Recovery reciente: {score.get('recovery_score', 'n/d')} %")
        print(f"HRV (rMSSD):       {score.get('hrv_rmssd_milli', 'n/d')} ms")
        print(f"FC en reposo:      {score.get('resting_heart_rate', 'n/d')} lpm")

    slp = _records(results.get("sueno", {}))
    if slp:
        s = (slp[0] or {}).get("score", {}) or {}
        print(f"Sueno (rendim.):   {s.get('sleep_performance_percentage', 'n/d')} %")

    cyc = _records(results.get("cycles", {}))
    if cyc:
        c = (cyc[0] or {}).get("score", {}) or {}
        print(f"Strain del dia:    {c.get('strain', 'n/d')}")

    wko = _records(results.get("workouts", {}))
    print(f"Workouts jalados:  {len(wko)}")
    print("==========================================")
    print(f"JSON crudo guardado en: {DATA_DIR}/")
    print("==========================================\n")


def main():
    load_dotenv(ENV_PATH)
    client_id = os.getenv("WHOOP_CLIENT_ID", "").strip()
    client_secret = os.getenv("WHOOP_CLIENT_SECRET", "").strip()
    refresh_token = os.getenv("WHOOP_REFRESH_TOKEN", "").strip()

    if not (client_id and client_secret and refresh_token):
        sys.exit(
            "\nFaltan datos en .env. Necesitas WHOOP_CLIENT_ID, WHOOP_CLIENT_SECRET y "
            "WHOOP_REFRESH_TOKEN.\nSi no tienes el refresh token, corre primero:  python whoop_auth.py"
        )

    print("Renovando access token...")
    access_token, new_refresh = refresh_access_token(client_id, client_secret, refresh_token)

    # WHOOP rota el refresh token: guardamos el nuevo o el proximo sync fallara.
    if new_refresh and new_refresh != refresh_token:
        set_key(ENV_PATH, "WHOOP_REFRESH_TOKEN", new_refresh)
        print("Refresh token rotado y actualizado en .env.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    results = {}
    for name, path, is_collection in ENDPOINTS:
        print(f"Descargando {name} ...")
        payload = fetch(path, access_token, is_collection)
        results[name] = payload
        saved = save_json(name, payload, stamp)
        if isinstance(payload, dict) and payload.get("_error"):
            print(f"  aviso: {name} devolvio {payload['_error']} (revisa {saved})")

    print_summary(results)


if __name__ == "__main__":
    main()
