#!/usr/bin/env python3
"""
tid_cliente.py — Tarjeta CLIENTE de TID-MAX (imagen para la familia).

Genera el dashboard "de cliente" (lenguaje claro, para la mamá de Gael y para Gael) desde los
datos reales del día (datos/procesado/coach-hoy.json) y lo RENDERIZA a una imagen vertical
(PNG) lista para WhatsApp. Incluye la curva de forma (preparación vs cansancio → frescura)
rumbo al evento.

Uso:
    python tid_agent.py                 # genera coach-hoy.json (con IA, ideal)
    python tid_cliente.py               # arma cliente.html y renderiza cliente.png
    python tid_cliente.py --solo-html   # solo el HTML (no intenta renderizar)

Render (una vez):
    pip install playwright
    playwright install chromium         # o usa tu Google Chrome (lo detecta solo)
"""
import os
import sys
import json
import glob
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROC = os.path.join(SCRIPT_DIR, "datos", "procesado")
COACH_JSON = os.path.join(PROC, "coach-hoy.json")
CONSUMO_JSON = os.path.join(PROC, "consumo-hoy.json")
OUT_HTML = os.path.join(SCRIPT_DIR, "cliente.html")
OUT_PNG = os.path.join(SCRIPT_DIR, "cliente.png")
# Carpeta que sirve el tunel de Cloudflare (index.html = tarjeta del dia).
PUBLICO_DIR = os.path.join(SCRIPT_DIR, "publico")
PUBLICO_HTML = os.path.join(PUBLICO_DIR, "index.html")

SEM = {"verde": ("good", "Listo", "#0f9d6b"), "amarillo": ("warn", "Moderado", "#d98a1a"),
       "rojo": ("crit", "Cuidado", "#d4504f")}

# ---------- curva de forma (CTL/ATL/TSB desde el plan del macrociclo) ----------
PESOS = [11, 6, 11, 6, 12, 7, 0]  # Lun..Dom


def _plan_semanas():
    for p in (os.path.join(PROC, "..", "plan-macro.json"), os.path.join(SCRIPT_DIR, "plan-macro.json")):
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f).get("semanas", [])
    return []


def build_form(hoy):
    semanas = _plan_semanas()
    if not semanas:
        return []
    dailies = []
    for s in semanas:
        try:
            ini = datetime.strptime(s["inicio"], "%Y-%m-%d").date()
            fin = datetime.strptime(s["fin"], "%Y-%m-%d").date()
        except (KeyError, ValueError, TypeError):
            continue
        km = s.get("km") or 0
        d = ini
        while d <= fin:
            dailies.append((d, round(km * PESOS[d.weekday()] / 53, 1)))
            d += timedelta(days=1)
    dailies = [x for x in dailies if x[0] <= hoy + timedelta(days=21)]
    ctl = atl = 7.0
    rows = []
    for d, load in dailies:
        tsb = ctl - atl
        ctl += (load - ctl) / 42
        atl += (load - atl) / 7
        rows.append([d.isoformat()[5:], round(ctl, 2), round(atl, 2), round(tsb, 2), d.isoformat()])
    ini_disp = (hoy - timedelta(days=18))
    return [r[:4] for r in rows if r[4] >= ini_disp.isoformat()]


