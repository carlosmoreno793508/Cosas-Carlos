#!/usr/bin/env python3
"""
polar_flow_import.py — Importa una sesión exportada de Polar Flow (H10) al esquema canónico.

Pensado para: Carlos corriendo en la CALLE con el Polar H10 + app Polar Flow/Beat.
Al volver, exportas la sesión desde Polar Flow y le pasas el archivo a este script.

Acepta:
  • TCX  (recomendado para GPS/ritmo/altitud) — Polar Flow > sesión > Export > TCX
  • CSV  (Polar Flow) — trae las muestras y, si está activado, los intervalos R-R (latido a latido)
Si tienes ambos, pásalos los dos y se combinan (TCX = GPS/pace, CSV = R-R para HRV).

Produce en datos/procesado/:
  • run_<sujeto>_<fecha>.json  — objeto compatible con el esquema (workout + hr_stream_resumen + hrv)
  • run_<sujeto>_<fecha>_rr.csv — los R-R (ms) latido a latido (base de HRV/DFA-alfa1)

Uso:
  python polar_flow_import.py sesion.tcx
  python polar_flow_import.py sesion.csv --subject carlos --fcmax 190 --fcrest 48
  python polar_flow_import.py sesion.tcx sesion.csv --subject carlos

Sin dependencias externas (solo librería estándar).
"""
import argparse
import csv
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from statistics import mean

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "datos", "procesado")

# ----------------------------------------------------------------------------- utilidades

