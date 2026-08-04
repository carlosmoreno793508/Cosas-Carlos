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

    # Sueño: WHOOP puede registrar VARIOS sueños por día (el nocturno + siestas).
    # Antes cada registro sobrescribía al anterior y solo quedaba UNO (se perdían las
    # siestas). Ahora AGREGAMOS por día: la arquitectura (profundo/REM/eficiencia) sale
    # del sueño PRINCIPAL, pero el TIEMPO DORMIDO total suma las siestas, y la deuda se
    # calcula contra ese total. Gael duerme siesta casi a diario para recuperar sueño
    # perdido, así que ignorarlas subestimaba sus horas e inflaba la deuda.
    def _asleep_ms(rec):
        st = (rec.get("score") or {}).get("stage_summary") or {}
        in_bed = st.get("total_in_bed_time_milli")
        awake = st.get("total_awake_time_milli") or 0
        return (in_bed - awake) if isinstance(in_bed, (int, float)) else None

    sueno_por_dia = {}
    for rec in _records("sueno"):
        d = _parse_dt(rec.get("start"))
        if not d:
            continue
        sueno_por_dia.setdefault(d.date().isoformat(), []).append(rec)

    def h(ms):
        return _round(ms / 3_600_000, 2) if isinstance(ms, (int, float)) else None

    for date_str, recs in sueno_por_dia.items():
        r = row(date_str)
        # Sueño PRINCIPAL = el no-siesta más largo (o el más largo si falta el flag 'nap').
        no_naps = [x for x in recs if not x.get("nap")]
        principal = max(no_naps or recs, key=lambda x: _asleep_ms(x) or 0)
        siestas = [x for x in recs if x is not principal]

        sc = principal.get("score") or {}
        stage = sc.get("stage_summary") or {}
        in_bed = stage.get("total_in_bed_time_milli")
        light = stage.get("total_light_sleep_time_milli")
        deep = stage.get("total_slow_wave_sleep_time_milli")   # sueño profundo (SWS)
        rem = stage.get("total_rem_sleep_time_milli")
        asleep_noche = _asleep_ms(principal)                   # dormido del sueño principal
        nap_ms = sum((_asleep_ms(x) or 0) for x in siestas)    # dormido de las siestas
        asleep_total = ((asleep_noche or 0) + nap_ms) or None  # dormido real del día

        r["sleep_perf_pct"] = sc.get("sleep_performance_percentage")
        r["sleep_efficiency_pct"] = _round(sc.get("sleep_efficiency_percentage"))
        r["sleep_consistency_pct"] = _round(sc.get("sleep_consistency_percentage"))
        r["sleep_hours"] = h(in_bed)                 # tiempo en cama (principal)
        r["sleep_asleep_h"] = h(asleep_total)        # dormido real TOTAL (noche + siestas)
        r["sleep_asleep_noche_h"] = h(asleep_noche)  # solo el sueño principal
        r["sleep_nap_h"] = h(nap_ms) if nap_ms else None
        r["n_siestas"] = len(siestas) or None
        r["sleep_deep_h"] = h(deep)
        r["sleep_rem_h"] = h(rem)
        r["sleep_light_h"] = h(light)
        # % de arquitectura sobre el sueño PRINCIPAL (las siestas no siempre traen fases).
        if asleep_noche and deep is not None:
            r["deep_pct"] = _round(deep / asleep_noche * 100)
        if asleep_noche and rem is not None:
            r["rem_pct"] = _round(rem / asleep_noche * 100)
        r["despertares"] = stage.get("disturbance_count")
        r["ciclos"] = stage.get("sleep_cycle_count")
        # Hora de acostarse y de despertar (del sueño PRINCIPAL), en hora LOCAL del atleta.
        tz = principal.get("timezone_offset")
        ini = _to_local(_parse_dt(principal.get("start")), tz)
        fin = _to_local(_parse_dt(principal.get("end")), tz)
        r["sleep_inicio"] = ini.strftime("%H:%M") if ini else None
        r["sleep_fin"] = fin.strftime("%H:%M") if fin else None
        # Deuda contra el sueño TOTAL. Excluimos el término 'need_from_recent_nap' de WHOOP:
        # ese campo ya descuenta la siesta de la necesidad; si además sumamos la siesta al
        # tiempo dormido, la contaríamos dos veces. Así el crédito por siesta aparece UNA vez.
        need = sc.get("sleep_needed") or {}
        need_ms = sum(v for k, v in need.items()
                      if isinstance(v, (int, float)) and "nap" not in k)
        if need_ms and asleep_total is not None:
            r["deuda_sueno_min"] = _round((need_ms - asleep_total) / 60_000)
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


