#!/usr/bin/env python3
"""
tid_agent.py — Agente coach de TID-MAX (Capa 2) sobre la Claude API.

Lee el esquema canónico (datos/procesado/dataset.json que produce tid_data.py), el MOTOR
determinista calcula los hechos duros (recovery vs base, HRV/FC vs base, ACWR, volumen de nado,
semáforo), y el AGENTE (Claude) los convierte en un coach conversacional en lenguaje natural.

Regla de oro: el LLM NO inventa números. El código calcula; el modelo interpreta y explica.
Sin ANTHROPIC_API_KEY (o sin el SDK), cae con gracia al texto por reglas — el producto sigue.

Uso:
    python whoop_sync.py          # baja WHOOP
    python tid_data.py            # normaliza -> dataset.json
    python tid_agent.py                          # coach del día (Claude o fallback)
    python tid_agent.py --pregunta "¿por qué bajó mi HRV esta semana?"   # Q&A libre
    python tid_agent.py --sin-ia                 # fuerza el modo por reglas (sin llamar a Claude)

Requiere (para el modo IA):
    pip install anthropic
    export ANTHROPIC_API_KEY=...   # o  ant auth login
"""
import os
import sys
import json
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATASET = os.path.join(SCRIPT_DIR, "datos", "procesado", "dataset.json")

MODEL = "claude-opus-5"  # el más capaz de uso general; claude-haiku-4-5 para abaratar a escala

PERSONA = (
    "Eres el coach de TID-MAX, un asistente de rendimiento y bienestar para Gael, un nadador "
    "competitivo de alto nivel (menor de edad) que se prepara para un evento en Vancouver. "
    "Hablas en español, claro y cercano, dirigiéndote a Gael y a su entrenador."
)

GUARDRAILS = (
    "REGLAS ESTRICTAS:\n"
    "1) Orientación de RENDIMIENTO y BIENESTAR, NO medicina. Nunca diagnostiques, nombres "
    "enfermedades ni sugieras fármacos. Ante una señal de alarma real, recomienda consultar a un "
    "profesional de la salud.\n"
    "2) NO inventes datos. Habla SOLO de los números que te doy en los HECHOS. Si algo falta, dilo.\n"
    "3) Es menor de edad: nada de restricción calórica agresiva ni sobrecarga; tono responsable.\n"
    "4) El semáforo (verde/amarillo/rojo) YA lo decidió el motor; respétalo, no lo cambies.\n"
    "5) Sé concreto y breve. Cada consejo se apoya en una señal concreta de los HECHOS."
)


