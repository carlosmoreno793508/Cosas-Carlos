#!/usr/bin/env python3
"""
tid_agent.py — Agentes AI de TID-MAX (Capa 2) sobre la Claude API.

Lee el esquema canónico (datos/procesado/dataset.json que produce tid_data.py). El MOTOR
determinista calcula los hechos duros (recovery vs base, HRV/FC vs base, tendencias, ACWR,
volumen de nado, semáforo) y los AGENTES (Claude) los convierten en consejo en lenguaje natural.

Regla de oro: el LLM NO inventa números. El código calcula; el modelo interpreta y explica.
Sin ANTHROPIC_API_KEY (o sin el SDK), cae con gracia al texto por reglas — el producto sigue.

Agentes:
  coach       (por defecto)  Reporte del día: veredicto + plan de 5 pilares.
  preventivo  (--preventivo) Vigila señales tempranas de fatiga y escala (vigilar→descarga→fisio).
  q&a         (--pregunta)   Responde preguntas libres del entrenador sobre el dataset.

Salida estructurada: el coach escribe datos/procesado/coach-hoy.json (lo consume el dashboard).

Uso:
    python whoop_sync.py && python tid_data.py     # baja WHOOP y normaliza
    python tid_agent.py                            # coach del día
    python tid_agent.py --preventivo               # informe preventivo
    python tid_agent.py --pregunta "¿por qué bajó mi HRV esta semana?"
    python tid_agent.py --deporte running          # usa el módulo de Running (default: perfil/natación)
    python tid_agent.py --sin-ia                   # fuerza modo por reglas (no llama a Claude)

Módulos por deporte: cada deporte es una "lente" (deportes/<deporte>.json) = persona + enfoque +
qué hechos priorizar. NO tocan el motor; solo cambian el system prompt y el énfasis del contexto.

Requiere (modo IA):
    pip install anthropic
    export ANTHROPIC_API_KEY=...   # o  ant auth login
"""
import os
import sys
import json
import glob
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATASET = os.path.join(SCRIPT_DIR, "datos", "procesado", "dataset.json")
COACH_OUT = os.path.join(SCRIPT_DIR, "datos", "procesado", "coach-hoy.json")

MODEL = "claude-opus-5"  # el más capaz de uso general; claude-haiku-4-5 para abaratar a escala

# Guardrails UNIVERSALES (aplican a todos los deportes). Lo específico de cada deporte vive en
# su módulo (deportes/<deporte>.json): persona + enfoque + qué hechos priorizar.
GUARDRAILS_BASE = (
    "REGLAS ESTRICTAS (universales):\n"
    "1) Orientación de RENDIMIENTO y BIENESTAR, NO medicina. Nunca diagnostiques, nombres "
    "enfermedades ni sugieras fármacos. Ante una señal de alarma real, recomienda consultar a un "
    "profesional de la salud.\n"
    "2) NO inventes datos. Habla SOLO de los números que te doy en los HECHOS. Si algo falta, dilo.\n"
    "3) Atleta joven: nada de restricción calórica agresiva ni sobrecarga; tono responsable.\n"
    "4) El semáforo (verde/amarillo/rojo) YA lo decidió el motor; respétalo, no lo cambies.\n"
    "5) Sé concreto y breve. Cada consejo se apoya en una señal concreta de los HECHOS."
)

# ---------- Módulos por deporte (la "lente": persona + enfoque + prioridad de contexto) ----------
# Un módulo NO toca el motor: solo cambia el system prompt y qué hechos resaltar. El usuario elige
# su deporte en el perfil (o con --deporte). Cada deporte = un JSON en deportes/.
DEPORTES_DIR = os.path.join(SCRIPT_DIR, "deportes")