def _percentil(vals, p):
    if not vals:
        return None
    s = sorted(vals)
    k = max(0, min(len(s) - 1, int(round((p / 100) * (len(s) - 1)))))
    return s[k]


def detecta_esfuerzo(serie, delta=18, sustain_s=25):
    """Detecta el arranque del esfuerzo en una serie [(datetime, hr), ...].
    Reposo = percentil 15 del pulso; el esfuerzo inicia cuando el HR se sostiene
    >= reposo+delta durante al menos sustain_s segundos (no un pico suelto)."""
    serie = [(t, hr) for t, hr in serie if t and isinstance(hr, (int, float)) and hr > 0]
    if len(serie) < 5:
        return None
    reposo = _percentil([hr for _, hr in serie], 15)
    umbral = reposo + delta
    n = len(serie)
    for i in range(n):
        if serie[i][1] < umbral:
            continue
        # ¿se sostiene 'sustain_s' segundos por encima del umbral desde aquí?
        j, ok = i, True
        while j < n and (serie[j][0] - serie[i][0]).total_seconds() < sustain_s:
            if serie[j][1] < umbral:
                ok = False
                break
            j += 1
        if ok and j > i:
            return {"hr_reposo": reposo, "umbral": umbral,
                    "inicio_iso": serie[i][0].isoformat(),
                    "inicio_hr": serie[i][1],
                    "seg_desde_captura": round((serie[i][0] - serie[0][0]).total_seconds())}
    return None