# ---------- Carga del esquema canónico ----------
def load_dataset(path):
    if not os.path.exists(path):
        # tolerancia: intenta encontrarlo aunque cambie la carpeta
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

    def col(key):
        return [(r["fecha"], r.get(key)) for r in daily if isinstance(r.get(key), (int, float))]

    def last(key):
        c = col(key)
        return c[-1][1] if c else None

    hrv_vals = [v for _, v in col("hrv_ms")]
    rhr_vals = [v for _, v in col("rhr_bpm")]
    hrv_base = _mean(hrv_vals[-30:]) if hrv_vals else None
    rhr_base = _mean(rhr_vals[-30:]) if rhr_vals else None
    hrv_today, rhr_today = last("hrv_ms"), last("rhr_bpm")
    hrv_dev = (hrv_today - hrv_base) / hrv_base if (hrv_today and hrv_base) else None
    rhr_dev = (rhr_today - rhr_base) / rhr_base if (rhr_today and rhr_base) else None

    # Carga: ACWR (agudo 7d : crónico 28d) sobre el strain diario
    s_vals = [v for _, v in col("strain")]
    acute, chronic = _mean(s_vals[-7:]), _mean(s_vals[-28:])
    acwr = acute / chronic if (acute and chronic) else None

    # Volumen de nado real (registro manual)
    swim = [(r["fecha"], r.get("swim_km")) for r in daily if isinstance(r.get("swim_km"), (int, float))]
    km_week = round(sum(v for _, v in swim[-7:]), 1) if swim else None
    km_prev = round(sum(v for _, v in swim[-14:-7]), 1) if len(swim) > 7 else None

    facts = {
        "atleta": atleta.get("nombre") or "Gael",
        "recovery_pct": last("recovery_pct"),
        "hrv_ms": round(hrv_today, 1) if hrv_today else None,
        "hrv_base_ms": round(hrv_base, 1) if hrv_base else None,
        "hrv_vs_base_pct": round(hrv_dev * 100) if hrv_dev is not None else None,
        "fc_reposo_lpm": rhr_today,
        "fc_reposo_base_lpm": round(rhr_base, 1) if rhr_base else None,
        "fc_reposo_vs_base_pct": round(rhr_dev * 100) if rhr_dev is not None else None,
        "sueno_pct": last("sleep_perf_pct"),
        "strain_hoy": last("strain"),
        "acwr": round(acwr, 2) if acwr else None,
        "km_nado_semana": km_week,
        "km_nado_semana_previa": km_prev,
        "dias_de_datos": len(daily),
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


# ---------- Fallback por reglas (sin IA) ----------
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
    km = f["km_nado_semana"] or 0
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


# ---------- Agente IA (Claude) ----------
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


def ai_daily_report(client, f):
    """Coach del día en lenguaje natural. El semáforo ya está fijado por el motor."""
    system = f"{PERSONA}\n\n{GUARDRAILS}"
    prompt = (
        "Estos son los HECHOS de hoy (calculados por el motor determinista; son la única verdad):\n\n"
        f"{json.dumps(f, ensure_ascii=False, indent=2)}\n\n"
        f"El semáforo del día es: {f['semaforo'].upper()} (razones: {', '.join(f['razones'])}).\n\n"
        "Escribe el coach del día para Gael con esta estructura:\n"
        "1) Un veredicto de 1–2 frases coherente con el semáforo.\n"
        "2) Plan de 5 pilares (Entrenamiento, Sueño, Hidratación, Nutrición, Recuperación), 1 frase cada uno, "
        "cada consejo anclado en una señal concreta de los HECHOS.\n"
        "3) Si hay riesgo (HRV baja, FC reposo alta, ACWR>1.4), una sección corta de Alertas preventivas.\n"
        "Tono humano y motivador, sin tecnicismos innecesarios."
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()


def ai_answer(client, f, pregunta):
    """Q&A libre del entrenador sobre los hechos del atleta (streaming)."""
    system = f"{PERSONA}\n\n{GUARDRAILS}"
    prompt = (
        "HECHOS del atleta (calculados por el motor; única verdad, no inventes otros):\n\n"
        f"{json.dumps(f, ensure_ascii=False, indent=2)}\n\n"
        f"Pregunta del entrenador: {pregunta}\n\n"
        "Responde apoyándote SOLO en los hechos. Si el dato no está, dilo."
    )
    out = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=1000,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            sys.stdout.write(text)
            sys.stdout.flush()
            out.append(text)
    print()
    return "".join(out)


# ---------- Presentación ----------
def print_facts(f):
    def s(v, suf=""):
        return f"{v}{suf}" if isinstance(v, (int, float)) else "—"
    icon = {"verde": "🟢", "amarillo": "🟡", "rojo": "🔴"}[f["semaforo"]]
    print("\n================ TID-MAX · AGENTE COACH ================")
    print(f"Atleta: {f['atleta']}   ({f['dias_de_datos']} días de datos)")
    print(f"Semáforo: {icon} {f['semaforo'].upper()}  —  {', '.join(f['razones'])}")
    print(f"Recovery {s(f['recovery_pct'],'%')} | HRV {s(f['hrv_ms'],' ms')} ({s(f['hrv_vs_base_pct'],'%')} vs base) | "
          f"FC rep {s(f['fc_reposo_lpm'],' lpm')} | Sueño {s(f['sueno_pct'],'%')} | "
          f"Km sem {s(f['km_nado_semana'],' km')} | ACWR {s(f['acwr'])}")
    print("--------------------------------------------------------")


def print_rule_report(rep):
    print(f"Veredicto: {rep['veredicto']}")
    print("\nPlan (5 pilares):")
    for k, v in rep["pilares"].items():
        print(f"  • {k}: {v}")
    for a in rep["alertas"]:
        print(f"  ⚠️ {a}")
    print(f"\n[modo: {rep['motor']}]")
    print("========================================================\n")


def main():
    args = sys.argv[1:]
    force_rules = "--sin-ia" in args
    pregunta = None
    if "--pregunta" in args:
        i = args.index("--pregunta")
        pregunta = args[i + 1] if i + 1 < len(args) else None

    ds = load_dataset(DEFAULT_DATASET)
    f = build_facts(ds)
    print_facts(f)

    client = None if force_rules else (ai_client() if have_api() else None)

    # Modo Q&A libre
    if pregunta:
        if client:
            print(f"❓ {pregunta}\n")
            ai_answer(client, f, pregunta)
            print("\n========================================================\n")
        else:
            print("El Q&A conversacional necesita la Claude API.")
            print("Configura:  pip install anthropic  &&  export ANTHROPIC_API_KEY=...\n")
        return

    # Modo reporte del día
    if client:
        try:
            print(ai_daily_report(client, f))
            print(f"\n[modo: Claude API · {MODEL}]")
            print("========================================================\n")
            return
        except Exception as e:
            print(f"[aviso] falló la llamada a Claude ({e}); uso el motor por reglas.\n")

    if not force_rules and not have_api():
        print("[sin ANTHROPIC_API_KEY: uso el coach por reglas. Para el modo conversacional: "
              "pip install anthropic && export ANTHROPIC_API_KEY=...]\n")
    print_rule_report(rule_based_report(f))


if __name__ == "__main__":
    main()
