#!/usr/bin/env python3
"""
intervals_sync.py — Baja los datos de un atleta desde intervals.icu (gratis).

intervals.icu es un agregador GRATIS: con UNA API key ya trae Garmin, Strava, Polar,
COROS, Oura (lo que el atleta conecte en su cuenta). Esto reemplaza el export manual de
TCX para Carlos (Polar) y evita Junction ($/mes) para fuentes no-WHOOP.

Qué hace:
  1. GET /api/v1/athlete/<id>/activities  → entrenamientos (runs, etc.)
  2. GET /api/v1/athlete/<id>/wellness     → RHR, HRV, sueño, peso por día
  3. Los MAPEA al esquema WHOOP-shape que tid_data.py ya lee y los escribe en la carpeta
     del atleta (respeta TID_DATA_DIR del pipeline multiusuario):
       workouts_intervals.json · recovery_intervals.json · sueno_intervals.json
     Además guarda el crudo (intervals_raw_*.json) para depurar/validar en el primer run.

Auth (de la guía de la comunidad): basic auth, usuario literal "API_KEY", password = tu key.
Requiere User-Agent de navegador (Cloudflare bloquea el agente default). athlete id "0"
resuelve al dueño de la key.

Env:
  INTERVALS_API_KEY    — tu API key (intervals.icu → Settings → Developer). NUNCA en el repo.
  INTERVALS_ATHLETE_ID — opcional, default "0" (el dueño de la key).
  TID_DATA_DIR         — carpeta de datos del atleta (pipeline multiusuario).
  INTERVALS_DIAS       — cuántos días hacia atrás bajar (default 120).

Uso:
    export INTERVALS_API_KEY=...        # o en software/.env
    python intervals_sync.py
"""
import os
import sys
import json
import datetime as dt

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
API = "https://intervals.icu/api/v1"
OUT_DIR = os.environ.get("TID_DATA_DIR") or os.path.join(SCRIPT_DIR, "datos")
UA = "Mozilla/5.0 (TID-MAX intervals_sync)"


def _auth():
    key = (os.environ.get("INTERVALS_API_KEY") or "").strip()
    if not key:
        sys.exit("Falta INTERVALS_API_KEY (intervals.icu → Settings → Developer). Ponla en el .env o como env var.")
    return ("API_KEY", key)


def _get(path, params=None):
    r = requests.get(f"{API}{path}", params=params, auth=_auth(),
                     headers={"User-Agent": UA, "Accept": "application/json"}, timeout=60)
    if r.status_code == 401:
        sys.exit("401 de intervals.icu. Recuerda: el USUARIO es el texto literal 'API_KEY' y tu key va de password.")
    r.raise_for_status()
    return r.json()


def _save(name, obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


def _num(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _kj_from_cal(cal):
    c = _num(cal)
    return round(c * 4.184, 1) if c is not None else None


def map_workouts(acts):
    """intervals.icu activity → esquema WHOOP-shape que lee build_workouts (tid_data)."""
    out = []
    for a in acts or []:
        # intervals: type, start_date_local, moving_time(s), distance(m), average_heartrate,
        # max_heartrate, calories, icu_training_load
        out.append({
            "id": a.get("id"),
            "sport_name": a.get("type") or a.get("name"),
            "start": a.get("start_date_local") or a.get("start_date"),
            "end": a.get("end_date_local"),
            "timezone_offset": a.get("timezone"),
            "score": {
                "distance_meter": _num(a.get("distance")),
                "average_heart_rate": a.get("average_heartrate") or a.get("icu_average_heartrate"),
                "max_heart_rate": a.get("max_heartrate") or a.get("icu_max_heartrate"),
                "kilojoule": _kj_from_cal(a.get("calories")),
                # intervals usa 'training_load' (escala propia), no el strain 0-21 de WHOOP.
                # Lo pasamos aparte por si el coach lo quiere; no lo forzamos como 'strain'.
                "training_load": _num(a.get("icu_training_load")),
                "moving_time_s": _num(a.get("moving_time")),
            },
        })
    return out


def map_wellness(wells):
    """intervals.icu wellness (por día) → recovery_*.json y sueno_*.json WHOOP-shape."""
    recovery, sueno = [], []
    for w in wells or []:
        fecha = w.get("id") or w.get("date")   # intervals usa la fecha como id del wellness
        hrv = w.get("hrv") or w.get("rmssd")
        rhr = w.get("restingHR") or w.get("resting_hr")
        if hrv is not None or rhr is not None or w.get("readiness") is not None:
            recovery.append({
                "fecha": fecha,
                "score": {
                    "recovery_score": w.get("readiness"),   # intervals no siempre lo trae (WHOOP-only)
                    "hrv_rmssd_milli": _num(hrv),
                    "resting_heart_rate": _num(rhr),
                    "spo2_percentage": _num(w.get("spO2")),
                    "skin_temp_celsius": _num(w.get("skinTemp")),
                },
            })
        sleep_secs = _num(w.get("sleepSecs"))
        if sleep_secs:
            sueno.append({
                "fecha": fecha,
                "timezone_offset": None,
                "score": {
                    "stage_summary": {
                        "total_in_bed_time_milli": sleep_secs * 1000,
                    },
                    "sleep_score": w.get("sleepScore"),
                    "respiratory_rate": _num(w.get("respiration")),
                },
            })
    return recovery, sueno


def main():
    dias = int(os.environ.get("INTERVALS_DIAS") or 120)
    aid = (os.environ.get("INTERVALS_ATHLETE_ID") or "0").strip()
    hoy = dt.date.today()
    oldest = (hoy - dt.timedelta(days=dias)).isoformat()
    newest = hoy.isoformat()

    print(f"intervals.icu: atleta {aid} · {oldest} → {newest} → {OUT_DIR}")
    acts = _get(f"/athlete/{aid}/activities", {"oldest": oldest, "newest": newest})
    wells = _get(f"/athlete/{aid}/wellness", {"oldest": oldest, "newest": newest})
    print(f"  bajados: {len(acts or [])} entrenamientos · {len(wells or [])} días de wellness")

    # Crudo (para validar nombres de campo en el primer run)
    _save("intervals_raw_activities.json", acts)
    _save("intervals_raw_wellness.json", wells)

    workouts = map_workouts(acts)
    recovery, sueno = map_wellness(wells)
    _save("workouts_intervals.json", workouts)
    if recovery:
        _save("recovery_intervals.json", recovery)
    if sueno:
        _save("sueno_intervals.json", sueno)

    print(f"  mapeado: {len(workouts)} workouts · {len(recovery)} recovery · {len(sueno)} sueño")
    print("Listo. El pipeline (tid_data) ya puede normalizar estos archivos.")


if __name__ == "__main__":
    main()
