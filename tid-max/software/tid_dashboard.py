#!/usr/bin/env python3
"""
tid_dashboard.py — Dashboard visual de TID-MAX (Capa 3, presentación).

Arma un dashboard HTML autocontenido (un solo archivo, sin dependencias externas) a partir de
la salida del coach (datos/procesado/coach-hoy.json) o, si no existe, del dataset canónico.
Muestra de un vistazo: cuenta regresiva al evento y fase, semáforo del día, vitales (recovery,
HRV, FC reposo, sueño, ACWR, strain), el plan de la semana del macrociclo y el veredicto + los
5 pilares del coach. Pensado para que Carlos, el entrenador y la mamá de Gael lo lean sin saber
de datos.

Uso:
    python tid_agent.py                 # genera coach-hoy.json (ideal, con IA)
    python tid_dashboard.py             # arma dashboard.html y lo abre
    python tid_dashboard.py --no-open   # solo lo genera
"""
import os
import sys
import json
import webbrowser
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROC = os.path.join(SCRIPT_DIR, "datos", "procesado")
COACH_JSON = os.path.join(PROC, "coach-hoy.json")
DATASET = os.path.join(PROC, "dataset.json")
OUT_HTML = os.path.join(SCRIPT_DIR, "dashboard.html")

SEM = {
    "verde":   {"label": "VERDE",   "cls": "good", "emoji": "🟢"},
    "amarillo": {"label": "AMARILLO", "cls": "warn", "emoji": "🟡"},
    "rojo":    {"label": "ROJO",    "cls": "crit", "emoji": "🔴"},
}

