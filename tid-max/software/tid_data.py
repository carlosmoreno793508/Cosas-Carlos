#!/usr/bin/env python3
"""
tid_data.py — Pipeline de datos de TID-MAX (procesamiento y normalización).

Toma TODO lo crudo de datos/ (WHOOP + Polar + registro de nado) y lo normaliza en un
**esquema canónico único** que los agentes AI van a consumir. Es la "única verdad".

Entradas (datos/):
  recovery_*.json, sueno_*.json, cycles_*.json, workouts_*.json, perfil_*.json,
  medidas_cuerpo_*.json  (WHOOP)  ·  registro-natacion.csv  (nado)  ·  polar_*.csv (Polar)

Salidas (datos/procesado/):
  daily.csv / daily.json      — una fila por día (todas las métricas fusionadas por fecha)
  workouts.csv                — una fila por sesión
  dataset.json                — todo junto (lo que leen los agentes)

Uso:
    python whoop_sync.py     # baja WHOOP
    python tid_data.py       # procesa y normaliza
"""
import os
import sys
import glob
import json
import csv
from datetime import datetime, timezone, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCRIPT_DIR, "datos")
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(DATA_DIR, "procesado")

SCHEMA_VERSION = "1.0"


def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _records(prefix):
    files = sorted(glob.glob(os.path.join(DATA_DIR, f"{prefix}_*.json")))
    if not files:
        return []
    with open(files[-1], encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"]
    return data if isinstance(data, list) else []


def _single(prefix):
    files = sorted(glob.glob(os.path.join(DATA_DIR, f"{prefix}_*.json")))
    if not files:
        return {}
    with open(files[-1], encoding="utf-8") as f:
        d = json.load(f)
    return d if isinstance(d, dict) else {}


def _to_local(dt_utc, tz_offset):
    if dt_utc is None:
        return None
    if tz_offset and len(tz_offset) >= 3:
        try:
            sign = -1 if tz_offset[0] == "-" else 1
            hh = int(tz_offset[1:3])
            mm = int(tz_offset[4:6]) if len(tz_offset) >= 6 else 0
            return dt_utc + sign * timedelta(hours=hh, minutes=mm)
        except (ValueError, IndexError):
            return dt_utc
    return dt_utc


def _round(v, n=1):
    return round(v, n) if isinstance(v, (int, float)) else None


def _kcal(kj):
    return round(kj * 0.239006) if isinstance(kj, (int, float)) else None


# ---------- Normalización al esquema canónico ----------
def build_daily():
    """Fusiona por fecha (YYYY-MM-DD) las métricas diarias de todas las fuentes."""
    daily = {}

    def row(date_str):
        return daily.setdefault(date_str, {"fecha": date_str, "fuentes": []})

    def mark(r, src):
        if src not in r["fuentes"]:
            r["fuentes"].append(src)

    for rec in _records("recovery"):
        d = _parse_dt(rec.get("created_at"))
        sc = rec.get("score") or {}
        if not d:
            continue
        r = row(d.date().isoformat())
        r["recovery_pct"] = sc.get("recovery_score")
        r["hrv_ms"] = _round(sc.get("hrv_rmssd_milli"))
        r["rhr_bpm"] = sc.get("resting_heart_rate")
        r["spo2_pct"] = sc.get("spo2_percentage")
        r["skin_temp_c"] = sc.get("skin_temp_celsius")
        mark(r, "whoop")

    for rec in _records("sueno"):
        d = _parse_dt(rec.get("start"))
        sc = rec.get("score") or {}
        stage = sc.get("stage_summary") or {}
        in_bed = stage.get("total_in_bed_time_milli")
        if not d:
            continue
        r = row(d.date().isoformat())
        r["sleep_perf_pct"] = sc.get("sleep_performance_percentage")
        r["sleep_hours"] = _round(in_bed / 3_600_000, 2) if isinstance(in_bed, (int, float)) else None
        r["resp_rate"] = _round(sc.get("respiratory_rate"))
        mark(r, "whoop")

    for rec in _records("cycles"):
        d = _parse_dt(rec.get("start"))
        sc = rec.get("score") or {}
        if not d:
            continue
        r = row(d.date().isoformat())
        r["strain"] = _round(sc.get("strain"), 2)
        r["kcal"] = _kcal(sc.get("kilojoule"))
        mark(r, "whoop")

    # Registro manual de nado
    path = os.path.join(DATA_DIR, "registro-natacion.csv")
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig", newline="") as f:
            for rec in csv.DictReader(f):
                s = (rec.get("fecha") or "").strip()
                d = None
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
                    try:
                        d = datetime.strptime(s, fmt)
                        break
                    except ValueError:
                        pass
                if not d:
                    continue
                r = row(d.date().isoformat())
                try:
                    r["swim_km"] = float((rec.get("km_natacion") or "0").replace(",", ".")) or None
                except ValueError:
                    r["swim_km"] = None
                try:
                    r["swim_sessions"] = int(float(rec.get("sesiones_nado") or 0)) or None
                except ValueError:
                    r["swim_sessions"] = None
                try:
                    r["pesas_min"] = int(float(rec.get("min_pesas") or 0)) or None
                except ValueError:
                    r["pesas_min"] = None
                mark(r, "manual")

    return [daily[k] for k in sorted(daily)]


def build_workouts():
    rows = []
    for rec in _records("workouts"):
        sc = rec.get("score") or {}
        tz = rec.get("timezone_offset")
        start = _to_local(_parse_dt(rec.get("start")), tz)
        end = _to_local(_parse_dt(rec.get("end")), tz)
        dist = sc.get("distance_meter")
        rows.append({
            "fecha": start.date().isoformat() if start else None,
            "inicio": start.strftime("%H:%M") if start else None,
            "fin": end.strftime("%H:%M") if end else None,
            "dur_min": round((end - start).total_seconds() / 60) if (start and end) else None,
            "deporte": rec.get("sport_name") or (f"sport {rec.get('sport_id')}" if rec.get("sport_id") is not None else None),
            "strain": _round(sc.get("strain"), 2),
            "fc_prom": sc.get("average_heart_rate"),
            "fc_max": sc.get("max_heart_rate"),
            "kcal": _kcal(sc.get("kilojoule")),
            "km_whoop": _round(dist / 1000, 2) if isinstance(dist, (int, float)) else None,
            "fuente": "whoop",
        })
    return sorted([r for r in rows if r["fecha"]], key=lambda x: x["fecha"], reverse=True)


def build_polar():
    """Resumen de cada captura BLE del Polar (FC latido a latido)."""
    out = []
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "polar_*.csv"))):
        name = os.path.basename(path)
        subject = name.replace("polar_", "").rsplit("_", 1)[0] if "_" in name else "?"
        hrs, rrs = [], []
        with open(path, encoding="utf-8", newline="") as f:
            for rec in csv.DictReader(f):
                try:
                    hr = int(rec.get("hr_bpm") or 0)
                    if hr > 0:
                        hrs.append(hr)
                except ValueError:
                    pass
                if rec.get("rr_ms"):
                    try:
                        rrs.append(float(rec["rr_ms"]))
                    except ValueError:
                        pass
        out.append({
            "archivo": name, "sujeto": subject, "muestras": len(hrs),
            "hr_prom": round(sum(hrs) / len(hrs)) if hrs else None,
            "hr_max": max(hrs) if hrs else None,
            "rr_muestras": len(rrs),
        })
    return out