# Fallback embebido por si falta el JSON: preserva EXACTAMENTE el comportamiento de natación (Gael).
_SPORT_BUILTIN = {
    "natacion": {
        "deporte": "natacion", "nombre": "Natación",
        "persona": (
            "Eres el coach de TID-MAX, un asistente de rendimiento y bienestar para Gael, un nadador "
            "competitivo de alto nivel (19 años) que se prepara para su próxima competencia "
            "internacional. Los HECHOS te dicen el nombre del evento, los días que faltan y la fase "
            "(carga/taper/pico): úsalos. En taper la prioridad es LLEGAR FRESCO, no acumular carga. "
            "Hablas en español, claro y cercano, dirigiéndote a Gael y a su entrenador."),
        "enfoque": [
            "CARGA DE NADO: aún no hay registro medido, así que el PLAN del macrociclo SE TOMA COMO "
            "REAL (el entrenador lo cumple rigurosamente). 'km_nado_semana' y 'km_nado_semana_previa' "
            "YA vienen del plan; razónalos como el volumen real de la semana. No plantees un 'plan vs "
            "real' como déficit ni regañes por km faltantes.",
            "VACACIONES/DESCANSO: si 'fase_plan_semana' dice 'Vacaciones' o el km planeado es 0, es "
            "descanso PLANEADO. NO empujes entrenamiento ni km; enfoca en recuperación, sueño y "
            "actividad ligera opcional. Es parte del plan.",
            "INTENSIDAD POR FC: si vienen 'zonas_fc', prescribe con esas zonas REALES (VT1/VT2), no "
            "con porcentajes genéricos. Esa FC máx es de carrera; en nado va ~5-10 lpm menor. La "
            "'zona sensible' (VT1-VT2) es su motor.",
        ],
        "contexto_prioridad": ["zonas_fc", "acwr", "km_nado_semana", "recovery_pct",
                               "hrv_vs_base_pct", "sueno_pct", "plan_nado_hoy", "fase_plan_semana"],
    },
}


