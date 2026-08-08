#!/usr/bin/env python3
"""
polar_sync.py — Paso 2 (despues de cada corrida): baja tus entrenamientos de Polar Flow.

Que hace (modelo de "transaccion" de AccessLink):
  1. Abre una transaccion con las sesiones NUEVAS (aun no descargadas).
  2. Por cada una guarda en datos/polar_flow/:
       resumen JSON  +  GPX (ruta)  +  TCX (FC/pace)  +  zonas de FC  +  muestras.
  3. Confirma (commit) la transaccion para no volver a bajar lo mismo.

Uso:
    python polar_sync.py         # baja todo lo nuevo desde la ultima vez

Nota: si no hay sesiones nuevas, Polar responde 204 y el script lo dice.
Corre polar_auth.py una sola vez antes que esto.

Flujo real: terminas de correr -> abres la app Polar Flow en el celular para que
sincronice a la nube -> corres este script en la Mac.
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
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

API_BASE = "https://www.polaraccesslink.com/v3"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
OUT_DIR = os.path.join(SCRIPT_DIR, "datos", "polar_flow")

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


def main():
    load_dotenv(ENV_PATH)
    token = os.getenv("POLAR_ACCESS_TOKEN", "").strip()
    user_id = os.getenv("POLAR_USER_ID", "").strip()
    if not token or not user_id:
        sys.exit(
            "\nFalta POLAR_ACCESS_TOKEN / POLAR_USER_ID en .env.\n"
            "Corre primero (una sola vez):  python polar_auth.py"
        )

    os.makedirs(OUT_DIR, exist_ok=True)
    base = f"{API_BASE}/users/{user_id}/exercise-transactions"

    # 1) Abrir transaccion con lo nuevo
    tx = requests.post(base, headers=_hdr(token), timeout=30)
    if tx.status_code == 204:
        print("No hay sesiones nuevas en Polar Flow.")
        print("(Abre la app Polar Flow en el celular para que sincronice el reloj/banda a la nube.)")
        return
    if tx.status_code == 401:
        sys.exit("Token invalido o expirado. Vuelve a correr:  python polar_auth.py")
    if tx.status_code != 201:
        sys.exit(f"No pude abrir la transaccion ({tx.status_code}): {tx.text}")

    tid = tx.json()["transaction-id"]
    tx_uri = f"{base}/{tid}"

    # 2) Listar y bajar cada ejercicio
    lst = requests.get(tx_uri, headers=_hdr(token), timeout=30).json()
    exercises = lst.get("exercises", [])
    print(f"{len(exercises)} sesion(es) nueva(s).\n")

    resumen_total = []
    for url in exercises:
        s = requests.get(url, headers=_hdr(token), timeout=30).json()
        eid = str(s.get("id", url.rstrip("/").split("/")[-1]))
        stamp = (s.get("start-time", "") or "").replace(":", "").replace("-", "")[:15]
        stem = os.path.join(OUT_DIR, f"polar_{stamp}_{eid}")

        with open(stem + ".json", "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)

        for nombre, sub, is_json in EXTRAS:
            accept = "application/json" if is_json else "*/*"
            r = requests.get(f"{url}/{sub}", headers=_hdr(token, accept), timeout=30)
            if r.status_code != 200 or not r.content:
                continue
            if is_json:
                with open(f"{stem}_{nombre}.json", "w", encoding="utf-8") as f:
                    f.write(r.text)
            else:
                with open(f"{stem}.{sub}", "wb") as f:
                    f.write(r.content)

        km = round((s.get("distance", 0) or 0) / 1000, 2)
        dur = s.get("duration", "")
        dep = s.get("detailed-sport-info") or s.get("sport", "—")
        fc = s.get("heart-rate") or {}
        cal = s.get("calories", "—")
        print(f"  - {str(dep):<18} {km:>6} km  ·  {dur}  ·  "
              f"FC {fc.get('average', '—')}/{fc.get('maximum', '—')} lpm  ·  {cal} kcal")
        resumen_total.append({
            "id": eid, "deporte": dep, "km": km, "duracion": dur,
            "fc_media": fc.get("average"), "fc_max": fc.get("maximum"),
            "calorias": cal, "inicio": s.get("start-time"),
        })

    # 3) Commit: marcar como leidas para no repetir
    requests.put(tx_uri, headers=_hdr(token), timeout=30)

    idx = os.path.join(OUT_DIR, "_ultima_sync.json")
    with open(idx, "w", encoding="utf-8") as f:
        json.dump({
            "sincronizado": datetime.now(timezone.utc).isoformat(),
            "sesiones": resumen_total,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nListo. Datos guardados en {OUT_DIR}\n")


if __name__ == "__main__":
    main()
