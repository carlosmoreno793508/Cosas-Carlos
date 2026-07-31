#!/usr/bin/env python3
"""
tid_plan.py — Capa 2 (Coach + Plan) de TID-MAX: bosquejo del plan de entrenamiento.

Genera la vista "Tu Plan" (estilo Runna) para Gael rumbo a su evento:
  - Tarjeta del plan: evento, fecha, semanas, fase (Carga/Taper), progreso de km del bloque.
  - Coach del día: adapta la sesión de HOY según el Recovery de WHOOP (verde/amarillo/rojo).
  - Semana actual: sesiones de nado ESTRUCTURADAS por día (+ pesas), marcando hecho/hoy/próximo.

Fuente del plan:  datos/plan.json  (si no existe, usa plan-vancouver.ejemplo.json).
Datos de hoy:     WHOOP (recovery) para la adaptación; registro-natacion.csv para el progreso.

Uso:
    python tid_plan.py
    open plan-semanal.html      # en Mac

Nota: orientación de rendimiento/bienestar, no consejo médico. En Fase 2 el texto se potencia
con la Claude API (coach conversacional) y las sesiones se guían en vivo con la banda TID-MAX.
"""
import os
import sys
import glob
import json
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCRIPT_DIR, "datos")
OUT_HTML = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SCRIPT_DIR, "plan-semanal.html")

INK, ACCENT, CYAN, MUTED = "#0B1220", "#16E0B5", "#0EA5E9", "#5A6B7B"
GREEN, YELLOW, RED, INDIGO, ORANGE = "#1DB954", "#F5B301", "#E5484D", "#7C6CF6", "#FF8A3D"

DIAS = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]

# Biblioteca de sesiones de nado (nombre, set, km aprox, color)
SESIONES = {
    "aerobico":       ("Aeróbico base",  "Cal 400 · 8×200 @3:10 · 400 suave",            2.4, CYAN),
    "umbral":         ("Umbral",         "Cal 600 · 5×300 desc:20 · 300 suave",          2.4, ORANGE),
    "velocidad":      ("Velocidad",      "Cal 600 · 12×50 sprint · 8×100 @1:30 · 300",   2.2, RED),
    "tecnica":        ("Técnica",        "Drills 800 · 6×100 técnica · 400 suave",       2.0, INDIGO),
    "aerobico_largo": ("Aeróbico largo", "Cal 400 · 3000 continuo · 300 suave",          3.7, "#0284C7"),
    "recuperacion":   ("Recuperación",   "Suave continuo 1500 · respiración",            1.5, GREEN),
    "taper":          ("Taper",          "Cal 600 · 6×50 ritmo comp · 400 suave",        1.5, "#06B6D4"),
}


def load_plan():
    for path in (os.path.join(DATA_DIR, "plan.json"),
                 os.path.join(SCRIPT_DIR, "plan-vancouver.ejemplo.json")):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    sys.exit("No encontré plan.json ni la plantilla de ejemplo.")


def latest_recovery():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "recovery_*.json")))
    if not files:
        return None, None
    with open(files[-1], encoding="utf-8") as f:
        data = json.load(f)
    recs = data.get("records", data) if isinstance(data, dict) else data
    scored = []
    for r in recs:
        sc = r.get("score") or {}
        if isinstance(sc.get("recovery_score"), (int, float)):
            scored.append((r.get("created_at", ""), sc))
    if not scored:
        return None, None
    scored.sort(key=lambda x: x[0])
    hrvs = [s.get("hrv_rmssd_milli") for _, s in scored if isinstance(s.get("hrv_rmssd_milli"), (int, float))]
    base = sum(hrvs) / len(hrvs) if hrvs else None
    last = scored[-1][1]
    return last.get("recovery_score"), (last.get("hrv_rmssd_milli"), base)


def readiness_level(recovery, hrv_info):
    hrv, base = hrv_info if hrv_info else (None, None)
    dev = (hrv - base) / base if (hrv and base) else None
    if isinstance(recovery, (int, float)):
        if recovery < 34 or (dev is not None and dev <= -0.20):
            return "rojo"
        if recovery < 67 or (dev is not None and dev <= -0.10):
            return "amarillo"
        return "verde"
    return "verde"