def load_sport(deporte):
    """Carga el módulo del deporte desde deportes/<deporte>.json; si falta, usa el builtin."""
    dep = (deporte or "natacion").lower()
    path = os.path.join(DEPORTES_DIR, f"{dep}.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return _SPORT_BUILTIN.get(dep, _SPORT_BUILTIN["natacion"])


def build_system(sport):
    """System prompt = persona del deporte + guardrails universales + enfoque del deporte."""
    enf = sport.get("enfoque") or []
    extra = ""
    if enf:
        extra = ("\n\nENFOQUE DEL DEPORTE (" + sport.get("nombre", "") + "):\n"
                 + "\n".join(f"- {e}" for e in enf))
    return f"{sport.get('persona', '')}\n\n{GUARDRAILS_BASE}{extra}"


def sport_focus_note(sport):
    """Nota para el prompt: qué hechos priorizar en este deporte (no filtra; solo resalta)."""
    pr = sport.get("contexto_prioridad") or []
    if not pr:
        return ""
    return ("\n\nPara este deporte (" + sport.get("nombre", "")
            + "), da más peso a estos hechos al aconsejar: " + ", ".join(pr) + ".")


# ---------- Carga del esquema canónico ----------
def load_dataset(path):
    if not os.path.exists(path):
        found = glob.glob(os.path.join(SCRIPT_DIR, "**", "dataset.json"), recursive=True)
        if found:
            path = found[0]
        else:
            sys.exit(
                f"\nNo encontré {path}.\nCorre primero:  python whoop_sync.py && python tid_data.py\n"
            )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _mean(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return sum(xs) / len(xs) if xs else None


# ---------- MOTOR determinista (calcula los hechos; el LLM no toca esto) ----------
def build_facts(ds):
    daily = ds.get("daily", [])
    atleta = ds.get("atleta", {})
    evento = ds.get("evento") or {}
    plan_sem = ds.get("plan_semana") or {}
    plan_dias = ds.get("plan_dias") or {}
    ses_hoy = ds.get("sesiones_hoy") or {}
    nutri = ds.get("nutricion_hoy") or {}
    zonas = ds.get("zonas_fc") or {}

    def col(key):
        return [r.get(key) for r in daily if isinstance(r.get(key), (int, float))]

    def last(key):
        c = col(key)
        return c[-1] if c else None

    hrv_vals, rhr_vals = col("hrv_ms"), col("rhr_bpm")
    hrv_base = _mean(hrv_vals[-30:]) if hrv_vals else None
    rhr_base = _mean(rhr_vals[-30:]) if rhr_vals else None
    hrv_today, rhr_today = last("hrv_ms"), last("rhr_bpm")
    hrv_dev = (hrv_today - hrv_base) / hrv_base if (hrv_today and hrv_base) else None
    rhr_dev = (rhr_today - rhr_base) / rhr_base if (rhr_today and rhr_base) else None

    # Tendencias 7d vs 7d previos (para el agente Preventivo)
    hrv_7d, hrv_prev7 = _mean(hrv_vals[-7:]), _mean(hrv_vals[-14:-7]) if len(hrv_vals) >= 8 else None
    rhr_7d, rhr_prev7 = _mean(rhr_vals[-7:]), _mean(rhr_vals[-14:-7]) if len(rhr_vals) >= 8 else None
    hrv_trend = (hrv_7d - hrv_prev7) / hrv_prev7 if (hrv_7d and hrv_prev7) else None
    rhr_trend = (rhr_7d - rhr_prev7) / rhr_prev7 if (rhr_7d and rhr_prev7) else None

    # Días recientes con recovery baja (<50%), consecutivos desde hoy hacia atrás
    rec_series = col("recovery_pct")
    dias_rec_baja = 0
    for v in reversed(rec_series):
        if v < 50:
            dias_rec_baja += 1
        else:
            break

    # Carga: ACWR (agudo 7d : crónico 28d) sobre el strain diario
    s_vals = col("strain")
    acute, chronic = _mean(s_vals[-7:]), _mean(s_vals[-28:])
    acwr = acute / chronic if (acute and chronic) else None

    # Volumen de nado. El PLAN del macrociclo SE TOMA COMO REAL (el entrenador lo cumple
    # rigurosamente) y es la fuente autoritativa del volumen: km de la semana y de la previa
    # salen del plan, y alimentan ACWR/tendencias y los pilares de hidratación/nutrición.
    # El registro manual (registro-natacion.csv) se conserva solo como dato informativo,
    # hasta que sea una fuente completa y validada.
    swim = col("swim_km")
    km_real = round(sum(swim[-7:]), 1) if (swim and sum(swim) > 0) else None
    km_plan = plan_sem.get("km_plan")
    km_plan_prev = plan_sem.get("km_plan_prev")
    if km_plan is not None:
        km_week, km_prev = km_plan, km_plan_prev
        carga_fuente = "plan del macrociclo tomado como real (el entrenador lo sigue riguroso)"
    else:
        km_week = km_real
        km_prev = round(sum(swim[-14:-7]), 1) if (swim and len(swim) > 7) else None
        carga_fuente = "registro real de nado"
    carga_km = km_week

    def pct(x):
        return round(x * 100) if isinstance(x, (int, float)) else None

    facts = {
        "atleta": atleta.get("nombre") or "Gael",
        "recovery_pct": last("recovery_pct"),
        "hrv_ms": round(hrv_today, 1) if hrv_today else None,
        "hrv_base_ms": round(hrv_base, 1) if hrv_base else None,
        "hrv_vs_base_pct": pct(hrv_dev),
        "hrv_tendencia_7d_pct": pct(hrv_trend),
        "fc_reposo_lpm": rhr_today,
        "fc_reposo_base_lpm": round(rhr_base, 1) if rhr_base else None,
        "fc_reposo_vs_base_pct": pct(rhr_dev),
        "fc_reposo_tendencia_7d_pct": pct(rhr_trend),
        "sueno_pct": last("sleep_perf_pct"),
        "spo2_pct": last("spo2_pct"),
        "skin_temp_c": last("skin_temp_c"),
        "resp_rate": last("resp_rate"),
        "sueno_detalle": {
            "horas_anoche": last("sleep_asleep_h") or last("sleep_hours"),
            "en_cama_h": last("sleep_hours"),
            "profundo_h": last("sleep_deep_h"), "rem_h": last("sleep_rem_h"), "ligero_h": last("sleep_light_h"),
            "profundo_pct": last("deep_pct"), "rem_pct": last("rem_pct"),
            "ciclos": last("ciclos"),
            "eficiencia_pct": last("sleep_efficiency_pct"),
            "consistencia_pct": last("sleep_consistency_pct"),
            "despertares": last("despertares"), "deuda_min": last("deuda_sueno_min"),
            "horas_prom_7d": (round(_mean(col("sleep_asleep_h")[-7:]), 1)
                              if col("sleep_asleep_h") else None),
            "perf_prom_7d": (round(_mean(col("sleep_perf_pct")[-7:]))
                             if col("sleep_perf_pct") else None),
        },
        "dias_recovery_baja_seguidos": dias_rec_baja,
        "strain_hoy": last("strain"),
        "acwr": round(acwr, 2) if acwr else None,
        "km_nado_semana": km_week,
        "km_nado_semana_previa": km_prev,
        "dias_de_datos": len(daily),
        "evento": evento.get("nombre"),
        "evento_sede": evento.get("sede"),
        "dias_al_evento": evento.get("dias_al_evento"),
        "dias_al_viaje": evento.get("dias_al_viaje"),
        "fase": evento.get("fase"),
        "km_plan_semana": plan_sem.get("km_plan"),
        "ses_plan_semana": plan_sem.get("ses_plan"),
        "fase_plan_semana": plan_sem.get("fase_plan"),
        "km_nado_real_registrado": km_real,
        "carga_referencia_km": carga_km,
        "carga_referencia_fuente": carga_fuente,
        "plan_nado_hoy": plan_dias.get("hoy"),
        "plan_nado_manana": plan_dias.get("manana"),
        "kcal_objetivo_hoy": nutri.get("kcal_objetivo"),
        "macros_hoy": ({"P": nutri.get("proteina_g"), "C": nutri.get("carbohidratos_g"),
                        "G": nutri.get("grasa_g")} if nutri else None),
        "kcal_por_comida": nutri.get("kcal_por_comida"),
        "vo2max": (ds.get("zonas_fc") or {}).get("vo2max"),
        "zonas_fc": ({"vt1": zonas.get("vt1"), "vt2": zonas.get("vt2"), "fatmax": zonas.get("fatmax"),
                      "fc_max": zonas.get("fc_max"), "fc_reposo": zonas.get("fc_reposo"),
                      "zonas": zonas.get("zonas")} if zonas else None),
        "sesiones_reales_hoy": ses_hoy or None,
        "horas_agua_hoy": ses_hoy.get("horas_agua"),
        "horas_seco_hoy": ses_hoy.get("horas_seco"),
    }
    facts["semaforo"], facts["razones"] = semaforo(facts)
    return facts


def semaforo(f):
    level, razones = "verde", []

    def esc(to, why):
        nonlocal level
        razones.append(why)
        order = {"verde": 0, "amarillo": 1, "rojo": 2}
        if order[to] > order[level]:
            level = to

    r = f["recovery_pct"]
    if isinstance(r, (int, float)):
        if r < 34:
            esc("rojo", f"Recovery muy baja ({r:.0f}%)")
        elif r < 67:
            esc("amarillo", f"Recovery media ({r:.0f}%)")
    d = f["hrv_vs_base_pct"]
    if isinstance(d, (int, float)):
        if d <= -20:
            esc("rojo", f"HRV {d:+.0f}% vs tu base")
        elif d <= -10:
            esc("amarillo", "HRV a la baja")
    rd = f["fc_reposo_vs_base_pct"]
    if isinstance(rd, (int, float)):
        if rd >= 12:
            esc("rojo", "FC en reposo elevada")
        elif rd >= 5:
            esc("amarillo", "FC en reposo algo alta")
    if isinstance(f["sueno_pct"], (int, float)) and f["sueno_pct"] < 70:
        esc("amarillo", f"Sueño bajo ({f['sueno_pct']:.0f}%)")
    if f["acwr"] and f["acwr"] > 1.3:
        esc("amarillo", f"Carga aguda alta (ACWR {f['acwr']:.2f})")
    if not razones:
        razones.append("Todas las señales en rango")
    return level, razones


# ---------- Agente PREVENTIVO: nivel de vigilancia + escalón (por reglas) ----------
def preventivo_flags(f):
    """vigilar -> descarga -> fisio, según señales tempranas acumuladas."""
    nivel, señales = "ok", []

    def esc(to, why):
        nonlocal nivel
        señales.append(why)
        order = {"ok": 0, "vigilar": 1, "descarga": 2, "fisio": 3}
        if order[to] > order[nivel]:
            nivel = to

    ht = f.get("hrv_tendencia_7d_pct")
    if isinstance(ht, (int, float)):
        if ht <= -15:
            esc("descarga", f"HRV promedio de la semana cayó {ht:+.0f}% vs la anterior")
        elif ht <= -8:
            esc("vigilar", f"HRV semanal a la baja ({ht:+.0f}%)")
    rt = f.get("fc_reposo_tendencia_7d_pct")
    if isinstance(rt, (int, float)):
        if rt >= 8:
            esc("descarga", f"FC en reposo subió {rt:+.0f}% en la semana")
        elif rt >= 4:
            esc("vigilar", f"FC en reposo con tendencia al alza ({rt:+.0f}%)")
    dr = f.get("dias_recovery_baja_seguidos") or 0
    if dr >= 3:
        esc("fisio", f"{dr} días seguidos con Recovery baja")
    elif dr == 2:
        esc("descarga", "2 días seguidos con Recovery baja")
    if f.get("acwr") and f["acwr"] > 1.5:
        esc("descarga", f"ACWR {f['acwr']:.2f} (spike de carga, riesgo de lesión)")
    elif f.get("acwr") and f["acwr"] > 1.3:
        esc("vigilar", f"ACWR {f['acwr']:.2f} (carga aguda alta)")
    if not señales:
        señales.append("Sin señales tempranas de fatiga/sobrecarga")
    accion = {
        "ok": "Seguir el plan; nada que ajustar por prevención.",
        "vigilar": "Mantener el plan pero observar de cerca 24–48 h; cuidar sueño e hidratación.",
        "descarga": "Meter una descarga: bajar volumen/intensidad esta semana. Priorizar recuperación.",
        "fisio": "Descarga + valoración con fisioterapeuta/entrenador. No forzar hasta revisar.",
    }[nivel]
    return {"nivel": nivel, "señales": señales, "accion": accion}


# ---------- Fallback por reglas (coach del día, sin IA) ----------
def rule_based_report(f):
    level = f["semaforo"]
    if level == "verde":
        veredicto = "Luz verde: el cuerpo está listo para entrenar fuerte."
        entreno = "Adelante con la sesión planeada. Puedes buscar calidad/intensidad."
    elif level == "amarillo":
        veredicto = "Precaución: modera hoy. Entrena, pero con cabeza."
        entreno = "Mantén la sesión pero baja volumen/intensidad ~10–20%. Técnica sobre esfuerzo máximo."
    else:
        veredicto = "Bandera roja: hoy toca recuperar, no forzar."
        entreno = "Sesión suave o de descarga (técnica, aeróbico ligero). Nada de series duras."
    km = f.get("carga_referencia_km") or 0
    pilares = {
        "Entrenamiento": entreno,
        "Sueño": ("Dormir es tu mayor palanca: apunta a 8–9 h."
                  if (not isinstance(f["sueno_pct"], (int, float)) or f["sueno_pct"] < 85)
                  else "Buen descanso — mantén el horario constante."),
        "Hidratación": ("Nadar deshidrata aunque no lo sientas: agua + electrolitos."
                        if km >= 6 else "Hidrátate de forma constante durante el día."),
        "Nutrición": ("Alto volumen: sube carbohidratos alrededor de los entrenos y proteína (1.6–2 g/kg)."
                      if km >= 6 else "Come balanceado; no te saltes la comida post-entreno."),
        "Recuperación": ("Movilidad, foam rolling y respiración lenta. Considera masaje/siesta."
                         if level == "rojo" else
                         "Suma 10–15 min de movilidad y respiración." if level == "amarillo"
                         else "Mantén tu rutina de movilidad; vas bien."),
    }
    alertas = []
    if isinstance(f["hrv_vs_base_pct"], (int, float)) and f["hrv_vs_base_pct"] <= -15:
        alertas.append("HRV cayó bastante vs tu base — señal temprana de fatiga. Vigila.")
    if isinstance(f["fc_reposo_vs_base_pct"], (int, float)) and f["fc_reposo_vs_base_pct"] >= 10:
        alertas.append("FC en reposo elevada — suele preceder a un resfriado o sobrecarga.")
    if f["acwr"] and f["acwr"] > 1.4:
        alertas.append(f"Carga aguda muy por encima de la crónica (ACWR {f['acwr']:.2f}) — riesgo; no subas más.")
    return {"veredicto": veredicto, "pilares": pilares, "alertas": alertas, "motor": "reglas (sin IA)"}


# ---------- Agentes IA (Claude) ----------
def have_api():
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def ai_client():
    try:
        import anthropic
    except ImportError:
        return None
    try:
        return anthropic.Anthropic()
    except Exception:
        return None


def ai_daily_report(client, f, sport):
    """Coach del día como SALIDA ESTRUCTURADA (Pydantic) para alimentar el dashboard."""
    from pydantic import BaseModel

    class CoachReport(BaseModel):
        veredicto: str
        entrenamiento: str
        sueno: str
        hidratacion: str
        nutricion: str
        recuperacion: str
        alertas: list[str]

    system = build_system(sport)
    prompt = (
        "Estos son los HECHOS de hoy (calculados por el motor determinista; única verdad):\n\n"
        f"{json.dumps(f, ensure_ascii=False, indent=2)}\n\n"
        f"El semáforo del día es {f['semaforo'].upper()} (razones: {', '.join(f['razones'])}); respétalo."
        f"{sport_focus_note(sport)}\n\n"
        "Devuelve el coach del día: un veredicto coherente con el semáforo, una frase por pilar "
        "(entrenamiento, sueño, hidratación, nutrición, recuperación) anclada en una señal de los HECHOS, "
        "y una lista de alertas preventivas (vacía si no hay riesgo)."
    )
    resp = client.messages.parse(
        model=MODEL,
        max_tokens=1500,
        system=system,
        messages=[{"role": "user", "content": prompt}],
        output_format=CoachReport,
    )
    r = resp.parsed_output
    return {
        "veredicto": r.veredicto,
        "pilares": {
            "Entrenamiento": r.entrenamiento, "Sueño": r.sueno, "Hidratación": r.hidratacion,
            "Nutrición": r.nutricion, "Recuperación": r.recuperacion,
        },
        "alertas": r.alertas,
        "motor": f"Claude API · {MODEL}",
    }


def ai_preventivo(client, f, flags, sport):
    system = build_system(sport)
    prompt = (
        "Actúas como el agente PREVENTIVO de TID-MAX (vigila fatiga/sobrecarga, no diagnostica).\n\n"
        "HECHOS y tendencias del motor (única verdad):\n"
        f"{json.dumps(f, ensure_ascii=False, indent=2)}\n\n"
        f"El motor fijó el nivel de vigilancia en '{flags['nivel'].upper()}' "
        f"(señales: {', '.join(flags['señales'])}; acción base: {flags['accion']}).{sport_focus_note(sport)}\n\n"
        "Explica en 3–5 frases, para el entrenador, qué está pasando y qué hacer los próximos días. "
        "Respeta el nivel del motor; sé concreto y prudente."
    )
    resp = client.messages.create(
        model=MODEL, max_tokens=800, thinking={"type": "adaptive"},
        system=system, messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()


def ai_answer(client, f, pregunta, sport):
    system = build_system(sport)
    prompt = (
        "HECHOS del atleta (calculados por el motor; única verdad, no inventes otros):\n\n"
        f"{json.dumps(f, ensure_ascii=False, indent=2)}\n\n"
        f"Pregunta del entrenador: {pregunta}\n\n"
        "Responde apoyándote SOLO en los hechos. Si el dato no está, dilo."
    )
    out = []
    with client.messages.stream(
        model=MODEL, max_tokens=1000, thinking={"type": "adaptive"},
        system=system, messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            sys.stdout.write(text)
            sys.stdout.flush()
            out.append(text)
    print()
    return "".join(out)


# ---------- Salida ----------
def print_facts(f):
    def s(v, suf=""):
        return f"{v}{suf}" if isinstance(v, (int, float)) else "—"
    icon = {"verde": "🟢", "amarillo": "🟡", "rojo": "🔴"}[f["semaforo"]]
    print("\n================ TID-MAX · AGENTE COACH ================")
    print(f"Atleta: {f['atleta']}   ({f['dias_de_datos']} días de datos)")
    if f.get("dias_al_evento") is not None:
        print(f"Evento: {f['evento']}  →  faltan {f['dias_al_evento']} días  "
              f"(fase: {f['fase']}; vuelo en {f['dias_al_viaje']} días)")
    if f.get("km_plan_semana") is not None:
        print(f"Plan semana: {f['fase_plan_semana']} · {f['km_plan_semana']} km / "
              f"{s(f.get('ses_plan_semana'))} ses (macrociclo del entrenador)")
    if f.get("carga_referencia_km") is not None:
        print(f"Carga de nado (semana): {f['carga_referencia_km']} km"
              + (f" · previa {f['km_nado_semana_previa']} km" if f.get("km_nado_semana_previa") is not None else "")
              + f"  —  {f['carga_referencia_fuente']}")

    def fmt_dia(d):
        if not d:
            return "—"
        ses = " + ".join(
            f"{s['hora'] or '—'} {s['km']}km" + (f" ({s['enfoque']})" if s.get("enfoque") else "")
            for s in d.get("sesiones", []))
        return f"{d['tipo']} · {d['km_dia']} km" + (f"  [{ses}]" if ses else "")
    if f.get("plan_nado_hoy"):
        print(f"Nado HOY ({f['plan_nado_hoy']['dia']}): {fmt_dia(f['plan_nado_hoy'])}")
    if f.get("plan_nado_manana"):
        print(f"Nado MAÑANA ({f['plan_nado_manana']['dia']}): {fmt_dia(f['plan_nado_manana'])}")
    sr = f.get("sesiones_reales_hoy")
    if sr:
        detalle = " · ".join(
            f"{s.get('inicio') or '—'}-{s.get('fin') or '—'} {s.get('tipo')}"
            for s in sr.get("sesiones", []))
        print(f"Sesiones reales HOY (WHOOP): {sr['n_sesiones']} · {sr['horas_total']} h "
              f"(agua {sr['horas_agua']} h · seco {sr['horas_seco']} h)"
              + (f"  [{detalle}]" if detalle else ""))
    if f.get("kcal_objetivo_hoy") and f.get("macros_hoy"):
        m = f["macros_hoy"]
        print(f"Nutrición HOY: ~{f['kcal_objetivo_hoy']} kcal · P {m['P']}g · C {m['C']}g · G {m['G']}g")
    sd = f.get("sueno_detalle") or {}
    if sd.get("horas_anoche") is not None:
        print(f"Sueño anoche: {sd['horas_anoche']} h dormido · {s(sd.get('sueno_pct') or f.get('sueno_pct'))}% perf · "
              f"prof {s(sd.get('profundo_pct'),'%')} · REM {s(sd.get('rem_pct'),'%')} · "
              f"efic {s(sd.get('eficiencia_pct'),'%')} · consist {s(sd.get('consistencia_pct'),'%')} · "
              f"{s(sd.get('despertares'))} despertares"
              + (f" · deuda {sd['deuda_min']} min" if isinstance(sd.get('deuda_min'), (int, float)) else ""))
        if sd.get("horas_prom_7d") is not None:
            print(f"           7d: {sd['horas_prom_7d']} h/noche · {s(sd.get('perf_prom_7d'),'%')} perf media")
    print(f"Semáforo: {icon} {f['semaforo'].upper()}  —  {', '.join(f['razones'])}")
    print(f"Recovery {s(f['recovery_pct'],'%')} | HRV {s(f['hrv_ms'],' ms')} ({s(f['hrv_vs_base_pct'],'%')} vs base) | "
          f"FC rep {s(f['fc_reposo_lpm'],' lpm')} | Sueño {s(f['sueno_pct'],'%')} | "
          f"Km sem {s(f['km_nado_semana'],' km')} | ACWR {s(f['acwr'])}")
    print("--------------------------------------------------------")


def print_report(rep):
    print(f"Veredicto: {rep['veredicto']}")
    print("\nPlan (5 pilares):")
    for k, v in rep["pilares"].items():
        print(f"  • {k}: {v}")
    for a in rep["alertas"]:
        print(f"  ⚠️ {a}")
    print(f"\n[modo: {rep['motor']}]")
    print("========================================================\n")


def write_coach_json(f, rep):
    """Salida estructurada que consume el dashboard."""
    os.makedirs(os.path.dirname(COACH_OUT), exist_ok=True)
    payload = {
        "generado_utc": datetime.now(timezone.utc).isoformat(),
        "atleta": f["atleta"],
        "semaforo": f["semaforo"],
        "razones": f["razones"],
        "veredicto": rep["veredicto"],
        "pilares": rep["pilares"],
        "alertas": rep["alertas"],
        "hechos": f,
        "motor": rep["motor"],
    }
    with open(COACH_OUT, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
    return COACH_OUT


def main():
    args = sys.argv[1:]
    force_rules = "--sin-ia" in args
    preventivo = "--preventivo" in args
    pregunta = None
    if "--pregunta" in args:
        i = args.index("--pregunta")
        pregunta = args[i + 1] if i + 1 < len(args) else None
    deporte = None
    if "--deporte" in args:
        i = args.index("--deporte")
        deporte = args[i + 1] if i + 1 < len(args) else None

    ds = load_dataset(DEFAULT_DATASET)
    f = build_facts(ds)
    # Módulo de deporte: --deporte gana; si no, el del perfil del atleta; si no, natación.
    sport = load_sport(deporte or (ds.get("atleta") or {}).get("deporte") or "natacion")
    print_facts(f)
    print(f"[módulo de deporte: {sport.get('nombre', '—')}]")

    client = None if force_rules else (ai_client() if have_api() else None)

    # Q&A libre
    if pregunta:
        if client:
            print(f"❓ {pregunta}\n")
            ai_answer(client, f, pregunta, sport)
            print("\n========================================================\n")
        else:
            print("El Q&A conversacional necesita la Claude API.")
            print("Configura:  pip install anthropic  &&  export ANTHROPIC_API_KEY=...\n")
        return

    # Agente Preventivo
    if preventivo:
        flags = preventivo_flags(f)
        icon = {"ok": "🟢", "vigilar": "🟡", "descarga": "🟠", "fisio": "🔴"}[flags["nivel"]]
        print(f"PREVENTIVO: {icon} {flags['nivel'].upper()}")
        for s in flags["señales"]:
            print(f"  • {s}")
        print(f"\nAcción: {flags['accion']}")
        if client:
            try:
                print("\n— Lectura del agente —")
                print(ai_preventivo(client, f, flags, sport))
                print(f"\n[modo: Claude API · {MODEL}]")
            except Exception as e:
                print(f"[aviso] falló Claude ({e}); me quedo con las reglas.]")
        print("========================================================\n")
        return

    # Coach del día (estructurado -> alimenta el dashboard)
    rep = None
    if client:
        try:
            rep = ai_daily_report(client, f, sport)
        except Exception as e:
            print(f"[aviso] falló la llamada a Claude ({e}); uso el motor por reglas.\n")
    if rep is None:
        if not force_rules and not have_api():
            print("[sin ANTHROPIC_API_KEY: coach por reglas. Para el modo IA: "
                  "pip install anthropic && export ANTHROPIC_API_KEY=...]\n")
        rep = rule_based_report(f)

    print_report(rep)
    out = write_coach_json(f, rep)
    print(f"Salida estructurada para el dashboard: {out}\n")


if __name__ == "__main__":
    main()
