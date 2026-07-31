#!/usr/bin/env python3
"""
tid_nutricion.py — Agente de Nutrición de TID-MAX (Capa 2, visión).

Gael (o Carlos) le toma una FOTO a la comida y el agente estima el platillo y sus macros
(calorías, proteína, carbohidratos, grasa) usando la visión de Claude. El resultado se apoya
en la plantilla real de Gael (nutricion-gael.json): dobles Lun/Mie/Vie, altísimo gasto, por lo
que el enfoque SIEMPRE es cubrir la demanda energética, nunca restringir (es menor de edad).

Regla de oro (igual que el resto de agentes): el modelo ESTIMA a partir de la imagen; los rangos
son aproximados y se marcan como tales. Sin ANTHROPIC_API_KEY (o sin SDK) cae con gracia a un
mensaje por reglas usando la plantilla base — el producto sigue.

Uso:
    python tid_nutricion.py foto_comida.jpg
    python tid_nutricion.py foto_comida.jpg --tipo doble    # contexto: día de doble sesión
    python tid_nutricion.py --plan                          # plan de comidas del día (kcal + sus alimentos)
    python tid_nutricion.py --plantilla                     # imprime la plantilla base de Gael

Requiere (modo IA):
    pip install anthropic
    export ANTHROPIC_API_KEY=...
"""
import os
import sys
import json
import base64

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_NUTRI = os.path.join(SCRIPT_DIR, "nutricion-gael.json")
MODEL = "claude-opus-5"

PERSONA = (
    "Eres el agente de nutrición de TID-MAX para Gael, nadador competitivo de alto nivel y menor "
    "de edad, que entrena en dobles sesiones (Lun/Mie/Vie) con un gasto energético altísimo. "
    "Tu trabajo es ESTIMAR, a partir de una foto, qué comió y sus macros aproximados, y decir si "
    "cubre bien la demanda del entrenamiento. Hablas en español, claro y cercano."
)

GUARDRAILS = (
    "REGLAS ESTRICTAS:\n"
    "1) Es MENOR de edad con gasto muy alto: NUNCA sugieras restringir calorías, saltarte comidas "
    "ni bajar de peso. El objetivo es cubrir energía, proteína y recuperación.\n"
    "2) Las cantidades de una foto son ESTIMADAS: da rangos y acláralo, no cifras falsamente exactas.\n"
    "3) Nutrición deportiva y bienestar, NO medicina. No diagnostiques ni prescribas. Ante dudas de "
    "dosis o seguridad de suplementos, deriva a un nutriólogo o médico del deporte.\n"
    "4) Sé concreto y breve; ancla el consejo en lo que se ve en el plato y en la fase del día."
)

MEDIA = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
         ".webp": "image/webp", ".gif": "image/gif"}


def load_base():
    if os.path.exists(BASE_NUTRI):
        with open(BASE_NUTRI, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def encode_image(path):
    ext = os.path.splitext(path)[1].lower()
    media = MEDIA.get(ext)
    if not media:
        sys.exit(f"Formato no soportado: {ext}. Usa {', '.join(MEDIA)}.")
    with open(path, "rb") as fh:
        data = base64.standard_b64encode(fh.read()).decode("utf-8")
    return media, data


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


def ai_estimate(client, img_path, tipo_dia, base):
    from pydantic import BaseModel

    class Macros(BaseModel):
        kcal_aprox: str
        proteina_g_aprox: str
        carbohidratos_g_aprox: str
        grasa_g_aprox: str

    class Estimacion(BaseModel):
        platillo: str
        alimentos: list[str]
        macros: Macros
        cubre_demanda: str      # sí / parcial / no + por qué
        sugerencia: str         # qué agregar/ajustar (sin restringir)
        confianza: str          # alta / media / baja

    media, data = encode_image(img_path)
    contexto = (
        f"Contexto: es un día de tipo '{tipo_dia}'. "
        "Plantilla base de Gael (referencia de lo que suele comer y sus suplementos):\n"
        f"{json.dumps(base, ensure_ascii=False)}"
    )
    resp = client.messages.parse(
        model=MODEL,
        max_tokens=1200,
        system=f"{PERSONA}\n\n{GUARDRAILS}",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": data}},
                {"type": "text", "text": contexto + "\n\nEstima el platillo, los alimentos, los "
                 "macros aproximados (en rangos), si cubre la demanda del entrenamiento y qué "
                 "sugerirías agregar. Marca tu nivel de confianza."},
            ],
        }],
        output_format=Estimacion,
    )
    return resp.parsed_output