def swim_km_block():
    path = os.path.join(DATA_DIR, "registro-natacion.csv")
    if not os.path.exists(path):
        return 0.0
    import csv
    total = 0.0
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            try:
                total += float((r.get("km_natacion") or "0").replace(",", "."))
            except ValueError:
                pass
    return round(total, 1)


def build_week(plan, today, taper, level):
    """Arma los 7 días de la semana actual con sus sesiones, aplicando fase y adaptación de hoy."""
    monday = today - timedelta(days=today.weekday())
    plantilla = plan.get("plantilla", {})
    pesas_dias = set(plan.get("pesas_dias", []))
    pesas_min = plan.get("pesas_min", 0)
    dias = []
    for i in range(7):
        fecha = monday + timedelta(days=i)
        clave = DIAS[i]
        tipos = list(plantilla.get(clave, []))
        es_hoy = fecha.date() == today.date()

        # Fase taper: sesiones más suaves
        if taper and tipos:
            tipos = ["taper" if t not in ("tecnica", "recuperacion") else t for t in tipos]
        # Adaptación de HOY según recovery
        nota_dia = ""
        if es_hoy and tipos:
            if level == "rojo":
                tipos = ["recuperacion"]
                nota_dia = "Ajustado por Recovery baja → hoy recuperar."
            elif level == "amarillo":
                nota_dia = "Recovery media → baja el volumen ~15%."

        sesiones = [SESIONES[t] for t in tipos if t in SESIONES]
        km = round(sum(s[2] for s in sesiones), 1)
        estado = "hoy" if es_hoy else ("hecho" if fecha.date() < today.date() else "prox")
        dias.append({
            "dia": clave, "fecha": fecha, "sesiones": sesiones, "km": km,
            "doble": len(sesiones) >= 2, "descanso": len(sesiones) == 0,
            "pesas": pesas_min if clave in pesas_dias else 0,
            "estado": estado, "es_hoy": es_hoy, "nota": nota_dia,
        })
    return dias


def render_html(plan, dias, fase, semana_x, semanas_plan, dias_evento, km_hecho, km_obj, level, coach_note):
    atleta = plan.get("atleta", "Atleta")
    evento = plan.get("evento", "Evento")
    meta = plan.get("meta", "")
    fcolor = {"verde": GREEN, "amarillo": YELLOW, "rojo": RED}[level]
    fetiqueta = {"verde": "LISTO", "amarillo": "PRECAUCIÓN", "rojo": "RECUPERAR"}[level]
    pct_sem = int(100 * semana_x / semanas_plan) if semanas_plan else 0
    pct_km = int(100 * km_hecho / km_obj) if km_obj else 0
    estado_lbl = {"hecho": "✓", "hoy": "●", "prox": "○"}

    filas = ""
    for d in dias:
        badge = ("DESCANSO" if d["descanso"] else ("DOBLE" if d["doble"] else "1 SESIÓN"))
        bcolor = (MUTED if d["descanso"] else (ORANGE if d["doble"] else CYAN))
        sess_html = ""
        if d["descanso"]:
            sess_html = "<div class='sess rest'>Descanso — movilidad opcional</div>"
        else:
            for nombre, sett, km, col in d["sesiones"]:
                sess_html += (f"<div class='sess' style='border-left-color:{col}'>"
                              f"<b>{nombre}</b> · <span class='km'>{km} km</span><br>"
                              f"<span class='set'>{sett}</span></div>")
        if d["pesas"]:
            sess_html += f"<div class='sess pesas'>🏋️ Pesas · {d['pesas']} min</div>"
        if d["nota"]:
            sess_html += f"<div class='dnote'>⚠ {d['nota']}</div>"
        hoy_cls = " hoy" if d["es_hoy"] else ""
        filas += (f"<div class='dia{hoy_cls}'>"
                  f"<div class='dcol'><div class='dname'>{estado_lbl[d['estado']]} {d['dia']}</div>"
                  f"<div class='ddate'>{d['fecha'].strftime('%d/%b')}</div>"
                  f"<div class='dbadge' style='background:{bcolor}'>{badge}</div></div>"
                  f"<div class='scol'>{sess_html}</div></div>")

    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>TID-MAX · Tu Plan — {atleta}</title>
