#!/usr/bin/env python3
"""
tid_coach.py — Demostración del ECOSISTEMA TID-MAX (motor + coach) con datos reales.

Bucle:  Datos (WHOOP + registro de nado)  ->  MOTOR determinista (métricas + reglas)
        ->  COACH v0 (recomendación diaria en lenguaje humano)  ->  reporte-diario.html

Es una prueba de la LÓGICA del producto con la fuente de datos que hoy tenemos (WHOOP).
Cuando llegue la pulsera propia / dato crudo, solo cambia la fuente; el motor y el coach siguen.

Uso:
    python whoop_sync.py        # (1) baja/actualiza datos de WHOOP
    python tid_coach.py         # (2) genera el reporte del día
    open reporte-diario.html    # (Mac)

Nota: orientación de RENDIMIENTO/BIENESTAR, no consejo médico ni diagnóstico.
"""
import os
import sys
import glob
import json
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCRIPT_DIR, "datos")
OUT_HTML = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SCRIPT_DIR, "reporte-diario.html")

GREEN, YELLOW, RED = "#1DB954", "#F5B301", "#E5484D"
INK, ACCENT, CYAN, MUTED = "#0B1220", "#16E0B5", "#0EA5E9", "#5A6B7B"


# ---------- Carga de datos ----------
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


def _series(prefix, key, date_field="created_at"):
    out = []
    for r in _records(prefix):
        sc = r.get("score") or {}
        d = _parse_dt(r.get(date_field))
        v = sc.get(key)
        if d and isinstance(v, (int, float)):
            out.append((d, v))
    return sorted(out, key=lambda x: x[0])


