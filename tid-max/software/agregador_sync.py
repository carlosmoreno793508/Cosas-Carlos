#!/usr/bin/env python3
"""
agregador_sync.py — Baja lo nuevo de TODOS los atletas conectados via Junction.

Es el espejo de polar_sync.py, pero contra el AGREGADOR: una sola API baja los
entrenos sin importar la marca (WHOOP, Polar, Garmin, Oura, Fitbit, Strava...).
Modelo "pull": corre este script y trae lo nuevo. (El "push" por webhook llega
en la Fase 2, ver agregador_webhook.py.)

Que hace por cada atleta conectado (datos/agregador_users.json):
  1. Pide sus workouts en un rango de fechas (por defecto, ultimos N dias).
  2. Guarda el crudo en datos/agregador/<atleta>/workouts_<rango>.json
     (y de una vez sleep/activity para el daily, si estan disponibles).
  3. Imprime un resumen por sesion.

Luego, para que entren al esquema canonico:
    python tid_data.py     # el normalizador ya lee datos/agregador/

Uso:
    python agregador_sync.py                 # ultimos 14 dias, todos los atletas
    python agregador_sync.py --atleta carlos # solo ese atleta
    python agregador_sync.py --dias 30       # cambia la ventana
    python agregador_sync.py --desde 2026-01-01 --hasta 2026-08-10

Conecta atletas con:  python agregador_connect.py --atleta <nombre>
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
# Mapeo local (agregador_connect.py, gitignored) + versionado (lo escribe la app
# via api/connect.js, para el sync en la nube). Se leen ambos; el local gana.
STORE_PATH = os.path.join(SCRIPT_DIR, "datos", "agregador_users.json")
STORE_PATH_REPO = os.path.join(SCRIPT_DIR, "agregador_users.json")
OUT_BASE = os.path.join(SCRIPT_DIR, "datos", "agregador")

DEFAULT_API_BASE = "https://api.sandbox.us.junction.com"

# Resumenes que intentamos bajar de cada atleta (los que no existan se saltan).
# (etiqueta, ruta_api)  ->  /v2/summary/<ruta>/<user_id>?start_date&end_date
SUMMARIES = [
    ("workouts", "workouts"),
    ("sleep", "sleep"),
    ("activity", "activity"),
]


def load_store():
    store = {}
    for path in (STORE_PATH_REPO, STORE_PATH):  # el local (2o) pisa al versionado
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    store.update(json.load(f))
            except (ValueError, OSError):
                pass
    return store


def _cfg():
    load_dotenv(ENV_PATH)
    api_key = os.getenv("JUNCTION_API_KEY", "").strip()
    api_base = os.getenv("JUNCTION_API_BASE", DEFAULT_API_BASE).strip().rstrip("/")
    if not api_key:
        sys.exit("\nFalta JUNCTION_API_KEY en .env. Vela con:  python agregador_connect.py --atleta <n>")
    return api_key, api_base


def _hdr(api_key):
    return {"x-vital-api-key": api_key, "Accept": "application/json"}


def bajar_resumen(api_key, api_base, user_id, ruta, desde, hasta):
    """Devuelve el JSON de un resumen (workouts/sleep/activity) o None si no hay/hay error."""
    url = f"{api_base}/v2/summary/{ruta}/{user_id}"
    r = requests.get(url, headers=_hdr(api_key),
                     params={"start_date": desde, "end_date": hasta}, timeout=45)
    if r.status_code == 200:
        return r.json()
    if r.status_code == 404:
        return None  # el atleta aun no conecta una fuente que aporte esto
    print(f"    (aviso: {ruta} devolvio {r.status_code}: {r.text[:160]})")
    return None


def _resumen_workouts(data):
    """Imprime una linea por workout. Defensivo con los nombres de campos."""
    if not data:
        return 0
    workouts = data.get("workouts") if isinstance(data, dict) else data
    if not isinstance(workouts, list):
        return 0
    for w in workouts:
        sport = w.get("sport") or {}
        dep = sport.get("name") if isinstance(sport, dict) else sport
        dep = dep or w.get("sport_name") or "—"
        prov = (w.get("source") or {}).get("provider") if isinstance(w.get("source"), dict) else w.get("provider")
        dist = w.get("distance")
        km = round(dist / 1000, 2) if isinstance(dist, (int, float)) else "—"
        cal = w.get("calories", "—")
        fc_prom = w.get("average_hr") or w.get("heart_rate_average") or "—"
        fc_max = w.get("max_hr") or w.get("heart_rate_maximum") or "—"
        ini = (w.get("time_start") or w.get("start") or "")[:16].replace("T", " ")
        print(f"    - {str(dep):<16} {str(km):>6} km  ·  {ini}  ·  "
              f"FC {fc_prom}/{fc_max} lpm  ·  {cal} kcal  ·  [{prov or '?'}]")
    return len(workouts)


def sync_atleta(api_key, api_base, atleta, user_id, desde, hasta):
    out_dir = os.path.join(OUT_BASE, atleta)
    os.makedirs(out_dir, exist_ok=True)
    rango = f"{desde}_{hasta}"
    total_workouts = 0

    for etiqueta, ruta in SUMMARIES:
        data = bajar_resumen(api_key, api_base, user_id, ruta, desde, hasta)
        if data is None:
            continue
        path = os.path.join(out_dir, f"{etiqueta}_{rango}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if etiqueta == "workouts":
            n = _resumen_workouts(data)
            total_workouts += n
            print(f"[{atleta}] {n} workout(s) en {desde}..{hasta}.")

    return total_workouts


def main():
    parser = argparse.ArgumentParser(description="Bajar datos de atletas via Junction (agregador).")
    parser.add_argument("--atleta", default=None, help="Solo ese atleta. Sin esto, todos.")
    parser.add_argument("--dias", type=int, default=14, help="Ventana hacia atras (default 14).")
    parser.add_argument("--desde", default=None, help="Fecha inicio YYYY-MM-DD (sobreescribe --dias).")
    parser.add_argument("--hasta", default=None, help="Fecha fin YYYY-MM-DD (default hoy).")
    args = parser.parse_args()

    api_key, api_base = _cfg()
    store = load_store()
    if not store:
        sys.exit("\nNo hay atletas conectados. Conecta uno con:  "
                 "python agregador_connect.py --atleta <nombre>")

    hoy = datetime.now(timezone.utc).date()
    hasta = args.hasta or hoy.isoformat()
    desde = args.desde or (hoy - timedelta(days=args.dias)).isoformat()

    if args.atleta:
        if args.atleta not in store:
            sys.exit(f"\nNo encuentro al atleta '{args.atleta}'. Conectados: {', '.join(store.keys())}")
        atletas = {args.atleta: store[args.atleta]}
    else:
        atletas = store

    print(f"Atletas a sincronizar: {', '.join(atletas.keys())}  ({desde}..{hasta})\n")
    total = 0
    for atleta, datos in atletas.items():
        uid = datos.get("user_id")
        if not uid:
            print(f"[{atleta}] sin user_id, saltando. Reconecta con agregador_connect.py.")
            continue
        total += sync_atleta(api_key, api_base, atleta, uid, desde, hasta)

    os.makedirs(OUT_BASE, exist_ok=True)
    with open(os.path.join(OUT_BASE, "_ultima_sync.json"), "w", encoding="utf-8") as f:
        json.dump({"sincronizado": datetime.now(timezone.utc).isoformat(),
                   "rango": [desde, hasta], "workouts": total}, f, ensure_ascii=False, indent=2)

    print(f"\nListo. {total} workout(s) en total. Guardado en {OUT_BASE}")
    print("Ahora normaliza al esquema canonico con:  python tid_data.py\n")


if __name__ == "__main__":
    main()