<style>
 *{{box-sizing:border-box;margin:0;padding:0}}
 body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#f4f6fa;color:{INK};padding:22px;max-width:820px;margin:auto}}
 .top{{background:{INK};color:#fff;border-radius:16px;padding:20px 22px;border-top:5px solid {ACCENT}}}
 .top h1{{font-size:21px}} .top .sub{{color:#8aa0b6;font-size:13px;margin-top:5px}}
 .card{{background:#fff;border-radius:16px;padding:18px 20px;margin-top:14px;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
 .plan-h{{display:flex;justify-content:space-between;align-items:flex-start}}
 .plan-h .ev{{font-size:18px;font-weight:800}} .plan-h .mt{{font-size:13px;color:{MUTED};margin-top:2px}}
 .fase{{font-size:11px;font-weight:800;letter-spacing:.06em;color:#fff;background:{ORANGE};padding:5px 12px;border-radius:20px}}
 .fase.taper{{background:{INDIGO}}}
 .stats{{display:flex;gap:26px;margin-top:14px;flex-wrap:wrap}}
 .stat .n{{font-size:20px;font-weight:800}} .stat .l{{font-size:11px;color:{MUTED};text-transform:uppercase;letter-spacing:.04em}}
 .bar{{height:8px;background:#e6ecf3;border-radius:6px;margin-top:6px;overflow:hidden}}
 .bar > span{{display:block;height:100%;border-radius:6px}}
 .coach{{display:flex;gap:14px;align-items:center}}
 .dot{{width:44px;height:44px;border-radius:50%;background:{fcolor};flex:0 0 auto;box-shadow:0 0 0 6px {fcolor}22}}
 .coach .et{{font-size:11px;font-weight:800;color:{fcolor}}} .coach .tx{{font-size:15px;font-weight:600;margin-top:2px}}
 h2{{font-size:15px;margin:20px 4px 10px}}
 .dia{{display:flex;gap:14px;background:#fff;border-radius:12px;padding:12px 14px;margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
 .dia.hoy{{outline:2px solid {ACCENT};background:#f2fffb}}
 .dcol{{flex:0 0 84px;text-align:center}} .dname{{font-weight:800;font-size:14px}} .ddate{{font-size:11px;color:{MUTED};margin-bottom:6px}}
 .dbadge{{font-size:9px;font-weight:800;color:#fff;border-radius:10px;padding:3px 6px;display:inline-block}}
 .scol{{flex:1}}
 .sess{{border-left:4px solid {ACCENT};background:#fafcff;border-radius:8px;padding:8px 10px;margin-bottom:6px;font-size:13px}}
 .sess .km{{color:{CYAN};font-weight:700}} .sess .set{{color:#33414f;font-size:12px}}
 .sess.rest{{color:{MUTED};border-left-color:{MUTED};font-style:italic}}
 .sess.pesas{{border-left-color:#64748b;color:#33414f}}
 .dnote{{font-size:12px;color:{RED};margin-top:3px}}
 .foot{{font-size:11px;color:#9fb3c8;margin-top:16px;border-top:1px solid #e3e9f0;padding-top:12px}}
</style></head><body>
 <div class="top"><h1>TID-MAX · Tu Plan</h1>
   <div class="sub">Atleta: {atleta} &nbsp;·&nbsp; Coach IA (v0) &nbsp;·&nbsp; {datetime.now():%d/%b/%Y}</div></div>

 <div class="card">
   <div class="plan-h"><div><div class="ev">🏊 {evento}</div><div class="mt">{meta} · {plan.get('fecha_evento','')}</div></div>
     <div class="fase {'taper' if fase=='Taper' else ''}">{fase.upper()}</div></div>
   <div class="stats">
     <div class="stat"><div class="n">Semana {semana_x}/{semanas_plan}</div><div class="l">del plan</div>
       <div class="bar"><span style="width:{pct_sem}%;background:{ACCENT}"></span></div></div>
     <div class="stat"><div class="n">{dias_evento} días</div><div class="l">al evento</div></div>
     <div class="stat"><div class="n">{km_hecho:.0f} / {km_obj} km</div><div class="l">volumen del bloque</div>
       <div class="bar"><span style="width:{min(pct_km,100)}%;background:{CYAN}"></span></div></div>
   </div>
 </div>

 <div class="card coach"><div class="dot"></div>
   <div><div class="et">COACH DEL DÍA · {fetiqueta}</div><div class="tx">{coach_note}</div></div></div>

 <h2>📅 Semana actual — sesiones de nado</h2>
 {filas}

 <div class="foot">Plan generado por el motor + coach v0 de TID-MAX. Sesiones estructuradas de nado con
 adaptación diaria según Recovery (WHOOP). En Fase 2: coach conversacional (Claude API) y guía en vivo
 con la banda TID-MAX. Orientación de rendimiento, no consejo médico.</div>
</body></html>"""


def main():
    plan = load_plan()
    today = datetime.now()

    try:
        event = datetime.strptime(plan["fecha_evento"], "%Y-%m-%d")
    except (KeyError, ValueError):
        sys.exit("El plan necesita 'fecha_evento' en formato AAAA-MM-DD.")
    dias_evento = (event.date() - today.date()).days
    semanas_rest = max(0, (dias_evento + 6) // 7)
    semanas_plan = plan.get("semanas_plan", 12)
    semanas_taper = plan.get("semanas_taper", 2)
    semana_x = max(1, min(semanas_plan, semanas_plan - semanas_rest + 1))
    taper = 0 < semanas_rest <= semanas_taper
    fase = "Taper" if taper else ("Evento" if dias_evento <= 0 else "Carga")

    recovery, hrv_info = latest_recovery()
    level = readiness_level(recovery, hrv_info)
    coach_note = {
        "verde": "Todo en verde: dale a la sesión completa de hoy.",
        "amarillo": "El cuerpo pide moderar: cumple la sesión pero baja el volumen ~15%.",
        "rojo": "Recovery baja: hoy toca recuperar. Cambié tu sesión a nado suave/técnica.",
    }[level]

    km_hecho = swim_km_block()
    km_obj = plan.get("km_objetivo_bloque", 0)
    dias = build_week(plan, today, taper, level)

    # Consola
    print("\n================ TID-MAX · TU PLAN ================")
    print(f"{plan.get('evento')} — {plan.get('fecha_evento')}  ({dias_evento} días, fase {fase})")
    print(f"Semana {semana_x}/{semanas_plan} · volumen bloque {km_hecho:.0f}/{km_obj} km")
    print(f"Coach del día ({level}): {coach_note}\n")
    for d in dias:
        if d["descanso"]:
            print(f"  {d['dia']} {d['fecha']:%d/%b}: descanso")
        else:
            tag = "DOBLE" if d["doble"] else "1 sesión"
            sess = " | ".join(f"{n} ({km}km)" for n, _, km, _ in d["sesiones"])
            pesas = f" + pesas {d['pesas']}m" if d["pesas"] else ""
            hoy = "  <-- HOY" if d["es_hoy"] else ""
            print(f"  {d['dia']} {d['fecha']:%d/%b} [{tag}]: {sess}{pesas}{hoy}")
    print("==================================================")

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(render_html(plan, dias, fase, semana_x, semanas_plan, dias_evento,
                            km_hecho, km_obj, level, coach_note))
    print(f"\nVista del plan: {OUT_HTML}")
    print(f"Ábrelo con:  open \"{OUT_HTML}\"\n")


if __name__ == "__main__":
    main()
