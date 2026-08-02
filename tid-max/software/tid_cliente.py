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
  <section class="tiles">
    <div class="tile"><div class="k">Descanso (recovery)</div><div class="v num">{rec}<small>%</small></div>{rec_chip}</div>
    <div class="tile"><div class="k">Variabilidad (HRV)</div><div class="v num">{round(f.get('hrv_ms') or 0)}<small>ms</small></div>{hrv_chip}</div>
    <div class="tile"><div class="k">Pulso en reposo</div><div class="v num">{f.get('fc_reposo_lpm','—')}<small>lpm</small></div>{chip('estable','good')}</div>
    <div class="tile"><div class="k">Sueño anoche</div><div class="v num">{sd.get('horas_anoche','—')}<small>h</small></div>{chip('corto','warn') if isinstance(sd.get('horas_anoche'),(int,float)) and sd['horas_anoche']<8 else chip('bien','good')}</div>
    <div class="tile"><div class="k">Capacidad aeróbica</div><div class="v num">{f.get('vo2max','—')}</div>{chip('élite (VO₂máx)','aqua')}</div>
  </section>
  <section class="card pad formwrap">
    <h2 class="h">Camino al evento — ¿va a llegar fresco?</h2>
    <p class="hsub">Su preparación se mantiene alta mientras el cansancio baja en el taper. Esa brecha = <b>qué tan fresco llega</b>.</p>
    <div class="legend">
      <span><i style="background:var(--fit)"></i><b>Preparación</b></span>
      <span><i style="background:var(--fat)"></i><b>Cansancio</b></span>
      <span><i style="background:var(--form);height:10px;width:10px;border-radius:2px"></i><b>Frescura</b> = la brecha</span>
    </div>
    <div id="chart"></div>
  </section>
  <section class="cols">
    <div class="card pad">
      <h2 class="h">Descanso 🌙</h2>
      <div class="row"><span class="lab">Horas dormidas (anoche)</span><span class="val num">{sd.get('horas_anoche','—')} h</span></div>
      <div class="row"><span class="lab">Promedio de la semana</span><span class="val num">{sd.get('horas_prom_7d','—')} h/noche</span></div>
      <div class="row"><span class="lab">Constancia de horarios</span><span class="val">{sd.get('consistencia_pct','—')}%</span></div>
      <div class="row"><span class="lab">Despertares / deuda</span><span class="val num">{sd.get('despertares','—')} · {sd.get('deuda_min','—')} min</span></div>
    </div>
    <div class="card pad">
      {_combustible_html(f, m, consumo)}
    </div>
  </section>
  <section class="card pad">
    <h2 class="h">Entrenamiento 🏊</h2>
    <div class="plan2">
      <div class="p"><div class="pl">Hoy</div><div class="pv">{hoy_txt}</div><div class="pd">{hoy_ses}</div></div>
      <div class="p"><div class="pl">Mañana</div><div class="pv">{man_txt}</div><div class="pd">{man_ses}</div></div>
    </div>
  </section>
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
