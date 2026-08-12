#!/usr/bin/env python3
"""
polar_sync.py — Baja los entrenamientos de Polar Flow (soporta VARIAS cuentas).

Que hace (por cada cuenta conectada):
  1. Abre una transaccion con las sesiones NUEVAS (aun no descargadas).
  2. Guarda en datos/polar_flow/<cuenta>/:
       resumen JSON  +  GPX (ruta)  +  TCX (FC/pace)  +  zonas de FC  +  muestras.
  3. Confirma (commit) la transaccion para no volver a bajar lo mismo.

Uso:
    python polar_sync.py                     # baja TODO lo nuevo de TODAS las cuentas
    python polar_sync.py --account personal  # solo esa cuenta

Las cuentas se conectan con:  python polar_auth.py --account <nombre>
Si no hay sesiones nuevas, Polar responde 204 y el script lo dice.

Flujo real: grabas la corrida con la app Polar Flow -> se sincroniza a la nube ->
corres este script en la Mac.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

API_BASE = "https://www.polaraccesslink.com/v3"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
STORE_PATH = os.path.join(SCRIPT_DIR, "datos", "polar_accounts.json")
# OUT_BASE respeta TID_DATA_DIR para aislar el crudo de Polar en la carpeta del atleta
# (datos/atletas/<slug>/polar_flow/) en el pipeline multiusuario. Sin la env = como siempre.
OUT_BASE = os.path.join(os.environ.get("TID_DATA_DIR") or os.path.join(SCRIPT_DIR, "datos"), "polar_flow")

# Sub-recursos que intentamos bajar de cada ejercicio (los que no existan se saltan).
# (nombre_archivo, ruta_api, es_json)
EXTRAS = [
    ("zonas_fc", "heart-rate-zones", True),
    ("muestras", "samples", True),
    ("gpx", "gpx", False),
    ("tcx", "tcx", False),
]


def _hdr(token, accept="application/json"):
    return {"Authorization": f"Bearer {token}", "Accept": accept}


def load_store():
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_store(store):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


def migrar_env_si_hace_falta(store):
    """Compatibilidad: si el token viejo esta en .env y no en el almacen, lo migra."""
    load_dotenv(ENV_PATH)
    token = os.getenv("POLAR_ACCESS_TOKEN", "").strip()
    user_id = os.getenv("POLAR_USER_ID", "").strip()
    if token and user_id and not any(str(d.get("user_id")) == user_id for d in store.values()):
        store["principal"] = {"access_token": token, "user_id": user_id}
        save_store(store)
        print("(Migre la cuenta que tenias en .env como 'principal'.)")
    return store


def sync_cuenta(nombre, token, user_id):
    """Baja lo nuevo de una cuenta. Devuelve la lista de sesiones bajadas."""
    out_dir = os.path.join(OUT_BASE, nombre)
    os.makedirs(out_dir, exist_ok=True)
    base = f"{API_BASE}/users/{user_id}/exercise-transactions"

    tx = requests.post(base, headers=_hdr(token), timeout=30)
    if tx.status_code == 204:
        print(f"[{nombre}] No hay sesiones nuevas.")
        return []
    if tx.status_code == 401:
        print(f"[{nombre}] Token invalido o expirado. Reconecta con:  "
              f"python polar_auth.py --account {nombre}")
        return []
    if tx.status_code != 201:
        print(f"[{nombre}] No pude abrir la transaccion ({tx.status_code}): {tx.text}")
        return []

    tid = tx.json()["transaction-id"]
    tx_uri = f"{base}/{tid}"
    exercises = requests.get(tx_uri, headers=_hdr(token), timeout=30).json().get("exercises", [])
    print(f"[{nombre}] {len(exercises)} sesion(es) nueva(s).")

    bajadas = []
    for url in exercises:
        s = requests.get(url, headers=_hdr(token), timeout=30).json()
        eid = str(s.get("id", url.rstrip("/").split("/")[-1]))
        stamp = (s.get("start-time", "") or "").replace(":", "").replace("-", "")[:15]
        stem = os.path.join(out_dir, f"polar_{stamp}_{eid}")

        with open(stem + ".json", "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)

        for etiq, sub, is_json in EXTRAS:
            accept = "application/json" if is_json else "*/*"
            r = requests.get(f"{url}/{sub}", headers=_hdr(token, accept), timeout=30)
            if r.status_code != 200 or not r.content:
                continue
            if is_json:
                with open(f"{stem}_{etiq}.json", "w", encoding="utf-8") as f:
                    f.write(r.text)
            else:
                with open(f"{stem}.{sub}", "wb") as f:
                    f.write(r.content)

        km = round((s.get("distance", 0) or 0) / 1000, 2)
        dur = s.get("duration", "")
        dep = s.get("detailed-sport-info") or s.get("sport", "—")
        fc = s.get("heart-rate") or {}
        cal = s.get("calories", "—")
        print(f"    - {str(dep):<18} {km:>6} km  ·  {dur}  ·  "
              f"FC {fc.get('average', '—')}/{fc.get('maximum', '—')} lpm  ·  {cal} kcal")
        bajadas.append({
            "cuenta": nombre, "id": eid, "deporte": dep, "km": km, "duracion": dur,
            "fc_media": fc.get("average"), "fc_max": fc.get("maximum"),
            "calorias": cal, "inicio": s.get("start-time"),
        })

    requests.put(tx_uri, headers=_hdr(token), timeout=30)  # commit
    return bajadas


def main():
    parser = argparse.ArgumentParser(description="Bajar entrenamientos de Polar Flow.")
    parser.add_argument("--account", default=None,
                        help="Baja solo esa cuenta. Sin esto, baja TODAS.")
    args = parser.parse_args()

    store = load_store()
    store = migrar_env_si_hace_falta(store)
    if not store:
        sys.exit("\nNo hay cuentas conectadas. Conecta una con:  python polar_auth.py --account principal")

    if args.account:
        if args.account not in store:
            sys.exit(f"\nNo encuentro la cuenta '{args.account}'. Conectadas: {', '.join(store.keys())}")
        cuentas = {args.account: store[args.account]}
    else:
        cuentas = store

    print(f"Cuentas a sincronizar: {', '.join(cuentas.keys())}\n")
    todo = []
    for nombre, datos in cuentas.items():
        todo.extend(sync_cuenta(nombre, datos["access_token"], str(datos["user_id"])))

    os.makedirs(OUT_BASE, exist_ok=True)
    with open(os.path.join(OUT_BASE, "_ultima_sync.json"), "w", encoding="utf-8") as f:
        json.dump({
            "sincronizado": datetime.now(timezone.utc).isoformat(),
            "sesiones": todo,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nListo. {len(todo)} sesion(es) bajada(s) en total. Guardado en {OUT_BASE}\n")


if __name__ == "__main__":
    main()