CSS = """
:root{
  --ground:#0a1622; --ground2:#0d1c2b; --card:#122232; --card2:#16293b;
  --ink:#eaf2f7; --muted:#89a3b6; --line:#1f3446; --accent:#22d3ee;
  --good:#35d39a; --warn:#f5b64c; --crit:#f8737f;
  --shadow:0 1px 0 rgba(255,255,255,.03),0 12px 32px rgba(0,0,0,.35);
}
@media (prefers-color-scheme: light){
  :root{
    --ground:#e9eff3; --ground2:#eef4f7; --card:#ffffff; --card2:#f4f8fa;
    --ink:#0e2230; --muted:#577182; --line:#d8e4ec; --accent:#0a97b0;
    --good:#0f9d6b; --warn:#c8811a; --crit:#d0505c;
    --shadow:0 1px 0 rgba(0,0,0,.02),0 10px 26px rgba(20,50,70,.10);
  }
}
:root[data-theme="dark"]{
  --ground:#0a1622; --ground2:#0d1c2b; --card:#122232; --card2:#16293b;
  --ink:#eaf2f7; --muted:#89a3b6; --line:#1f3446; --accent:#22d3ee;
  --good:#35d39a; --warn:#f5b64c; --crit:#f8737f;
  --shadow:0 1px 0 rgba(255,255,255,.03),0 12px 32px rgba(0,0,0,.35);
}
:root[data-theme="light"]{
  --ground:#e9eff3; --ground2:#eef4f7; --card:#ffffff; --card2:#f4f8fa;
  --ink:#0e2230; --muted:#577182; --line:#d8e4ec; --accent:#0a97b0;
  --good:#0f9d6b; --warn:#c8811a; --crit:#d0505c;
  --shadow:0 1px 0 rgba(0,0,0,.02),0 10px 26px rgba(20,50,70,.10);
}
*{box-sizing:border-box}
body{margin:0;background:
  radial-gradient(1200px 600px at 80% -10%, var(--ground2), transparent 60%), var(--ground);
  color:var(--ink);
  font-family:"SF Pro Text",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  line-height:1.5;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1020px;margin:0 auto;padding:28px 20px 56px;}
.num{font-variant-numeric:tabular-nums lining-nums;}
header.top{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:20px;}
.brand{font-weight:800;letter-spacing:.14em;font-size:.82rem;color:var(--accent);text-transform:uppercase;}
.brand small{color:var(--muted);font-weight:600;letter-spacing:.04em;margin-left:8px;}
.who{color:var(--muted);font-size:.86rem;}
.who b{color:var(--ink);}

.hero{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;margin-bottom:14px;}
@media(max-width:680px){.hero{grid-template-columns:1fr;}}
.panel{background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);
  border-radius:16px;padding:20px 22px;box-shadow:var(--shadow);}
.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.68rem;color:var(--muted);font-weight:700;}
.countdown{display:flex;align-items:baseline;gap:12px;margin-top:6px;}
.countdown .big{font-size:3.4rem;font-weight:800;line-height:1;letter-spacing:-.02em;}
.countdown .unit{color:var(--muted);font-weight:600;}
.evline{margin-top:10px;color:var(--ink);font-weight:600;}
.evsub{color:var(--muted);font-size:.9rem;margin-top:2px;}
.phase{display:inline-block;margin-top:12px;padding:5px 12px;border-radius:999px;
  border:1px solid var(--line);background:rgba(34,211,238,.08);color:var(--accent);
  font-weight:700;font-size:.8rem;letter-spacing:.02em;}

.sem{display:flex;flex-direction:column;justify-content:center;}
.sembadge{display:flex;align-items:center;gap:12px;}
.dot{width:46px;height:46px;border-radius:50%;flex:0 0 auto;box-shadow:0 0 0 6px color-mix(in srgb,var(--sc) 18%,transparent);background:var(--sc);}
.sem.good{--sc:var(--good)} .sem.warn{--sc:var(--warn)} .sem.crit{--sc:var(--crit)}
.semlabel{font-size:1.7rem;font-weight:800;letter-spacing:.02em;color:var(--sc);}
.semwhy{color:var(--muted);font-size:.9rem;margin-top:10px;}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:12px;margin:14px 0;}
.tile{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;}
.tile .k{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700;}
.tile .v{font-size:1.9rem;font-weight:800;letter-spacing:-.01em;margin-top:4px;}
.tile .v small{font-size:.9rem;color:var(--muted);font-weight:600;}
.chip{display:inline-block;margin-top:8px;font-size:.74rem;font-weight:700;padding:2px 8px;border-radius:999px;}
.chip.good{color:var(--good);background:color-mix(in srgb,var(--good) 15%,transparent);}
.chip.warn{color:var(--warn);background:color-mix(in srgb,var(--warn) 15%,transparent);}
.chip.crit{color:var(--crit);background:color-mix(in srgb,var(--crit) 15%,transparent);}
.chip.flat{color:var(--muted);background:color-mix(in srgb,var(--muted) 14%,transparent);}

.cols{display:grid;grid-template-columns:1fr 1.3fr;gap:14px;}
@media(max-width:680px){.cols{grid-template-columns:1fr;}}
.h{font-size:1rem;font-weight:800;margin:0 0 12px;letter-spacing:.01em;}
.planrow{display:flex;justify-content:space-between;gap:10px;padding:9px 0;border-bottom:1px dashed var(--line);}
.planrow:last-child{border-bottom:0;}
.planrow .lab{color:var(--muted);}
.planrow .val{font-weight:700;text-align:right;}
.note{margin-top:12px;font-size:.8rem;color:var(--muted);border-left:3px solid var(--accent);padding-left:10px;}

.nado{margin:14px 0;}
.nadogrid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
@media(max-width:680px){.nadogrid{grid-template-columns:1fr;}}
.daycol{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:12px 14px;}
.daylab{display:flex;justify-content:space-between;align-items:baseline;gap:8px;
  text-transform:uppercase;letter-spacing:.08em;font-size:.72rem;font-weight:800;color:var(--muted);margin-bottom:8px;}
.daysum{color:var(--accent);letter-spacing:0;font-size:.82rem;text-transform:none;}
.ses{display:flex;align-items:baseline;gap:10px;padding:6px 0;border-top:1px solid var(--line);}
.ses:first-of-type{border-top:0;}
.hora{flex:0 0 52px;font-weight:800;color:var(--ink);}
.sesk{flex:0 0 56px;font-weight:700;color:var(--accent);}
.senf{color:var(--muted);font-size:.86rem;}

.verdict{font-size:1.12rem;font-weight:700;margin:0 0 14px;text-wrap:balance;}
.pillar{display:flex;gap:12px;padding:11px 0;border-top:1px solid var(--line);}
.pillar:first-of-type{border-top:0;}
.pillar .pk{flex:0 0 116px;font-weight:800;color:var(--accent);font-size:.9rem;}
.pillar .pv{color:var(--ink);font-size:.94rem;}
.alerts{margin-top:14px;display:flex;flex-direction:column;gap:8px;}
.alert{display:flex;gap:10px;align-items:flex-start;background:color-mix(in srgb,var(--warn) 12%,transparent);
  border:1px solid color-mix(in srgb,var(--warn) 30%,transparent);border-radius:10px;padding:9px 12px;font-size:.88rem;}
.alert::before{content:"▲";color:var(--warn);font-size:.8rem;line-height:1.5;}
footer{margin-top:26px;color:var(--muted);font-size:.76rem;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;}
.toggle{cursor:pointer;background:var(--card);border:1px solid var(--line);color:var(--muted);
  border-radius:999px;padding:5px 12px;font-size:.76rem;font-weight:600;}
.toggle:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

TOGGLE_JS = """
(function(){
  var b=document.getElementById('themebtn');
  if(!b)return;
  b.addEventListener('click',function(){
    var r=document.documentElement;
    var cur=r.getAttribute('data-theme');
    var dark=cur? cur==='dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    r.setAttribute('data-theme', dark?'light':'dark');
  });
})();
"""


def fnum(v, dec=0):
    if not isinstance(v, (int, float)):
        return "—"
    return f"{v:.{dec}f}" if dec else f"{round(v)}"


def chip(text, cls):
    return f'<span class="chip {cls}">{text}</span>'


def delta_chip(pct, good_is_positive=True):
    if not isinstance(pct, (int, float)):
        return ""
    sign = "+" if pct > 0 else ""
    good = (pct > 0) if good_is_positive else (pct < 0)
    cls = "flat" if pct == 0 else ("good" if good else "crit")
    return chip(f"{sign}{pct}% vs base", cls)


def tile(k, v, unit="", extra=""):
    unit_html = f" <small>{unit}</small>" if unit else ""
    return (f'<div class="tile"><div class="k">{k}</div>'
            f'<div class="v num">{v}{unit_html}</div>{extra}</div>')


def build_html(p):
    f = p.get("hechos", {})
    sem = SEM.get(p.get("semaforo", "amarillo"), SEM["amarillo"])

    # --- vitales con semántica de color ---
    rec = f.get("recovery_pct")
    rec_cls = "crit" if isinstance(rec, (int, float)) and rec < 50 else ("warn" if isinstance(rec, (int, float)) and rec < 67 else "good")
    acwr = f.get("acwr")
    acwr_cls = "flat"
    if isinstance(acwr, (int, float)):
        acwr_cls = "crit" if acwr > 1.4 else ("good" if 0.8 <= acwr <= 1.3 else "warn")
    sueno = f.get("sueno_pct")
    sueno_extra = chip("meta ≥85%", "warn") if isinstance(sueno, (int, float)) and sueno < 85 else chip("óptimo", "good")

    tiles = "".join([
        tile("Recovery", fnum(rec), "%", chip({"good": "listo", "warn": "moderar", "crit": "cuidar"}[rec_cls], rec_cls)),
        tile("HRV", fnum(f.get("hrv_ms")), "ms", delta_chip(f.get("hrv_vs_base_pct"), good_is_positive=True)),
        tile("FC reposo", fnum(f.get("fc_reposo_lpm")), "lpm", delta_chip(f.get("fc_reposo_vs_base_pct"), good_is_positive=False)),
        tile("Sueño", fnum(sueno), "%", sueno_extra),
        tile("ACWR", fnum(acwr, 2), "", chip({"good": "en rango", "warn": "vigilar", "crit": "riesgo", "flat": "—"}[acwr_cls], acwr_cls)),
        tile("Strain hoy", fnum(f.get("strain_hoy"), 1), "", ""),
    ])

    # --- tendencia HRV 7d (señal preventiva) ---
    trend = f.get("hrv_tendencia_7d_pct")
    trend_html = ""
    if isinstance(trend, (int, float)):
        trend_html = f'<div class="note">Tendencia HRV 7d: {"+" if trend>0 else ""}{trend}% vs 7d previos — {"a la baja, vigilar fatiga" if trend<0 else "estable/al alza"}.</div>'

    # --- plan de la semana ---
    plan_rows = "".join([
        f'<div class="planrow"><span class="lab">Fase</span><span class="val">{f.get("fase_plan_semana") or "—"}</span></div>',
        f'<div class="planrow"><span class="lab">Km planeados</span><span class="val num">{fnum(f.get("km_plan_semana"))} km</span></div>',
        f'<div class="planrow"><span class="lab">Sesiones</span><span class="val num">{fnum(f.get("ses_plan_semana"))}</span></div>',
        f'<div class="planrow"><span class="lab">Carga de nado (semana)</span><span class="val num">{fnum(f.get("carga_referencia_km"))} km</span></div>',
        f'<div class="planrow"><span class="lab">Semana previa</span><span class="val num">{fnum(f.get("km_nado_semana_previa"))} km</span></div>',
    ])
    fuente = f.get("carga_referencia_fuente") or ""

    # --- nado hoy / mañana (con horarios) ---
    def sesiones_html(d):
        if not d:
            return '<div class="evsub">—</div>'
        if d.get("tipo") == "descanso" or not d.get("sesiones"):
            return '<div class="ses"><span class="hora">—</span><span class="sesk">Descanso</span></div>'
        rows = ""
        for s in d["sesiones"]:
            enf = f'<span class="senf">{s["enfoque"]}</span>' if s.get("enfoque") else ""
            rows += (f'<div class="ses"><span class="hora num">{s.get("hora") or "—"}</span>'
                     f'<span class="sesk num">{fnum(s.get("km"),1)} km</span>{enf}</div>')
        return rows

    hoy_p = f.get("plan_nado_hoy")
    man_p = f.get("plan_nado_manana")
    nado_html = ""
    if hoy_p or man_p:
        def daycard(titulo, d):
            head = f'{d["tipo"]} · {fnum(d.get("km_dia"),1)} km' if d else "—"
            return (f'<div class="daycol"><div class="daylab">{titulo}'
                    f'<span class="daysum">{head}</span></div>{sesiones_html(d)}</div>')
        nado_html = (f'<div class="panel nado"><h2 class="h">Nado</h2><div class="nadogrid">'
                     f'{daycard("HOY · " + (hoy_p["dia"] if hoy_p else ""), hoy_p)}'
                     f'{daycard("MAÑANA · " + (man_p["dia"] if man_p else ""), man_p)}'
                     f'</div></div>')

    # --- pilares + alertas ---
    pilares = "".join(
        f'<div class="pillar"><div class="pk">{k}</div><div class="pv">{v}</div></div>'
        for k, v in (p.get("pilares") or {}).items()
    )
    alertas = p.get("alertas") or []
    alertas_html = ""
    if alertas:
        alertas_html = '<div class="alerts">' + "".join(f'<div class="alert">{a}</div>' for a in alertas) + "</div>"

    dias = f.get("dias_al_evento")
    dias_str = fnum(dias) if isinstance(dias, (int, float)) else "—"
    viaje = f.get("dias_al_viaje")
    viaje_str = f"vuelo en {fnum(viaje)} días" if isinstance(viaje, (int, float)) else ""
    gen = p.get("generado_utc", "")[:10]
    motor = p.get("motor", "")

    return f"""<div class="wrap">
  <header class="top">
    <div><span class="brand">TID-MAX <small>· Coach del día</small></span></div>
    <div class="who">Atleta: <b>{p.get('atleta','Gael')}</b> · {gen}
      <button id="themebtn" class="toggle" type="button">tema</button></div>
  </header>

  <section class="hero">
    <div class="panel">
      <div class="eyebrow">Cuenta regresiva</div>
      <div class="countdown"><span class="big num">{dias_str}</span><span class="unit">días al evento</span></div>
      <div class="evline">{f.get('evento') or 'Evento objetivo'}</div>
      <div class="evsub">{(f.get('evento_sede') or '')}{(' · ' + viaje_str) if viaje_str else ''}</div>
      <span class="phase">Fase: {f.get('fase') or '—'}</span>
    </div>
    <div class="panel sem {sem['cls']}">
      <div class="eyebrow">Semáforo del día</div>
      <div class="sembadge"><div class="dot"></div><div class="semlabel">{sem['label']}</div></div>
      <div class="semwhy">{' · '.join(p.get('razones') or []) or '—'}</div>
    </div>
  </section>

  <section class="grid">{tiles}</section>
  {trend_html}
  {nado_html}

  <section class="cols">
    <div class="panel">
      <h2 class="h">Plan de la semana</h2>
      {plan_rows}
      <div class="note">{fuente}</div>
    </div>
    <div class="panel">
      <h2 class="h">Veredicto del coach</h2>
      <p class="verdict">{p.get('veredicto','—')}</p>
      {pilares}
      {alertas_html}
    </div>
  </section>

  <footer>
    <span>Motor: {motor} · los números los calcula el motor determinista; Claude los explica.</span>
    <span>TID-MAX · rendimiento y bienestar</span>
  </footer>