def build_athlete():
    perfil = _single("perfil")
    body = _single("medidas_cuerpo")
    return {
        "nombre": f"{perfil.get('first_name', '')} {perfil.get('last_name', '')}".strip() or None,
        "altura_m": body.get("height_meter"),
        "peso_kg": body.get("weight_kilogram"),
        "fc_max": body.get("max_heart_rate"),
    }


def write_csv(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    daily = build_daily()
    workouts = build_workouts()
    polar = build_polar()
    athlete = build_athlete()

    if not any([daily, workouts, polar]):
        sys.exit(f"\nNo encontré datos en {DATA_DIR}. Corre primero:  python whoop_sync.py")

    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()

    dataset = {
        "schema_version": SCHEMA_VERSION,
        "generado_utc": stamp,
        "atleta": athlete,
        "daily": daily,
        "workouts": workouts,
        "polar_capturas": polar,
    }
    with open(os.path.join(OUT_DIR, "dataset.json"), "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "daily.json"), "w", encoding="utf-8") as f:
        json.dump(daily, f, ensure_ascii=False, indent=2)

    daily_cols = ["fecha", "recovery_pct", "hrv_ms", "rhr_bpm", "spo2_pct", "skin_temp_c",
                  "sleep_perf_pct", "sleep_hours", "resp_rate", "strain", "kcal",
                  "swim_km", "swim_sessions", "pesas_min", "fuentes"]
    write_csv(os.path.join(OUT_DIR, "daily.csv"),
              [{**r, "fuentes": "|".join(r.get("fuentes", []))} for r in daily], daily_cols)
    write_csv(os.path.join(OUT_DIR, "workouts.csv"), workouts,
              ["fecha", "inicio", "fin", "dur_min", "deporte", "strain", "fc_prom", "fc_max", "kcal", "km_whoop", "fuente"])

    fechas = [r["fecha"] for r in daily]
    print("\n============== TID-MAX · PIPELINE DE DATOS ==============")
    print(f"Atleta: {athlete.get('nombre') or '(sin nombre)'}")
    print(f"Días normalizados: {len(daily)}   ({fechas[0]} → {fechas[-1]})" if fechas else "Días: 0")
    print(f"Workouts: {len(workouts)}   |   Capturas Polar: {len(polar)}")
    print(f"Esquema canónico v{SCHEMA_VERSION}. Salida en: {OUT_DIR}/")
    print("  - dataset.json  (lo que leen los agentes AI)")
    print("  - daily.csv / daily.json / workouts.csv")
    print("========================================================\n")


if __name__ == "__main__":
    main()