def _f(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


def linfit(xs, ys):
    """Ajuste lineal mínimos cuadrados -> (pendiente, intercepto)."""
    n = len(xs)
    if n < 2:
        return 0.0, (ys[0] if ys else 0.0)
    mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return 0.0, my
    m = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den
    return m, my - m * mx


# ----------------------------------------------------------------------------- TCX

def parse_tcx(path):
    """Extrae muestras (t, hr, dist_m, alt, cad) + resumen de un TCX de Polar Flow."""
    ns = {"tcx": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    tree = ET.parse(path)
    root = tree.getroot()

    def tag(e):  # nombre sin namespace
        return e.tag.split("}")[-1]

    samples, start_iso, kcal = [], None, None
    for tp in root.iter():
        if tag(tp) != "Trackpoint":
            continue
        t = hr = dist = alt = cad = None
        for ch in tp:
            n = tag(ch)
            if n == "Time":
                t = ch.text
            elif n == "HeartRateBpm":
                for c in ch:
                    if tag(c) == "Value":
                        hr = _f(c.text)
            elif n == "DistanceMeters":
                dist = _f(ch.text)
            elif n == "AltitudeMeters":
                alt = _f(ch.text)
            elif n == "Cadence":
                cad = _f(ch.text)
        if t:
            if start_iso is None:
                start_iso = t
            samples.append({"t": t, "hr": hr, "dist_m": dist, "alt": alt, "cad": cad})
    # Calorías (si vienen en algún Lap)
    for e in root.iter():
        if tag(e) == "Calories" and e.text:
            kcal = (kcal or 0) + (_f(e.text) or 0)
    return samples, start_iso, kcal


# ----------------------------------------------------------------------------- CSV (Polar Flow)

def parse_polar_csv(path):
    """
    El CSV de Polar Flow trae 2 bloques: cabecera-resumen (2 filas) y luego las muestras
    (con encabezado propio). Detectamos la fila de encabezado de muestras y leemos HR + R-R.
    """
    with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return [], []
    # localizar la fila de encabezado de muestras (contiene "HR" o "Sample rate"/"Time")
    hdr_idx = None
    for i, r in enumerate(rows):
        low = [c.strip().lower() for c in r]
        if ("hr (bpm)" in low or "heart rate (bpm)" in low or "hr" in low) and ("time" in low or "sample rate" in low or "phase time" in low):
            hdr_idx = i
            break
    samples, rr = [], []
    if hdr_idx is not None:
        hdr = [c.strip().lower() for c in rows[hdr_idx]]

        def col(*names):
            for nm in names:
                if nm in hdr:
                    return hdr.index(nm)
            return None

        i_hr = col("hr (bpm)", "heart rate (bpm)", "hr")
        i_rr = col("r-r (ms)", "rr (ms)", "r-r interval (ms)")
        i_sp = col("speed (km/h)", "speed (mph)")
        i_pace = col("pace (min/km)", "pace (min/mi)")
        i_dist = col("distances (m)", "distance (m)", "distances (km)")
        for r in rows[hdr_idx + 1:]:
            if not any(c.strip() for c in r):
                continue
            hr = _f(r[i_hr]) if i_hr is not None and i_hr < len(r) else None
            if hr:
                samples.append({"hr": hr})
            if i_rr is not None and i_rr < len(r):
                v = _f(r[i_rr])
                if v and 250 < v < 2500:
                    rr.append(v)
    return samples, rr


# ----------------------------------------------------------------------------- métricas

def clean_rr(rr):
    """Filtra artefactos: rango fisiológico + salto >20% vs. anterior."""
    out = []
    prev = None
    for v in rr:
        if not (300 <= v <= 2000):
            prev = v
            continue
        if prev is not None and abs(v - prev) / prev > 0.20:
            continue
        out.append(v)
        prev = v
    return out


def hrv_metrics(rr):
    rr = clean_rr(rr)
    if len(rr) < 20:
        return {"n_rr": len(rr), "nota": "muy pocos R-R validos para HRV"}
    diffs = [rr[i + 1] - rr[i] for i in range(len(rr) - 1)]
    rmssd = math.sqrt(mean(d * d for d in diffs))
    m = mean(rr)
    sdnn = math.sqrt(mean((x - m) ** 2 for x in rr))
    nn50 = sum(1 for d in diffs if abs(d) > 50)
    pnn50 = 100 * nn50 / len(diffs)
    return {
        "n_rr": len(rr),
        "rr_medio_ms": round(m, 1),
        "rmssd_ms": round(rmssd, 1),
        "sdnn_ms": round(sdnn, 1),
        "pnn50_pct": round(pnn50, 1),
        "dfa_alfa1": dfa_alpha1(rr),
    }


def dfa_alpha1(rr, nmin=4, nmax=16):
    """Detrended Fluctuation Analysis, exponente de escala de corto plazo (alfa1)."""
    N = len(rr)
    if N < nmax * 2:
        return None
    m = mean(rr)
    y, acc = [], 0.0
    for v in rr:  # serie integrada
        acc += v - m
        y.append(acc)
    logn, logf = [], []
    for n in range(nmin, nmax + 1):
        nboxes = N // n
        if nboxes < 1:
            continue
        rms_sum = 0.0
        for b in range(nboxes):
            seg = y[b * n:(b + 1) * n]
            xs = list(range(n))
            slope, inter = linfit(xs, seg)
            rms_sum += sum((seg[i] - (slope * i + inter)) ** 2 for i in range(n)) / n
        F = math.sqrt(rms_sum / nboxes)
        if F > 0:
            logn.append(math.log10(n))
            logf.append(math.log10(F))
    if len(logn) < 3:
        return None
    a1, _ = linfit(logn, logf)
    return round(a1, 3)


def zonas(samples, fcmax, fcrest):
    """Tiempo en 5 zonas por %FCmax (genérico) — asume ~1 muestra/seg."""
    z = [0, 0, 0, 0, 0]
    bounds = [0.60, 0.70, 0.80, 0.90]  # Z1<60,60-70,70-80,80-90,>90
    for s in samples:
        hr = s.get("hr")
        if not hr:
            continue
        p = hr / fcmax
        if p < bounds[0]:
            z[0] += 1
        elif p < bounds[1]:
            z[1] += 1
        elif p < bounds[2]:
            z[2] += 1
        elif p < bounds[3]:
            z[3] += 1
        else:
            z[4] += 1
    return {f"Z{i+1}_min": round(v / 60, 1) for i, v in enumerate(z)}


def trimp(samples, fcmax, fcrest):
    """TRIMP de Banister (hombres) — carga interna de la sesión, ~1 muestra/seg."""
    total = 0.0
    for s in samples:
        hr = s.get("hr")
        if not hr:
            continue
        hrr = (hr - fcrest) / (fcmax - fcrest)
        hrr = max(0.0, min(1.0, hrr))
        total += (1 / 60.0) * hrr * 0.64 * math.exp(1.92 * hrr)
    return round(total, 1)


# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Importa sesión de Polar Flow (H10) al esquema canónico.")
    ap.add_argument("files", nargs="+", help="archivo(s) .tcx y/o .csv de Polar Flow")
    ap.add_argument("--subject", default="carlos", help="de quién es la sesión (va en el nombre)")
    ap.add_argument("--deporte", default="Carrera", help="deporte de la sesión")
    ap.add_argument("--fcmax", type=int, default=190, help="FC máxima (para zonas/TRIMP)")
    ap.add_argument("--fcrest", type=int, default=50, help="FC en reposo (para TRIMP)")
    args = ap.parse_args()

    tcx_samples, csv_samples, rr = [], [], []
    start_iso, kcal = None, None
    for path in args.files:
        if not os.path.exists(path):
            sys.exit(f"No existe el archivo: {path}")
        ext = os.path.splitext(path)[1].lower()
        if ext == ".tcx":
            tcx_samples, start_iso, kcal = parse_tcx(path)
            print(f"TCX: {len(tcx_samples)} muestras")
        elif ext == ".csv":
            csv_samples, rr = parse_polar_csv(path)
            print(f"CSV: {len(csv_samples)} muestras, {len(rr)} intervalos R-R")
        else:
            print(f"  (ignorado, extensión no soportada: {path})")

    samples = tcx_samples or csv_samples  # TCX manda para stream/GPS
    if not samples and not rr:
        sys.exit("No pude leer muestras ni R-R. ¿Es un export de Polar Flow (TCX/CSV)?")

    hrs = [s["hr"] for s in samples if s.get("hr")]
    dur_min = round(len(samples) / 60.0, 1) if samples else None
    dists = [s["dist_m"] for s in samples if s.get("dist_m") is not None]
    km = round(max(dists) / 1000.0, 2) if dists else None

    fecha = (start_iso or datetime.now(timezone.utc).isoformat())[:10]
    workout = {
        "fecha": fecha,
        "inicio": start_iso,
        "dur_min": dur_min,
        "deporte": args.deporte,
        "fc_prom": round(mean(hrs)) if hrs else None,
        "fc_max": round(max(hrs)) if hrs else None,
        "km": km,
        "ritmo_min_km": round(dur_min / km, 2) if (dur_min and km) else None,
        "kcal": round(kcal) if kcal else None,
        "trimp": trimp(samples, args.fcmax, args.fcrest) if hrs else None,
        "zonas": zonas(samples, args.fcmax, args.fcrest) if hrs else None,
        "fuente": "polar_h10",
    }
    out = {
        "schema_version": "1.0",
        "sujeto": args.subject,
        "workout": workout,
        "hrv": hrv_metrics(rr) if rr else {"nota": "sin R-R (usa export CSV con R-R activado para HRV/DFA)"},
        "hr_stream_resumen": {"n_muestras": len(samples), "hz_aprox": 1},
        "nota": "Importado de Polar Flow. R-R = base de HRV/DFA-alfa1 (dato del H10).",
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    base = f"run_{re.sub(r'[^A-Za-z0-9_-]', '-', args.subject)}_{fecha}"
    jpath = os.path.join(OUT_DIR, base + ".json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    if rr:
        rpath = os.path.join(OUT_DIR, base + "_rr.csv")
        with open(rpath, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["rr_ms"])
            for v in clean_rr(rr):
                w.writerow([v])

    # resumen en pantalla
    w = workout
    print("\n──────── Sesión importada ────────")
    print(f"  {w['deporte']} · {w['fecha']} · {w['dur_min']} min" + (f" · {w['km']} km" if w['km'] else ""))
    if w["fc_prom"]:
        print(f"  FC prom {w['fc_prom']} / máx {w['fc_max']} lpm · TRIMP {w['trimp']}")
    if w["ritmo_min_km"]:
        print(f"  Ritmo {w['ritmo_min_km']} min/km")
    if rr:
        h = out["hrv"]
        print(f"  HRV: rMSSD {h.get('rmssd_ms')} ms · SDNN {h.get('sdnn_ms')} ms · DFA-α1 {h.get('dfa_alfa1')}  (n={h.get('n_rr')})")
    else:
        print("  HRV: sin R-R (exporta el CSV de Polar Flow con R-R para tener HRV/DFA)")
    print(f"\n  Guardado: {jpath}")


if __name__ == "__main__":
    main()