def build_polar():
    """Resumen de cada captura BLE del Polar (FC latido a latido) + arranque de esfuerzo."""
    out = []
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "polar_*.csv"))):
        name = os.path.basename(path)
        subject = name.replace("polar_", "").rsplit("_", 1)[0] if "_" in name else "?"
        hrs, rrs, serie = [], [], []
        with open(path, encoding="utf-8", newline="") as f:
            for rec in csv.DictReader(f):
                try:
                    hr = int(rec.get("hr_bpm") or 0)
                except ValueError:
                    hr = 0
                if hr > 0:
                    hrs.append(hr)
                    t = _parse_dt(rec.get("t_iso"))
                    if t:
                        serie.append((t, hr))
                if rec.get("rr_ms"):
                    try:
                        rrs.append(float(rec["rr_ms"]))
                    except ValueError:
                        pass
        esfuerzo = detecta_esfuerzo(serie)
        out.append({
            "archivo": name, "sujeto": subject, "muestras": len(hrs),
            "hr_prom": round(sum(hrs) / len(hrs)) if hrs else None,
            "hr_max": max(hrs) if hrs else None,
            "rr_muestras": len(rrs),
            "esfuerzo": esfuerzo,
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


def build_evento():
    """Evento objetivo + fase calculada (carga/taper/pico) según los días que faltan."""
    ev = {}
    for p in (os.path.join(DATA_DIR, "evento.json"), os.path.join(SCRIPT_DIR, "evento.json")):
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                ev = json.load(f)
            break
    if not ev:
        return None

    hoy = datetime.now().date()

    def dias_hasta(key):
        try:
            return (datetime.strptime(ev[key], "%Y-%m-%d").date() - hoy).days
        except (KeyError, ValueError, TypeError):
            return None

    d = dias_hasta("fecha_inicio")
    if d is None:
        fase = None
    elif d < 0:
        fase = "post-evento"
    elif d <= 7:
        fase = "competencia / pico"
    elif d <= 21:
        fase = "taper (afinamiento)"
    else:
        fase = "carga"

    return {
        "nombre": ev.get("nombre"),
        "sede": ev.get("sede"),
        "fecha_inicio": ev.get("fecha_inicio"),
        "fecha_fin": ev.get("fecha_fin"),
        "fecha_viaje": ev.get("fecha_viaje"),
        "meta": ev.get("meta"),
        "dias_al_evento": d,
        "dias_al_viaje": dias_hasta("fecha_viaje"),
        "fase": fase,
    }


def build_plan_semana():
    """Semana del macrociclo (plan-macro.json) que cae en la fecha de hoy: km/ses/fase planeados."""
    plan = {}
    for p in (os.path.join(DATA_DIR, "plan-macro.json"), os.path.join(SCRIPT_DIR, "plan-macro.json")):
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                plan = json.load(f)
            break
    semanas = plan.get("semanas") or []
    if not semanas:
        return None
    hoy = datetime.now().date()
    for idx, s in enumerate(semanas):
        try:
            ini = datetime.strptime(s["inicio"], "%Y-%m-%d").date()
            fin = datetime.strptime(s["fin"], "%Y-%m-%d").date()
        except (KeyError, ValueError, TypeError):
            continue
        if ini <= hoy <= fin:
            prev = semanas[idx - 1] if idx > 0 else {}
            return {
                "semana": f"{s['inicio']} → {s['fin']}",
                "fase_plan": s.get("fase"),
                "km_plan": s.get("km"),
                "ses_plan": s.get("ses"),
                "comp": s.get("comp"),
                "km_plan_prev": prev.get("km"),
            }
    return None


DIAS_KEY = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]

# Clasifica un workout de WHOOP en agua / seco / otro, SOLO por el nombre del deporte.
# (Nada de heurísticas por duración: una caminata a la basura NO es entrenamiento.)
AGUA_KW = ("swim", "natac", "pool", "water")
SECO_KW = ("weight", "strength", "functional", "yoga", "pilates", "stretch",
           "mobility", "gym", "pesas", "fuerza", "estiram", "movil", "pilate")
# Actividad incidental que WHOOP autodetecta y NO es entrenamiento (no suma carga).
OTRO_KW = ("walk", "camin", "hik")


def _clasifica_deporte(w):
    n = (w.get("deporte") or "").lower()
    if any(k in n for k in AGUA_KW):
        return "agua"
    if any(k in n for k in SECO_KW):
        return "seco"
    if any(k in n for k in OTRO_KW):
        return "otro"
    return "otro"


def build_zonas_fc():
    """Zonas de FC ancladas en datos reales del PE (perfil de nutricion-gael.json):
    FATmax, VT1 (umbral aeróbico) y VT2 (umbral anaeróbico) medidos, más FC máx y reposo.
    Si faltan umbrales, cae a %FCmáx. Nota: FC máx del PE es de CARRERA; en nado suele ser
    ~5-10 lpm menor."""
    cfg = {}
    for p in (os.path.join(DATA_DIR, "nutricion-gael.json"), os.path.join(SCRIPT_DIR, "nutricion-gael.json")):
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                cfg = json.load(f)
            break
    perfil = cfg.get("perfil") or {}
    fc_max = perfil.get("fc_max_carrera")
    fc_rep = perfil.get("fc_reposo")
    fatmax = perfil.get("fatmax_fc")
    vt1 = perfil.get("vt1_fc")
    vt2 = perfil.get("vt2_fc")
    if not fc_max:
        return None

    if vt1 and vt2 and fatmax:
        # Orden real del PE: VT1(143) < VT2(167) < FATmax(173) < FCmax(181).
        # El FATmax esta POR ENCIMA del VT2 (alta flexibilidad metabolica): no es el piso.
        zonas = [
            {"zona": "Z1 · Base aeróbica", "min": fc_rep or 0, "max": vt1 - 1, "uso": "recuperación, técnica, aeróbico ligero"},
            {"zona": "Z2 · Zona sensible (VT1–VT2)", "min": vt1, "max": vt2 - 1, "uso": "construcción de rendimiento aeróbico (a priorizar)"},
            {"zona": "Z3 · Umbral (≥VT2)", "min": vt2, "max": fatmax - 1, "uso": "trabajo de umbral; el lactato empieza a acumularse"},
            {"zona": "Z4 · Alta intensidad", "min": fatmax, "max": fc_max, "uso": "intervalos duros; FATmax aquí (quema grasa aun a alta intensidad)"},
        ]
        base = "umbrales medidos del PE (VT1<VT2<FATmax)"
    else:
        def pct(a, b):
            return round(fc_max * a), round(fc_max * b)
        z = [pct(.60, .70), pct(.70, .80), pct(.80, .90), pct(.90, 1.0)]
        nom = ["Z1 · Recuperación", "Z2 · Aeróbico", "Z3 · Umbral", "Z4 · VO₂/máx"]
        zonas = [{"zona": n, "min": a, "max": b, "uso": ""} for n, (a, b) in zip(nom, z)]
        base = "%FC máx (sin umbrales medidos)"

    return {"fc_max": fc_max, "fc_reposo": fc_rep, "vt1": vt1, "vt2": vt2, "fatmax": fatmax,
            "vo2max": perfil.get("vo2max"),
            "base": base, "nota": "FC máx de CARRERA; en nado ~5-10 lpm menor.", "zonas": zonas}


def build_nutricion(km_dia, seco_min, atleta):
    """Estima el gasto calórico del día y la ingesta objetivo (kcal + macros) por comida.
    BMR (Mifflin-St Jeor) + actividad no-entreno + gasto de nado/seco, con un pequeño
    margen de seguridad para no subalimentar. Es una ESTIMACIÓN para orientar, no una prescripción."""
    cfg = {}
    for p in (os.path.join(DATA_DIR, "nutricion-gael.json"), os.path.join(SCRIPT_DIR, "nutricion-gael.json")):
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                cfg = json.load(f)
            break
    perfil = cfg.get("perfil") or {}
    # El perfil manda sobre WHOOP: WHOOP puede traer la envergadura (2.08 m) como "altura".
    peso = perfil.get("peso_kg") or atleta.get("peso_kg")
    altura_cm = perfil.get("altura_cm") or (atleta.get("altura_m") * 100 if atleta.get("altura_m") else None)
    edad = perfil.get("edad")
    sexo = perfil.get("sexo", "M")
    if not (peso and altura_cm and edad):
        return None

    bmr = 10 * peso + 6.25 * altura_cm - 5 * edad + (5 if sexo == "M" else -161)
    tdee_base = bmr * perfil.get("factor_actividad_no_entreno", 1.45)
    kcal_entreno = (km_dia or 0) * perfil.get("kcal_por_km_nado", 230) \
        + (seco_min or 0) * perfil.get("kcal_por_min_seco", 6)
    kcal = (tdee_base + kcal_entreno) * (1 + perfil.get("margen_crecimiento_pct", 5) / 100)

    # Proteína fija por peso; grasa ~27% de las kcal; los carbohidratos son el resto
    # (así el combustible escala con el volumen de entrenamiento, como debe ser).
    prot_g = round(peso * 1.8)
    grasa_g = round(kcal * 0.27 / 9)
    carbs_g = max(round((kcal - prot_g * 4 - grasa_g * 9) / 4), round(peso * 3))
    split = {"desayuno": 0.30, "comida": 0.38, "cena": 0.27, "snacks_entreno": 0.05}
    return {
        "km_dia": km_dia,
        "kcal_objetivo": round(kcal / 10) * 10,
        "bmr": round(bmr),
        "kcal_entreno": round(kcal_entreno),
        "proteina_g": prot_g,
        "carbohidratos_g": carbs_g,
        "grasa_g": grasa_g,
        "kcal_por_comida": {k: round(kcal * v / 10) * 10 for k, v in split.items()},
    }


def build_sesiones_reales(workouts, dia_iso):
    """Sesiones reales de WHOOP para una fecha: horas de inicio/fin, duración, agua vs seco."""
    del_dia = [w for w in workouts if w.get("fecha") == dia_iso]
    if not del_dia:
        return None
    ses = []
    for w in sorted(del_dia, key=lambda x: x.get("inicio") or ""):
        ses.append({
            "inicio": w.get("inicio"), "fin": w.get("fin"), "dur_min": w.get("dur_min"),
            "deporte": w.get("deporte"), "tipo": _clasifica_deporte(w),
            "fc_prom": w.get("fc_prom"), "strain": w.get("strain"), "km_whoop": w.get("km_whoop"),
        })

    def horas(tipo):
        m = sum(s["dur_min"] for s in ses if s["tipo"] == tipo and isinstance(s["dur_min"], (int, float)))
        return round(m / 60, 1)

    h_agua, h_seco = horas("agua"), horas("seco")
    entreno = [s for s in ses if s["tipo"] in ("agua", "seco")]
    return {
        "fecha": dia_iso,
        "n_sesiones": len(entreno),          # solo entrenamiento (agua/seco); la caminata no cuenta
        "n_incidental": len(ses) - len(entreno),
        "horas_agua": h_agua,
        "horas_seco": h_seco,
        "horas_total": round(h_agua + h_seco, 1),  # carga real = agua + seco, sin incidentales
        "sesiones": ses,
    }


def build_plan_dias(km_semana):
    """Reparte km_semana por día según plan-semana.json (patrón + horarios). Devuelve hoy y mañana."""
    cfg = {}
    for p in (os.path.join(DATA_DIR, "plan-semana.json"), os.path.join(SCRIPT_DIR, "plan-semana.json")):
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                cfg = json.load(f)
            break
    dias = cfg.get("dias") or {}
    if not dias or not isinstance(km_semana, (int, float)):
        return None
    horarios = cfg.get("horarios") or {}
    total_peso = sum(d.get("peso", 0) for d in dias.values()) or 1

    def dia_plan(key):
        d = dias.get(key)
        if not d:
            return None
        km_dia = round(km_semana * d.get("peso", 0) / total_peso, 1)
        horas = d.get("horas") or horarios.get(d.get("tipo"), [])   # 'horas' por día sobrescribe
        split = d.get("split") or ([1.0] if km_dia else [])
        enfoque = d.get("enfoque") or []
        sesiones = []
        for i, frac in enumerate(split):
            sesiones.append({
                "hora": horas[i] if i < len(horas) else None,
                "km": round(km_dia * frac, 1),
                "enfoque": enfoque[i] if i < len(enfoque) else None,
            })
        return {"dia": key, "tipo": d.get("tipo"), "km_dia": km_dia, "sesiones": sesiones}

    hoy_idx = datetime.now().weekday()
    return {
        "hoy": dia_plan(DIAS_KEY[hoy_idx]),
        "manana": dia_plan(DIAS_KEY[(hoy_idx + 1) % 7]),
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
    evento = build_evento()
    plan_semana = build_plan_semana()
    plan_dias = build_plan_dias(plan_semana.get("km_plan")) if plan_semana else None
    sesiones_hoy = build_sesiones_reales(workouts, datetime.now().date().isoformat())
    km_hoy = (plan_dias or {}).get("hoy", {}).get("km_dia") if plan_dias else None
    seco_min_hoy = round((sesiones_hoy or {}).get("horas_seco", 0) * 60) if sesiones_hoy else 0
    nutricion_hoy = build_nutricion(km_hoy, seco_min_hoy, athlete)
    zonas_fc = build_zonas_fc()

    if not any([daily, workouts, polar]):
        sys.exit(f"\nNo encontré datos en {DATA_DIR}. Corre primero:  python whoop_sync.py")

    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()

    dataset = {
        "schema_version": SCHEMA_VERSION,
        "generado_utc": stamp,
        "atleta": athlete,
        "evento": evento,
        "plan_semana": plan_semana,
        "plan_dias": plan_dias,
        "sesiones_hoy": sesiones_hoy,
        "nutricion_hoy": nutricion_hoy,
        "zonas_fc": zonas_fc,
        "daily": daily,
        "workouts": workouts,
        "polar_capturas": polar,
    }
    with open(os.path.join(OUT_DIR, "dataset.json"), "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "daily.json"), "w", encoding="utf-8") as f:
        json.dump(daily, f, ensure_ascii=False, indent=2)

    daily_cols = ["fecha", "recovery_pct", "hrv_ms", "rhr_bpm", "spo2_pct", "skin_temp_c",
                  "sleep_perf_pct", "sleep_inicio", "sleep_fin", "sleep_hours",
                  "sleep_asleep_h", "sleep_asleep_noche_h",
                  "sleep_nap_h", "n_siestas", "sleep_deep_h", "sleep_rem_h",
                  "deep_pct", "rem_pct", "sleep_efficiency_pct", "sleep_consistency_pct",
                  "despertares", "deuda_sueno_min", "resp_rate", "strain", "kcal",
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
    for cap in polar:
        e = cap.get("esfuerzo")
        if e:
            hora = e["inicio_iso"][11:19]
            print(f"  Polar {cap['archivo']}: esfuerzo arranca {hora} "
                  f"(HR {round(e['inicio_hr'])} vs reposo {e['hr_reposo']}, "
                  f"{e['seg_desde_captura']}s tras iniciar)")
    if evento and evento.get("dias_al_evento") is not None:
        print(f"Evento: {evento['nombre']}  →  faltan {evento['dias_al_evento']} días "
              f"(fase: {evento['fase']}; vuelo en {evento['dias_al_viaje']} días)")
    if plan_semana:
        print(f"Plan semana: {plan_semana['fase_plan']}  —  {plan_semana['km_plan']} km / "
              f"{plan_semana['ses_plan']} ses planeados"
              + (f"  ({plan_semana['comp']})" if plan_semana.get("comp") else ""))
    if plan_dias and plan_dias.get("hoy"):
        h = plan_dias["hoy"]
        horas = " + ".join(s["hora"] for s in h["sesiones"] if s.get("hora"))
        print(f"Nado hoy ({h['dia']}): {h['tipo']} · {h['km_dia']} km" + (f" · {horas}" if horas else ""))
    if sesiones_hoy:
        sh = sesiones_hoy
        print(f"Sesiones reales hoy (WHOOP): {sh['n_sesiones']} · {sh['horas_total']} h "
              f"(agua {sh['horas_agua']} h · seco {sh['horas_seco']} h)")
    if nutricion_hoy:
        n = nutricion_hoy
        print(f"Nutrición hoy: ~{n['kcal_objetivo']} kcal  (P {n['proteina_g']}g · "
              f"C {n['carbohidratos_g']}g · G {n['grasa_g']}g)  para {n['km_dia']} km de nado")
    if zonas_fc:
        z = zonas_fc
        print(f"Zonas FC (reposo {z['fc_reposo']} · máx {z['fc_max']} · VT1 {z['vt1']} · VT2 {z['vt2']}):")
        for zz in z["zonas"]:
            print(f"   {zz['zona']:28} {zz['min']}–{zz['max']} lpm" + (f"  · {zz['uso']}" if zz['uso'] else ""))
    print(f"Esquema canónico v{SCHEMA_VERSION}. Salida en: {OUT_DIR}/")
    print("  - dataset.json  (lo que leen los agentes AI)")
    print("  - daily.csv / daily.json / workouts.csv")
    print("========================================================\n")


if __name__ == "__main__":
    main()