</div>"""


def load_payload():
    if os.path.exists(COACH_JSON):
        with open(COACH_JSON, encoding="utf-8") as fh:
            return json.load(fh)
    # sin coach-hoy.json: reconstruye desde el dataset con el motor por reglas
    if not os.path.exists(DATASET):
        sys.exit("No encuentro coach-hoy.json ni dataset.json. Corre primero:  python tid_data.py && python tid_agent.py")
    sys.path.insert(0, SCRIPT_DIR)
    import tid_agent
    with open(DATASET, encoding="utf-8") as fh:
        ds = json.load(fh)
    f = tid_agent.build_facts(ds)
    rep = tid_agent.rule_based_report(f)
    return {
        "generado_utc": datetime.now(timezone.utc).isoformat(),
        "atleta": f["atleta"], "semaforo": f["semaforo"], "razones": f["razones"],
        "veredicto": rep["veredicto"], "pilares": rep["pilares"], "alertas": rep["alertas"],
        "hechos": f, "motor": rep["motor"],
    }


def main():
    payload = load_payload()
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>TID-MAX · Coach del día</title><style>{CSS}</style></head>'
            f'<body>{build_html(payload)}<script>{TOGGLE_JS}</script></body></html>')
    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Dashboard escrito en: {OUT_HTML}")
    if "--no-open" not in sys.argv:
        try:
            webbrowser.open("file://" + OUT_HTML)
        except Exception:
            pass


if __name__ == "__main__":
    main()