CSS = open(os.path.join(SCRIPT_DIR, "cliente-estilos.css"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(SCRIPT_DIR, "cliente-estilos.css")) else ""


def _fmt_nado(d):
    if not d:
        return ("—", "—")
    ses = "  ·  ".join(f"{x.get('hora') or ''} {x.get('km')}km".strip() for x in d.get("sesiones", []))
    return (f"{d.get('tipo','').capitalize()} · {d.get('km_dia')} km", ses)


def load_consumo():
    """Consumo registrado HOY (lo que Carlos mandó por foto/texto). None si no hay o es de otro día."""
    if not os.path.exists(CONSUMO_JSON):
        return None
    try:
        with open(CONSUMO_JSON, encoding="utf-8") as fh:
            d = json.load(fh)
    except Exception:
        return None
    return d if d.get("fecha") == datetime.now().date().isoformat() else None


def _combustible_html(f, m, consumo):
    """Tarjeta de combustible: solo meta si no hay consumo; consumido vs meta si sí."""
    meta_k = f.get("kcal_objetivo_hoy", "—")
    filas = [
        ("Energía objetivo", f'<span style="color:var(--aqua)">~{meta_k} kcal</span>'),
        ("Carbohidratos", f"{m.get('C','—')} g"),
        ("Proteína", f"{m.get('P','—')} g"),
        ("Grasa", f"{m.get('G','—')} g"),
    ]
    if not consumo:
        rows = "".join(
            f'<div class="row"><span class="lab">{a}</span><span class="val num">{b}</span></div>'
            for a, b in filas)
        return f'<h2 class="h">Combustible del día 🍽️</h2>{rows}'
    t = consumo.get("totales", {})
    meta = consumo.get("meta", {})
    mk = meta.get("kcal") or (meta_k if isinstance(meta_k, (int, float)) else 0) or 0
    ck = t.get("kcal", 0)
    pct = round(100 * ck / mk) if mk else 0
    falta_k = max(mk - ck, 0) if mk else 0
    chip_c = "good" if 90 <= pct <= 115 else ("warn" if pct < 90 else "crit")
    ncom = len(consumo.get("comidas", []))
    comidas = "".join(
        f'<div class="row"><span class="lab" style="font-size:.86rem">{c.get("hora","")} · {c.get("platillo","")}</span>'
        f'<span class="val num" style="font-weight:600">{c.get("kcal",0)} kcal</span></div>'
        for c in consumo.get("comidas", []))

    def cm(cons, met, u="g"):
        return f'{cons} / {met if met is not None else "—"} {u}'
    return (
        f'<h2 class="h">Combustible del día 🍽️ <span class="chip {chip_c}" '
        f'style="text-transform:none;letter-spacing:0">{pct}% de la meta</span></h2>'
        f'<div class="row"><span class="lab">Consumido ({ncom} comida{"s" if ncom!=1 else ""})</span>'
        f'<span class="val num">{cm(ck, mk, "kcal")}</span></div>'
        f'<div class="row"><span class="lab">Carbohidratos</span><span class="val num">{cm(t.get("carb_g",0), meta.get("carb_g"))}</span></div>'
        f'<div class="row"><span class="lab">Proteína</span><span class="val num">{cm(t.get("prot_g",0), meta.get("prot_g"))}</span></div>'
        f'<div class="row"><span class="lab">Grasa</span><span class="val num">{cm(t.get("grasa_g",0), meta.get("grasa_g"))}</span></div>'
        f'<div class="row"><span class="lab">Falta por cubrir</span>'
        f'<span class="val num" style="color:var(--aqua)">~{falta_k} kcal</span></div>'
        f'{comidas}')


def _hm(h):
    """Horas decimales -> 'H:MM'."""
    if not isinstance(h, (int, float)):
        return "—"
    t = round(h * 60)
    return f"{t // 60}:{t % 60:02d}"


def _mchip(txt, c):
    return f'<span class="chip {c}"><span class="dot"></span>{txt}</span>'


def _mrow(name, valnum, unit, chip_html, width, grad, rng=""):
    u = f'<small>{unit}</small>' if unit else ''
    r = f'<div class="mrng">{rng}</div>' if rng else ''
    w = max(3.0, min(100.0, float(width))) if isinstance(width, (int, float)) else 3.0
    return (f'<div class="mrow"><div class="mtop"><span class="mname">{name}</span>'
            f'<span class="mval"><span class="num">{valnum}{u}</span>{chip_html}</span></div>'
            f'<div class="track"><i style="width:{w:.0f}%;background:{grad}"></i></div>{r}</div>')


def _srow(name, val_html, chip_html=""):
    return (f'<div class="srow"><span class="lab">{name}</span>'
            f'<span class="rval">{val_html}{chip_html}</span></div>')


def _vitales_html(f):
    out = []
    rec = f.get("recovery_pct")
    if isinstance(rec, (int, float)):
        c = "good" if rec >= 67 else ("warn" if rec >= 34 else "crit")
        t = "óptimo" if rec >= 67 else ("moderar" if rec >= 34 else "rojo")
        grad = "linear-gradient(90deg,var(--good),var(--aqua))" if c == "good" else "linear-gradient(90deg,var(--crit),var(--warn))"
        out.append(_mrow("Recovery", rec, "%", _mchip(t, c), rec, grad, "≥ 67% verde · 34–66% ámbar · &lt; 33% rojo"))
    hrv = f.get("hrv_ms")
    if isinstance(hrv, (int, float)):
        base = f.get("hrv_base_ms")
        baja = base and hrv < base
        out.append(_mrow("HRV", round(hrv, 1), "ms", _mchip("baja" if baja else "estable", "warn" if baja else "good"),
                         hrv / 120 * 100, "linear-gradient(90deg,var(--fit),var(--form))", "por debajo de su base habitual" if baja else "en su base"))
    fcr = f.get("fc_reposo_lpm")
    if isinstance(fcr, (int, float)):
        elev = fcr > 58
        out.append(_mrow("FC en reposo", fcr, "lpm", _mchip("elevada" if elev else "estable", "warn" if elev else "good"),
                         (fcr - 40) / 30 * 100, "linear-gradient(90deg,var(--fit),var(--good))", "42–58 lpm en nadadores élite"))
    spo2 = f.get("spo2_pct")
    if isinstance(spo2, (int, float)):
        c = "good" if spo2 >= 95 else ("warn" if spo2 >= 93 else "crit")
        t = "óptimo" if spo2 >= 95 else ("aceptable" if spo2 >= 93 else "bajo")
        out.append(_mrow("Oxigenación · SpO₂", spo2, "%", _mchip(t, c), (spo2 - 90) / 10 * 100,
                         "linear-gradient(90deg,var(--fat),var(--warn))", "≥ 95% óptimo · 93–94% aceptable"))
    temp = f.get("skin_temp_c")
    if isinstance(temp, (int, float)):
        out.append(_mrow("Temperatura de piel", temp, "°C", _mchip("normal", "good"), 52,
                         "linear-gradient(90deg,var(--muted),var(--fit))", "dentro de ±0.5 °C de su base"))
    vo2 = f.get("vo2max")
    if vo2 is not None:
        out.append(_srow("Capacidad aeróbica", f'<span class="num">{vo2}</span>', _mchip("élite (VO₂máx)", "aqua")))
    return ('<section class="card pad"><h2 class="h">Recovery y señales vitales</h2>'
            '<p class="psub">con rango óptimo</p>' + "".join(out) + '</section>')


def _sueno_html(f):
    sd = f.get("sueno_detalle") or {}
    out = []
    encama = sd.get("en_cama_h"); real = sd.get("horas_anoche")
    despierto = (encama - real) if isinstance(encama, (int, float)) and isinstance(real, (int, float)) else None
    if isinstance(encama, (int, float)):
        good = 8 <= encama <= 9.6
        out.append(_mrow("Tiempo en cama", _hm(encama), "", _mchip("óptimo" if good else "revisar", "good" if good else "warn"),
                         encama / 9.5 * 100, "linear-gradient(90deg,var(--aqua),var(--good))", "8–9.5 h en cama"))
    if isinstance(real, (int, float)):
        nm = "Sueño real" + (f" · {_hm(despierto)} despierto" if isinstance(despierto, (int, float)) and despierto > 0 else "")
        out.append(_mrow(nm, _hm(real), "", _mchip("corto", "warn") if real < 8 else _mchip("bien", "good"),
                         real / 9 * 100, "linear-gradient(90deg,var(--aqua),var(--fit))", "de 8–10 h objetivo"))
    rem = sd.get("rem_h")
    if isinstance(rem, (int, float)):
        lab = "alto" if rem > 2.5 else ("óptimo" if rem >= 1.75 else "bajo")
        out.append(_mrow("REM · técnica y memoria", _hm(rem), "", _mchip(lab, "warn" if lab == "bajo" else "good"),
                         rem / 2.8 * 100, "linear-gradient(90deg,var(--form),#a07cf0)", "1:45–2:30 objetivo"))
    prof = sd.get("profundo_h")
    if isinstance(prof, (int, float)):
        ok = prof >= 1.5
        out.append(_mrow("Profundo · reparación", _hm(prof), "", _mchip("óptimo" if ok else "bajo", "good" if ok else "warn"),
                         prof / 2.3 * 100, "linear-gradient(90deg,var(--fit),#7c8ef0)", "≥ 1:30 objetivo"))
    lig = sd.get("ligero_h")
    if isinstance(lig, (int, float)):
        out.append(_mrow("Ligero", _hm(lig), "", _mchip("bajo", "warn"), lig / 3 * 100,
                         "linear-gradient(90deg,var(--muted),#9fb2be)",
                         "lectura orientativa — el sensor puede confundir fases si duerme boca abajo"))
    deuda = sd.get("deuda_min")
    if isinstance(deuda, (int, float)):
        c = "crit" if deuda > 120 else ("warn" if deuda > 30 else "good")
        t = "alta" if deuda > 120 else ("moderada" if deuda > 30 else "baja")
        out.append(_srow("Deuda de sueño", f'<span class="num">{_hm(deuda / 60)} h</span>', _mchip(t, c)))
    cons = sd.get("consistencia_pct")
    if isinstance(cons, (int, float)):
        c = "good" if cons >= 75 else ("warn" if cons >= 50 else "crit")
        t = "buena" if cons >= 75 else ("baja" if cons >= 50 else "muy baja")
        out.append(_srow("Constancia de horarios", f'<span class="num">{cons}%</span>', _mchip(t, c)))
    return ('<section class="card pad"><h2 class="h">😴 Sueño completo</h2>'
            '<p class="psub">con rango óptimo</p>' + "".join(out) + '</section>')


def _zonas_html(f):
    z = f.get("zonas_fc") or {}
    vt1, vt2, fm, fx = z.get("vt1"), z.get("vt2"), z.get("fatmax"), z.get("fc_max")
    rest = z.get("fc_reposo") or 60
    if not (vt1 and vt2 and fm and fx and fx > rest):
        return ""
    span = fx - rest
    w1, w2, w3, w4 = (vt1 - rest) / span * 100, (vt2 - vt1) / span * 100, (fm - vt2) / span * 100, (fx - fm) / span * 100
    p1, p2, p3 = w1, w1 + w2, w1 + w2 + w3
    bar = (f'<div class="zbar"><span style="width:{w1:.1f}%;background:#1f9d6b"></span>'
           f'<span style="width:{w2:.1f}%;background:#159fb4"></span>'
           f'<span style="width:{w3:.1f}%;background:#d99a1a"></span>'
           f'<span style="width:{w4:.1f}%;background:#df6a3a"></span></div>')
    marks = (f'<div class="zmarks"><b style="left:{p1:.1f}%"><i>VT1 {vt1}</i>aeróbico</b>'
             f'<b style="left:{p2:.1f}%"><i>VT2 {vt2}</i>anaeróbico</b>'
             f'<b style="left:{p3:.1f}%;top:20px"><i>FATmax {fm}</i>grasa máx.</b>'
             f'<b style="left:100%"><i>FCmáx {fx}</i>máxima</b></div>')
    prio = (f'<div class="zprio">Zona a priorizar en calidad: <b>{vt1}–{vt2} lpm</b> (entre VT1 y VT2). '
            f'El FATmax de Gael está <b>por encima del VT2</b> — hallazgo notable de alta flexibilidad '
            f'metabólica que marca el propio laboratorio.</div>')
    return ('<section class="card pad zonewrap"><h2 class="h">Zonas de frecuencia cardíaca</h2>'
            '<p class="psub">de su prueba de esfuerzo · PE Somnia</p>' + bar + marks + prio + '</section>')


def _forma_html(p, f):
    """Snapshot REAL de la forma de hoy (CTL/ATL/TSB del dato de WHOOP) + estado de pico."""
    forma = f.get("forma") or {}
    if not forma:
        return ""
    rend = p.get("rendimiento") or {}
    est = rend.get("estado", "")
    MAP = {"en_pico": ("En pico", "good"), "afinando": ("Afinando", "aqua"),
           "atrasado": ("Atrasado", "warn"), "construyendo": ("Construyendo", "fit"),
           "cargado": ("Cargado", "warn"), "estable": ("Estable", "good")}
    lbl, c = MAP.get(est, ("", ""))
    badge = f'<span class="chip {c}"><span class="dot"></span>{lbl}</span>' if lbl else ""
    tsb = forma.get("forma_tsb")
    tsb_txt = f"{tsb:+g}" if isinstance(tsb, (int, float)) else "—"

    def stat(k, v, color):
        return (f'<div style="flex:1;text-align:center">'
                f'<div style="font-size:.7rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)">{k}</div>'
                f'<div class="num" style="font-size:1.5rem;color:{color}">{v}</div></div>')
    stats = (stat("Preparación", forma.get("fitness_ctl", "—"), "var(--fit)")
             + stat("Cansancio", forma.get("fatiga_atl", "—"), "var(--fat)")
             + stat("Frescura", tsb_txt, "var(--form)"))
    lect = rend.get("lectura", "")
    lect_html = f'<p class="hsub" style="margin-top:10px">{lect}</p>' if lect else ""
    return (f'<div style="display:flex;align-items:center;gap:10px;margin:4px 0 8px">'
            f'<b>Estado de forma hoy</b> <small style="color:var(--muted)">(de su carga real)</small>{badge}</div>'
            f'<div style="display:flex;gap:8px;margin-bottom:4px">{stats}</div>{lect_html}')


def _plan_hoy_html(p, cls):
    pil = p.get("pilares") or {}
    if not pil:
        return ""
    li = "".join(f'<li><span class="b">{i}</span><span><b>{k}.</b> {v}</span></li>'
                 for i, (k, v) in enumerate(pil.items(), 1))
    return f'<section class="card pad planhoy {cls}"><h2 class="h">🎯 Plan de hoy</h2><ul>{li}</ul></section>'


def build_html(p):
    f = p.get("hechos", {})
    consumo = load_consumo()
    cls, lbl, color = SEM.get(p.get("semaforo", "amarillo"), SEM["amarillo"])
    rec = f.get("recovery_pct")
    hrv_t = f.get("hrv_tendencia_7d_pct")
    sd = f.get("sueno_detalle") or {}
    ev_dias = f.get("dias_al_evento")
    hoy_txt, hoy_ses = _fmt_nado(f.get("plan_nado_hoy"))
    man_txt, man_ses = _fmt_nado(f.get("plan_nado_manana"))
    kpc = f.get("kcal_por_comida") or {}
    m = f.get("macros_hoy") or {}
    form = build_form(datetime.now().date())
    veredicto = p.get("veredicto", "")

    def chip(txt, c):
        return f'<span class="chip {c}"><span class="dot"></span>{txt}</span>'

    hrv_chip = chip(f"{hrv_t:+d}% en 7 días", "crit" if isinstance(hrv_t, (int, float)) and hrv_t <= -8 else "good") if isinstance(hrv_t, (int, float)) else ""
    rec_chip = chip("moderar", "warn") if isinstance(rec, (int, float)) and rec < 67 else chip("listo", "good")

    return f"""<div class="wrap">
  <header class="top">
    <div class="brand"><span class="dot"></span>TID-MAX <small>· Rendimiento</small></div>
    <div style="display:flex;align-items:center;gap:14px">
      <button class="theme-toggle" onclick="tglTheme()" aria-label="Cambiar modo día/noche">🌙 Noche</button>
      <div class="athlete">Atleta<b>{p.get('atleta','Gael')}</b></div>
    </div>
  </header>
  <section class="hero">
    <div class="card pad">
      <div class="eyebrow">Próxima competencia</div>
      <div class="count"><span class="big num">{ev_dias if ev_dias is not None else '—'}</span><span class="u">días</span></div>
      <div class="evt">{f.get('evento','')}</div>
      <div class="evtsub">{f.get('evento_sede','')}</div>
      <span class="phase">◐ Fase: {f.get('fase','')}</span>
    </div>
    <div class="card pad ready {cls}">
      <div class="eyebrow">Preparación de hoy</div>
      <div class="rr"><div class="ring" style="background:{color}">{rec if rec is not None else '—'}</div>
        <div><div class="lbl" style="color:{color}">{lbl}</div><div class="sub">Recovery {rec}% · {', '.join(p.get('razones',[]))}</div></div></div>
      <div class="say">{veredicto}</div>
    </div>
  </section>
  <div class="grid2">
    {_vitales_html(f)}
    {_sueno_html(f)}
  </div>
  {_zonas_html(f)}
  <section class="card pad formwrap">
    <h2 class="h">Camino al evento — ¿va a llegar fresco?</h2>
    <p class="hsub">Su preparación se mantiene alta mientras el cansancio baja en el taper. Esa brecha = <b>qué tan fresco llega</b>.</p>
    {_forma_html(p, f)}
    <p class="hsub" style="margin-top:6px">Proyección según el plan del entrenador:</p>
    <div class="legend">
      <span><i style="background:var(--fit)"></i><b>Preparación</b></span>
      <span><i style="background:var(--fat)"></i><b>Cansancio</b></span>
      <span><i style="background:var(--form);height:10px;width:10px;border-radius:2px"></i><b>Frescura</b> = la brecha</span>
    </div>
    <div id="chart"></div>
  </section>
  <section class="cols">
    <div class="card pad">
      {_combustible_html(f, m, consumo)}
    </div>
    <div class="card pad">
      <h2 class="h">Entrenamiento 🏊</h2>
      <div class="plan2">
        <div class="p"><div class="pl">Hoy</div><div class="pv">{hoy_txt}</div><div class="pd">{hoy_ses}</div></div>
        <div class="p"><div class="pl">Mañana</div><div class="pv">{man_txt}</div><div class="pd">{man_ses}</div></div>
      </div>
    </div>
  </section>
  {_plan_hoy_html(p, cls)}
  <footer>TID-MAX · lo que mide el reloj, convertido en decisiones · orientación de bienestar (no médica)</footer>
</div>
<script>const D={json.dumps(form)};{CHART_JS}</script>"""


CHART_JS = r"""
// --- Modo dia/noche: sigue el telefono por defecto; el boton lo cambia a mano ---
function _esNoche(){var r=document.documentElement,t=r.getAttribute('data-theme');
  return t?t==='dark':window.matchMedia('(prefers-color-scheme:dark)').matches;}
function _pintaBoton(){var b=document.querySelector('.theme-toggle');if(b)b.textContent=_esNoche()?'☀️ Día':'🌙 Noche';}
function tglTheme(){document.documentElement.setAttribute('data-theme',_esNoche()?'light':'dark');_pintaBoton();
  if(window._redibuja)window._redibuja();}
_pintaBoton();
try{window.matchMedia('(prefers-color-scheme:dark)').addEventListener('change',function(){
  if(!document.documentElement.getAttribute('data-theme')){_pintaBoton();if(window._redibuja)window._redibuja();}});}catch(e){}
const W=1000,H=280,pl=44,pr=16,pt=18,pb=34;
window._redibuja=function(){
if(!(D&&D.length))return;
const xs=i=>pl+(W-pl-pr)*i/(D.length-1);
const vals=D.flatMap(d=>[d[1],d[2]]);const ymin=Math.floor(Math.min(...vals))-0.3,ymax=Math.ceil(Math.max(...vals))+0.3;
const ys=v=>pt+(H-pt-pb)*(1-(v-ymin)/(ymax-ymin));
const cs=k=>getComputedStyle(document.documentElement).getPropertyValue(k).trim();
const poly=idx=>D.map((d,i)=>`${xs(i).toFixed(1)},${ys(d[idx]).toFixed(1)}`).join(' ');
const area=D.map((d,i)=>`${xs(i).toFixed(1)},${ys(d[1]).toFixed(1)}`).join(' ')+' '+D.slice().reverse().map((d,i)=>`${xs(D.length-1-i).toFixed(1)},${ys(d[2]).toFixed(1)}`).join(' ');
const fit=cs('--fit'),fat=cs('--fat'),form=cs('--form'),line=cs('--line'),muted=cs('--muted');
let g=`<svg viewBox="0 0 ${W} ${H}">`;
for(let v=Math.ceil(ymin);v<=ymax;v++){const y=ys(v).toFixed(1);g+=`<line x1="${pl}" y1="${y}" x2="${W-pr}" y2="${y}" stroke="${line}"/>`;g+=`<text x="${pl-8}" y="${(ys(v)+4).toFixed(1)}" fill="${muted}" font-size="11" text-anchor="end">${v}</text>`;}
g+=`<polygon points="${area}" fill="${form}" opacity="0.14"/>`;
g+=`<polyline points="${poly(2)}" fill="none" stroke="${fat}" stroke-width="2.5"/>`;
g+=`<polyline points="${poly(1)}" fill="none" stroke="${fit}" stroke-width="2.5"/>`;
D.forEach((d,i)=>{if(i%6===0||i===D.length-1)g+=`<text x="${xs(i).toFixed(1)}" y="${H-pb+18}" fill="${muted}" font-size="10.5" text-anchor="middle">${d[0]}</text>`;});
g+='</svg>';document.getElementById('chart').innerHTML=g;};
_redibuja();
"""


def render_png(html_path, png_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False, "Playwright no instalado (pip install playwright && playwright install chromium)"
    url = "file://" + os.path.abspath(html_path)
    # Ubica un binario ya instalado (Chromium de Playwright o Google Chrome del sistema)
    exe_env = []
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if base:
        exe_env += glob.glob(os.path.join(base, "chromium-*", "chrome-linux", "chrome"))
        exe_env += glob.glob(os.path.join(base, "chromium-*", "chrome-mac*", "**", "Chromium"), recursive=True)
    with sync_playwright() as pw:
        browser = None
        intentos = [{"channel": "chrome"}, {}] + [{"executable_path": e} for e in exe_env]
        for kw in intentos:
            try:
                browser = pw.chromium.launch(args=["--no-sandbox"], **kw)
                break
            except Exception:
                continue
        if not browser:
            return False, "No pude abrir Chromium/Chrome. En Mac: instala Google Chrome, o corre 'playwright install chromium'."
        pg = browser.new_page(viewport={"width": 460, "height": 1000}, device_scale_factor=2, color_scheme="light")
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(400)
        pg.screenshot(path=png_path, full_page=True)
        browser.close()
    return True, png_path


def main():
    if not os.path.exists(COACH_JSON):
        sys.exit("No encuentro coach-hoy.json. Corre primero:  python tid_data.py && python tid_agent.py")
    with open(COACH_JSON, encoding="utf-8") as f:
        payload = json.load(f)
    body = build_html(payload)
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<style>{CSS}</style></head><body>{body}</body></html>')
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML: {OUT_HTML}")
    # Copia servible para el tunel de Cloudflare (link publico para la mama de Gael).
    os.makedirs(PUBLICO_DIR, exist_ok=True)
    with open(PUBLICO_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Público (para el túnel): {PUBLICO_HTML}")
    if "--solo-html" in sys.argv:
        return
    ok, detalle = render_png(OUT_HTML, OUT_PNG)
    print(("✅ Imagen: " if ok else "⚠️ ") + str(detalle))


if __name__ == "__main__":
    main()