def cargar_nutricion_hoy():
    path = os.path.join(SCRIPT_DIR, "datos", "procesado", "dataset.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        ds = json.load(f)
    return ds.get("nutricion_hoy"), ds.get("plan_dias", {}).get("hoy")


def ai_plan_comidas(client, nutri, plan_hoy, base):
    from pydantic import BaseModel

    class Comida(BaseModel):
        nombre: str          # Desayuno / Comida / Cena
        kcal_aprox: str
        sugerencia: str      # platillo armado con SUS alimentos
        porciones: str       # cantidades caseras aproximadas

    class PlanDia(BaseModel):
        resumen: str
        desayuno: Comida
        comida: Comida
        cena: Comida
        snack_entreno: str

    kpc = nutri.get("kcal_por_comida", {})
    prompt = (
        "Arma el PLAN DE COMIDAS de HOY para Gael usando SOLO (o casi solo) sus alimentos "
        "preferidos. Objetivo del día:\n"
        f"- {nutri['kcal_objetivo']} kcal · Proteína {nutri['proteina_g']} g · "
        f"Carbohidratos {nutri['carbohidratos_g']} g · Grasa {nutri['grasa_g']} g\n"
        f"- Nado de hoy: {plan_hoy.get('km_dia') if plan_hoy else '—'} km\n"
        f"- Reparto sugerido por comida (kcal): {json.dumps(kpc, ensure_ascii=False)}\n\n"
        f"Sus alimentos preferidos:\n{json.dumps(base.get('alimentos_preferidos', {}), ensure_ascii=False)}\n\n"
        "Para cada comida da un platillo concreto con porciones caseras aproximadas que sumen "
        "cerca de sus kcal objetivo. Es adolescente en crecimiento: cubrir energía, sin restringir."
    )
    resp = client.messages.parse(
        model=MODEL, max_tokens=1400, system=f"{PERSONA}\n\n{GUARDRAILS}",
        messages=[{"role": "user", "content": prompt}], output_format=PlanDia,
    )
    return resp.parsed_output


def print_plan(nutri, plan_hoy, plan):
    print("\n============== TID-MAX · PLAN DE COMIDAS DEL DÍA ==============")
    print(f"Objetivo: ~{nutri['kcal_objetivo']} kcal · P {nutri['proteina_g']}g · "
          f"C {nutri['carbohidratos_g']}g · G {nutri['grasa_g']}g  (nado {nutri.get('km_dia')} km)")
    if plan:
        print(f"\n{plan.resumen}\n")
        for c in (plan.desayuno, plan.comida, plan.cena):
            print(f"● {c.nombre} (~{c.kcal_aprox} kcal)")
            print(f"   {c.sugerencia}")
            print(f"   Porciones: {c.porciones}")
        print(f"\n🍌 Snack alrededor del entreno: {plan.snack_entreno}")
    print("\n(Estimaciones para orientar; ajústalas con un nutriólogo del deporte.)")


def print_estimacion(e):
    print("\n============== TID-MAX · AGENTE DE NUTRICIÓN ==============")
    print(f"Platillo: {e.platillo}   (confianza: {e.confianza})")
    print("Alimentos:")
    for a in e.alimentos:
        print(f"  • {a}")
    m = e.macros
    print(f"\nMacros aprox: {m.kcal_aprox} kcal | Proteína {m.proteina_g_aprox} | "
          f"Carbos {m.carbohidratos_g_aprox} | Grasa {m.grasa_g_aprox}")
    print(f"\n¿Cubre la demanda?: {e.cubre_demanda}")
    print(f"Sugerencia: {e.sugerencia}")
    print("\n(Estimación por visión: cantidades aproximadas. No sustituye a un nutriólogo.)")


def fallback(base, tipo_dia):
    print("\n============== TID-MAX · AGENTE DE NUTRICIÓN (modo base) ==============")
    print("Sin ANTHROPIC_API_KEY / SDK: no puedo analizar la foto, muestro la plantilla de referencia.")
    dt = base.get("dia_tipo_doble", {})
    print(f"\nDía tipo '{tipo_dia}'. Comidas de referencia de Gael:")
    for k, v in dt.items():
        if isinstance(v, dict) and v.get("ingredientes"):
            print(f"  • {v.get('descripcion', k)}: {', '.join(v['ingredientes'])}")
    print("\nPara estimar macros desde una foto:  export ANTHROPIC_API_KEY=...  y vuelve a correr.")


def main():
    args = [a for a in sys.argv[1:]]
    tipo_dia = "doble"
    if "--tipo" in args:
        i = args.index("--tipo")
        if i + 1 < len(args):
            tipo_dia = args[i + 1]
            del args[i:i + 2]

    base = load_base()

    if "--plantilla" in args:
        print(json.dumps(base, ensure_ascii=False, indent=2))
        return

    if "--plan" in args:
        datos = cargar_nutricion_hoy()
        if not datos or not datos[0]:
            sys.exit("No hay nutricion_hoy en el dataset. Corre primero:  python tid_data.py")
        nutri, plan_hoy = datos
        client = ai_client() if have_api() else None
        plan = None
        if client:
            try:
                plan = ai_plan_comidas(client, nutri, plan_hoy, base)
            except Exception as e:
                print(f"(Aviso: falló la IA: {e}. Muestro solo los objetivos.)")
        print_plan(nutri, plan_hoy, plan)
        return

    fotos = [a for a in args if not a.startswith("--")]
    if not fotos:
        sys.exit("Uso: python tid_nutricion.py <foto.jpg> [--tipo doble|sencilla] | --plantilla")
    img_path = fotos[0]
    if not os.path.exists(img_path):
        sys.exit(f"No encuentro la foto: {img_path}")

    client = ai_client() if have_api() else None
    if client:
        try:
            print_estimacion(ai_estimate(client, img_path, tipo_dia, base))
            return
        except Exception as e:
            print(f"(Aviso: falló la llamada IA: {e}. Caigo a modo base.)")
    fallback(base, tipo_dia)


if __name__ == "__main__":
    main()
