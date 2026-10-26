#!/usr/bin/env python3
"""
garmin_auth.py — Autorizar una cuenta de Garmin Connect con TID-MAX (API PERSONAL, soporta
varias cuentas). STUB listo para enchufar una key real.

Contexto (oct-2026): Garmin reabrió su Connect Developer Program con un **tier PERSONAL**: cada
usuario obtiene su propia API key entrando a Garmin Connect, sin proceso de aprobación. Cubre
actividad (JSON + .FIT), salud (JSON) y salud femenina; es **pull-only** y excluye Courses/Training
(no empuja entrenos al reloj — a nosotros solo nos interesa LEER).

⚠️  POR VERIFICAR contra https://developer.garmin.com/gc-developer-program/overview/ antes de
    producción (no se probó en vivo, no había cuenta disponible):
      1. Flujo exacto de credenciales del tier personal: ¿key estática que copias de Garmin
         Connect, u OAuth2/PKCE? Este stub soporta AMBOS (key directa en .env, o el esqueleto
         OAuth de abajo). Confirmar cuál aplica.
      2. Hosts/paths reales de autorización y token (los de abajo son los documentados para el
         programa; pueden cambiar en el tier personal).
      3. Si la key personal devuelve el .FIT COMPLETO (con R-R latido a latido) o uno recortado.
         De eso depende que Garmin sea fuente de señal para hrv_rr (ver garmin_fit.py).

Patrón idéntico a polar_auth.py: almacén multi-cuenta en datos/garmin_accounts.json.

Uso:
    # Opción A — key personal directa (si el tier personal entrega un token estático):
    #   pon GARMIN_PERSONAL_TOKEN=... en .env  y luego:
    python garmin_auth.py --account carlos --from-env

    # Opción B — OAuth (si el tier personal usa el flujo OAuth):
    python garmin_auth.py --account carlos            # abre el navegador

Requisitos .env (de developer.garmin.com > tu app, SOLO si usas OAuth):
    GARMIN_CLIENT_ID=...
    GARMIN_CLIENT_SECRET=...        (trátalo como contraseña — NUNCA lo pegues en un chat)
    GARMIN_REDIRECT_URI=http://localhost:8766/callback
"""
import os
import sys
import json
import argparse
import secrets
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

# --- Endpoints del programa (POR VERIFICAR para el tier personal) ---
AUTH_URL = "https://connect.garmin.com/oauth2Confirm"          # VERIFICAR
TOKEN_URL = "https://diauth.garmin.com/di-oauth2-service/oauth/token"  # VERIFICAR
SCOPE = "ACTIVITY_EXPORT HEALTH_EXPORT"                         # VERIFICAR nombres de scope

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
STORE_PATH = os.path.join(SCRIPT_DIR, "datos", "garmin_accounts.json")
DEFAULT_REDIRECT = "http://localhost:8766/callback"


def load_store():
    """Almacén de cuentas: { "nombre": {"access_token", "refresh_token"?, "user_id"?} }."""
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_store(store):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    print(f"Guardado en {STORE_PATH}")


def guardar_token_directo(nombre):
    """Opción A: el tier personal entrega una key/token estático → se copia de .env al almacén."""
    load_dotenv(ENV_PATH)
    token = os.getenv("GARMIN_PERSONAL_TOKEN", "").strip()
    if not token:
        sys.exit("Falta GARMIN_PERSONAL_TOKEN en .env (la key personal de Garmin Connect).")
    store = load_store()
    store[nombre] = {"access_token": token, "tipo": "personal_key"}
    save_store(store)
    print(f"Cuenta '{nombre}' registrada con key personal. Ya puedes correr:  python garmin_sync.py")


# ------------------------------------------------------ OAuth (Opción B, esqueleto por verificar)

class _CallbackHandler(BaseHTTPRequestHandler):
    code = None
    state_expected = None

    def do_GET(self):
        q = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(q.query)
        if q.path.startswith("/callback") and params.get("state", [None])[0] == _CallbackHandler.state_expected:
            _CallbackHandler.code = params.get("code", [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"TID-MAX: Garmin conectado. Puedes cerrar esta pestana.")
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, *a):
        pass


def oauth_flow(nombre):
    load_dotenv(ENV_PATH)
    cid = os.getenv("GARMIN_CLIENT_ID", "").strip()
    secret = os.getenv("GARMIN_CLIENT_SECRET", "").strip()
    redirect = os.getenv("GARMIN_REDIRECT_URI", DEFAULT_REDIRECT).strip()
    if not (cid and secret):
        sys.exit("Faltan GARMIN_CLIENT_ID / GARMIN_CLIENT_SECRET en .env (de developer.garmin.com).")

    state = secrets.token_urlsafe(16)
    _CallbackHandler.state_expected = state
    port = urllib.parse.urlparse(redirect).port or 8766
    server = HTTPServer(("localhost", port), _CallbackHandler)
    threading.Thread(target=server.handle_request, daemon=True).start()

    auth = AUTH_URL + "?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": cid, "redirect_uri": redirect,
        "scope": SCOPE, "state": state,
    })
    print("Abriendo el navegador para autorizar Garmin...\n" + auth)
    webbrowser.open(auth)

    # Espera el callback (bloqueante, simple para un stub local).
    import time
    for _ in range(120):
        if _CallbackHandler.code:
            break
        time.sleep(1)
    code = _CallbackHandler.code
    if not code:
        sys.exit("No llegó el código de autorización. Revisa el REDIRECT_URI (debe coincidir EXACTO).")

    resp = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code", "code": code,
        "client_id": cid, "client_secret": secret, "redirect_uri": redirect,
    }, timeout=30)
    if not resp.ok:
        sys.exit(f"Falló el canje de token ({resp.status_code}): {resp.text[:300]}")
    tok = resp.json()
    store = load_store()
    store[nombre] = {
        "access_token": tok.get("access_token"),
        "refresh_token": tok.get("refresh_token"),
        "tipo": "oauth",
    }
    save_store(store)
    print(f"Cuenta '{nombre}' conectada por OAuth.")


def main():
    ap = argparse.ArgumentParser(description="Conecta una cuenta de Garmin (API personal) con TID-MAX.")
    ap.add_argument("--account", default="principal", help="nombre de la cuenta (default: principal)")
    ap.add_argument("--from-env", action="store_true",
                    help="usa GARMIN_PERSONAL_TOKEN de .env (key personal estática) en vez de OAuth")
    args = ap.parse_args()
    if args.from_env:
        guardar_token_directo(args.account)
    else:
        print("NOTA: flujo OAuth POR VERIFICAR contra developer.garmin.com. Si el tier personal te da "
              "una key estática, usa:  python garmin_auth.py --account <n> --from-env")
        oauth_flow(args.account)


if __name__ == "__main__":
    main()