def _mean(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return sum(xs) / len(xs) if xs else None


def load_swim():
    path = os.path.join(DATA_DIR, "registro-natacion.csv")
    if not os.path.exists(path):
        return []
    import csv
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            s = (r.get("fecha") or "").strip()
            d = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
                try:
                    d = datetime.strptime(s, fmt)
                    break
                except ValueError:
                    pass
            if not d:
                continue
            try:
                km = float((r.get("km_natacion") or "0").replace(",", ".")) or 0
            except ValueError:
                km = 0
            rows.append({"fecha": d, "km": km})
    return sorted(rows, key=lambda x: x["fecha"])


# ---------- MOTOR determinista ----------
def engine():
    rec_score = _series("recovery", "recovery_score")
    hrv = _series("recovery", "hrv_rmssd_milli")
    rhr = _series("recovery", "resting_heart_rate")
    slp = _series("sueno", "sleep_performance_percentage", "start")
    strain = _series("cycles", "strain", "start")
    swim = load_swim()

    def last(s):
        return s[-1][1] if s else None

    hrv_vals = [v for _, v in hrv]
    rhr_vals = [v for _, v in rhr]
    hrv_base = _mean(hrv_vals[-30:]) if hrv_vals else None
    rhr_base = _mean(rhr_vals[-30:]) if rhr_vals else None
    hrv_today, rhr_today = last(hrv), last(rhr)
    hrv_dev = (hrv_today - hrv_base) / hrv_base if (hrv_today and hrv_base) else None
    rhr_dev = (rhr_today - rhr_base) / rhr_base if (rhr_today and rhr_base) else None

    # Carga: ACWR (agudo 7d : crónico 28d) sobre el strain diario
    s_vals = [v for _, v in strain]
    acute = _mean(s_vals[-7:])
    chronic = _mean(s_vals[-28:])
    acwr = acute / chronic if (acute and chronic) else None

    # Volumen de nado (real, registro manual)
    km_week = km_prev = None
    if swim:
        ref = swim[-1]["fecha"]
        km_week = round(sum(x["km"] for x in swim if (ref - x["fecha"]).days < 7), 1)
        km_prev = round(sum(x["km"] for x in swim if 7 <= (ref - x["fecha"]).days < 14), 1)

    return {
        "recovery": last(rec_score), "hrv": hrv_today, "hrv_base": hrv_base, "hrv_dev": hrv_dev,
        "rhr": rhr_today, "rhr_base": rhr_base, "rhr_dev": rhr_dev,
        "sleep": last(slp), "strain": last(strain), "acwr": acwr,
        "km_week": km_week, "km_prev": km_prev,
    }


def semaforo(m):
    """Combina las señales en un estado verde/amarillo/rojo + razones."""
    level = "verde"
    razones = []

    def esc(to, why):
        nonlocal level
        razones.append(why)
        order = {"verde": 0, "amarillo": 1, "rojo": 2}
        if order[to] > order[level]:
            level = to

    r = m["recovery"]
    if isinstance(r, (int, float)):
        if r < 34:
            esc("rojo", f"Recovery muy baja ({r:.0f}%)")
        elif r < 67:
            esc("amarillo", f"Recovery media ({r:.0f}%)")
    if m["hrv_dev"] is not None:
        if m["hrv_dev"] <= -0.20:
            esc("rojo", f"HRV {m['hrv_dev']*100:.0f}% vs tu base")
        elif m["hrv_dev"] <= -0.10:
            esc("amarillo", "HRV a la baja")
    if m["rhr_dev"] is not None:
        if m["rhr_dev"] >= 0.12:
            esc("rojo", "FC en reposo elevada")
        elif m["rhr_dev"] >= 0.05:
            esc("amarillo", "FC en reposo algo alta")
    if isinstance(m["sleep"], (int, float)) and m["sleep"] < 70:
        esc("amarillo", f"Sueño bajo ({m['sleep']:.0f}%)")
    if m["acwr"] and m["acwr"] > 1.3:
        esc("amarillo", f"Carga aguda alta (ACWR {m['acwr']:.2f})")
    if not razones:
        razones.append("Todas las señales en rango")
    return level, razones


# ---------- COACH v0 (reglas) ----------
def coach(m, level):
    good = level == "verde"
    warn = level == "amarillo"
    if level == "verde":
        veredicto = "Luz verde: el cuerpo está listo para entrenar fuerte."
        entreno = "Adelante con la sesión planeada (incluida la doble si toca). Puedes buscar calidad/intensidad."
    elif level == "amarillo":
        veredicto = "Precaución: el cuerpo pide moderar. Entrena, pero con cabeza."
        entreno = "Mantén la sesión pero baja volumen/intensidad ~10–20%. Prioriza técnica sobre esfuerzo máximo."
    else:
        veredicto = "Bandera roja: hoy toca recuperar, no forzar."
        entreno = "Sesión suave o de descarga (técnica, aeróbico ligero). Nada de series duras hoy."

    sueno = ("Dormir es tu mayor palanca: apunta a 8–9 h."
             if (not isinstance(m["sleep"], (int, float)) or m["sleep"] < 85) else
             "Buen descanso — mantén el horario constante.")
    hidratacion = ("Nadar deshidrata aunque no lo sientas: agua + electrolitos, sobre todo en días de doble sesión."
                   if (m["km_week"] or 0) >= 6 else "Hidrátate de forma constante durante el día.")
    nutricion = ("Alto volumen: sube carbohidratos alrededor de los entrenos y proteína para reparar (1.6–2 g/kg)."
                 if (m["km_week"] or 0) >= 6 else "Come balanceado; no te saltes la comida post-entreno.")
    if level == "rojo":
        recuperacion = "Movilidad, foam rolling y respiración lenta (activa el vago). Considera masaje/siesta."
    elif level == "amarillo":
        recuperacion = "Suma 10–15 min de movilidad y respiración; cuida la ventana de sueño."
    else:
        recuperacion = "Mantén tu rutina de movilidad; vas bien."

    alertas = []
    if m["hrv_dev"] is not None and m["hrv_dev"] <= -0.15:
        alertas.append("HRV cayó bastante vs tu línea base — señal temprana de fatiga/enfermedad. Vigila.")
    if m["rhr_dev"] is not None and m["rhr_dev"] >= 0.10:
        alertas.append("FC en reposo elevada — suele preceder a un resfriado o sobrecarga.")
    if m["acwr"] and m["acwr"] > 1.4:
        alertas.append(f"Carga aguda muy por encima de la crónica (ACWR {m['acwr']:.2f}) — riesgo de lesión; ojo con subir más.")

    return {
        "veredicto": veredicto,
        "pilares": {
            "Entrenamiento": entreno,
            "Sueño": sueno,
            "Hidratación": hidratacion,
            "Nutrición": nutricion,
            "Recuperación": recuperacion,
        },
        "alertas": alertas,
    }


# ---------- Salida ----------
def fmt(v, suf="", dec=0):
    if not isinstance(v, (int, float)):
        return "—"
    return f"{v:.{dec}f}{suf}"


def render_html(nombre, m, level, razones, plan):
    color = {"verde": GREEN, "amarillo": YELLOW, "rojo": RED}[level]
    etiqueta = {"verde": "LISTO", "amarillo": "PRECAUCIÓN", "rojo": "RECUPERAR"}[level]
    hoy = datetime.now().strftime("%d/%b/%Y")
    dev = lambda x: (f"{x*100:+.0f}% vs base" if isinstance(x, (int, float)) else "")

    def card(lbl, val, extra=""):
        return f"""<div class="card"><div class="lbl">{lbl}</div><div class="val">{val}</div>
        <div class="ex">{extra}</div></div>"""

    pilares = "".join(
        f"<div class='pilar'><div class='pt'>{k}</div><div class='pd'>{v}</div></div>"
        for k, v in plan["pilares"].items()
    )
    alertas = ""
    if plan["alertas"]:
        items = "".join(f"<li>{a}</li>" for a in plan["alertas"])
        alertas = f"<div class='alertas'><h3>⚠️ Alertas preventivas</h3><ul>{items}</ul></div>"

    acwr = m["acwr"]
    acwr_txt = f"{acwr:.2f}" if acwr else "—"
    acwr_note = ("zona segura" if acwr and 0.8 <= acwr <= 1.3 else
                 "spike de carga" if acwr and acwr > 1.3 else
                 "carga baja" if acwr and acwr < 0.8 else "")

    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TID-MAX Coach — {nombre}</title>
<style>
 *{{box-sizing:border-box;margin:0;padding:0}}
 body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#f4f6fa;color:#0B1220;padding:24px;max-width:860px;margin:auto}}
 .top{{background:{INK};color:#fff;border-radius:16px;padding:22px 24px;border-top:5px solid {ACCENT}}}
 .top h1{{font-size:22px}} .top .sub{{color:#8aa0b6;font-size:13px;margin-top:6px}}
 .estado{{display:flex;align-items:center;gap:16px;background:#fff;border-radius:16px;padding:20px 24px;margin-top:16px;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
 .dot{{width:54px;height:54px;border-radius:50%;background:{color};flex:0 0 auto;box-shadow:0 0 0 6px {color}22}}
 .estado .et{{font-size:12px;letter-spacing:.08em;color:{color};font-weight:700}}
 .estado .vd{{font-size:18px;font-weight:700;margin-top:2px}}
 .estado .rz{{font-size:13px;color:{MUTED};margin-top:4px}}
 .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin-top:16px}}
 .card{{background:#fff;border-radius:14px;padding:14px 16px;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
 .card .lbl{{font-size:11px;color:{MUTED};font-weight:700;letter-spacing:.05em}}
 .card .val{{font-size:24px;font-weight:800;margin-top:4px}}
 .card .ex{{font-size:11px;color:{MUTED};margin-top:2px}}
 h2{{font-size:15px;margin:22px 0 10px}}
 .pilar{{background:#fff;border-radius:12px;padding:12px 16px;margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,.05);border-left:4px solid {ACCENT}}}
 .pilar .pt{{font-weight:700;font-size:14px}} .pilar .pd{{font-size:14px;color:#33414f;margin-top:2px}}
 .alertas{{background:#fff3f3;border:1px solid {RED}55;border-radius:12px;padding:14px 18px;margin-top:14px}}
 .alertas h3{{font-size:14px;color:{RED};margin-bottom:6px}} .alertas li{{font-size:13px;margin-left:18px;margin-top:4px}}
 .ctx{{font-size:13px;color:{MUTED};margin-top:18px;font-style:italic}}
 .foot{{font-size:11px;color:#9fb3c8;margin-top:18px;border-top:1px solid #e3e9f0;padding-top:12px}}
</style></head><body>
 <div class="top"><h1>TID-MAX · Coach del día</h1>
   <div class="sub">Atleta: {nombre} &nbsp;·&nbsp; {hoy} &nbsp;·&nbsp; fuente: WHOOP (demo del ecosistema)</div></div>

 <div class="estado"><div class="dot"></div>
   <div><div class="et">{etiqueta}</div><div class="vd">{plan['veredicto']}</div>
   <div class="rz">{' · '.join(razones)}</div></div></div>

 <div class="cards">
   {card("RECOVERY", fmt(m['recovery'], '%'))}
   {card("HRV (rMSSD)", fmt(m['hrv'], ' ms', 0), dev(m['hrv_dev']))}
   {card("FC REPOSO", fmt(m['rhr'], ' lpm'), dev(m['rhr_dev']))}
   {card("SUEÑO", fmt(m['sleep'], '%'))}
   {card("KM SEMANA", fmt(m['km_week'], ' km', 1), f"antes: {fmt(m['km_prev'],' km',1)}")}
   {card("CARGA (ACWR)", acwr_txt, acwr_note)}
 </div>

 <h2>📋 Plan del día — 5 pilares</h2>
 {pilares}
 {alertas}

 <div class="ctx">Contexto: fase de <b>carga</b> (dobles Lun/Mié/Vie) rumbo al <b>taper</b> para el evento
 principal en <b>Vancouver</b>. El motor ajusta las señales a la línea base de Gael.</div>
 <div class="foot">Orientación de rendimiento/bienestar generada por el motor determinista + coach v0 de TID-MAX.
 No es consejo médico ni diagnóstico. En Fase 2 el texto del coach se potencia con la Claude API.</div>
</body></html>"""


def main():
    perfil = _single("perfil")
    nombre = f"{perfil.get('first_name', '')} {perfil.get('last_name', '')}".strip() or "Gael"
    m = engine()
    if m["recovery"] is None and m["hrv"] is None:
        sys.exit(f"\nNo encontré datos en {DATA_DIR}. Corre primero:  python whoop_sync.py")
    level, razones = semaforo(m)
    plan = coach(m, level)

    # Consola
    icon = {"verde": "🟢", "amarillo": "🟡", "rojo": "🔴"}[level]
    print("\n================ TID-MAX · COACH DEL DÍA ================")
    print(f"Atleta: {nombre}")
    print(f"Estado: {icon} {level.upper()}  —  {plan['veredicto']}")
    print(f"Señales: {' · '.join(razones)}")
    print(f"Recovery {fmt(m['recovery'],'%')} | HRV {fmt(m['hrv'],' ms')} | FC rep {fmt(m['rhr'],' lpm')} | "
          f"Sueño {fmt(m['sleep'],'%')} | Km sem {fmt(m['km_week'],' km',1)} | ACWR {m['acwr']:.2f}" if m['acwr'] else "")
    print("\nPlan (5 pilares):")
    for k, v in plan["pilares"].items():
        print(f"  • {k}: {v}")
    for a in plan["alertas"]:
        print(f"  ⚠️ {a}")
    print("========================================================")

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(render_html(nombre, m, level, razones, plan))
    print(f"\nReporte visual: {OUT_HTML}")
    print(f"Ábrelo con:  open \"{OUT_HTML}\"\n")


if __name__ == "__main__":
    main()
