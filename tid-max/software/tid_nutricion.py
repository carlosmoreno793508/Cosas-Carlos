#!/usr/bin/env python3
"""
tid_nutricion.py — Agente de Nutrición de TID-MAX (Capa 2, visión).

Gael (o Carlos) le toma una FOTO a la comida y el agente estima el platillo y sus macros
(calorías, proteína, carbohidratos, grasa) usando la visión de Claude. El resultado se apoya
en la plantilla real de Gael (nutricion-gael.json): dobles Lun/Mie/Vie, altísimo gasto, por lo
que el enfoque SIEMPRE es cubrir la demanda energética, nunca restringir (atleta joven de 19).

Regla de oro (igual que el resto de agentes): el modelo ESTIMA a partir de la imagen; los rangos
son aproximados y se marcan como tales. Sin ANTHROPIC_API_KEY (o sin SDK) cae con gracia a un
mensaje por reglas usando la plantilla base — el producto sigue.

Uso:
    python tid_nutricion.py foto_comida.jpg                 # analiza foto Y la registra como consumo de hoy
    python tid_nutricion.py foto_comida.jpg --tipo doble    # contexto: día de doble sesión
    python tid_nutricion.py --texto "6 huevos, licuado, 50 g totopos"   # registra por texto (sin foto)
    python tid_nutricion.py IMG.jpeg --avisar               # registra Y avisa a la familia (link actualizado)
    python tid_nutricion.py --consumo                       # muestra el consumo acumulado de hoy vs meta
    python tid_nutricion.py --reset-consumo                 # borra el consumo de hoy (empezar de cero)
    python tid_nutricion.py --plan                          # plan de comidas del día (kcal + sus alimentos)
    python tid_nutricion.py --plantilla                     # imprime la plantilla base de Gael
    python tid_nutricion.py --memoria                       # muestra lo que el agente ha APRENDIDO

Cada foto/--texto SUMA una comida al consumo del día (datos/procesado/consumo-hoy.json);
la tarjeta del cliente muestra "consumido vs meta" cuando hay algo registrado hoy.

MEMORIA (aprendizaje): cada comida también se guarda en datos/procesado/historial-alimentos.json.
Con eso el agente aprende los platillos recurrentes de Gael y sus macros típicos, y cuando subes
una FOTO SIN escribir los detalles, reconoce "el desayuno de siempre" y autocompleta las porciones
(bajando la confianza a 'media'). No reentrena el modelo: es memoria + reconocimiento.

Requiere (modo IA):
    pip install anthropic
    export ANTHROPIC_API_KEY=...
"""
import os
import sys
import json
import base64
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_NUTRI = os.path.join(SCRIPT_DIR, "nutricion-gael.json")
# Registro del consumo del día (lo que Carlos manda: foto/texto). La tarjeta lo lee.
CONSUMO_JSON = os.path.join(SCRIPT_DIR, "datos", "procesado", "consumo-hoy.json")
# MEMORIA de alimentos: bitácora acumulada de TODAS las comidas estimadas (todos los días).
# De aquí el agente "aprende" los platillos recurrentes de Gael y sus macros típicos, para
# autocompletar cuando el usuario sube una foto SIN escribir los detalles.
HISTORIAL_JSON = os.path.join(SCRIPT_DIR, "datos", "procesado", "historial-alimentos.json")
HISTORIAL_MAX = 800          # tope de entradas guardadas (memoria acotada)
MEMORIA_TOP = 8              # cuántos platillos frecuentes se le pasan como contexto
MODEL = "claude-opus-5"

PERSONA = (
    "Eres el agente de nutrición de TID-MAX para Gael, nadador competitivo de alto nivel de 19 "
    "años, que entrena en dobles sesiones (Lun/Mie/Vie) con un gasto energético altísimo. "
    "Tu trabajo es ESTIMAR, a partir de una foto, qué comió y sus macros aproximados, y decir si "
    "cubre bien la demanda del entrenamiento. Hablas en español, claro y cercano."
)

GUARDRAILS = (
    "REGLAS ESTRICTAS:\n"
    "1) Atleta joven de 19 con gasto muy alto: NUNCA sugieras restringir calorías, saltarte comidas "
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


def _modelo_estimacion():
    """Esquema Pydantic. Los macros llevan un RANGO (…_aprox, para leer) y un NÚMERO
    puntual (…_num, para poder sumar el consumo del día)."""
    from pydantic import BaseModel

    class Macros(BaseModel):
        kcal_aprox: str
        kcal_num: int
        proteina_g_aprox: str
        proteina_g_num: int
        carbohidratos_g_aprox: str
        carbohidratos_g_num: int
        grasa_g_aprox: str
        grasa_g_num: int

    class Estimacion(BaseModel):
        platillo: str
        alimentos: list[str]
        macros: Macros
        cubre_demanda: str      # sí / parcial / no + por qué
        sugerencia: str         # qué agregar/ajustar (sin restringir)
        confianza: str          # alta / media / baja

    return Estimacion


_INSTR = ("Estima el platillo, los alimentos y los macros: da un RANGO (…_aprox) y ADEMÁS un "
          "NÚMERO puntual entero (…_num, tu mejor estimación) para poder sumar el día. Di si "
          "cubre la demanda del entrenamiento y qué sugerirías agregar. Marca tu confianza. "
          "Sé BREVE: 'cubre_demanda' y 'sugerencia' en 1–2 frases cada uno.\n"
          "IMPORTANTE — usa la MEMORIA: si la foto/descripción viene SIN detalles (no dice "
          "porciones ni todos los ingredientes), y coincide con un platillo recurrente de la "
          "memoria de Gael, AUTOCOMPLETA con lo que sueles ver en ese platillo (alimentos y "
          "porciones típicas), pero baja la 'confianza' a 'media' y acláralo en la sugerencia. "
          "Si no se parece a nada de la memoria, estima normal. NO inventes precisión que no tienes.")


def _memoria_txt():
    mem = construir_memoria()
    if not mem:
        return ""
    return ("\n\nMEMORIA — platillos que Gael ya ha comido antes (aprendidos de fotos previas; "
            "úsalos para reconocer y autocompletar cuando falten detalles):\n"
            f"{json.dumps(mem, ensure_ascii=False)}")


def _contexto(tipo_dia, base):
    return (f"Contexto: es un día de tipo '{tipo_dia}'. "
            "Plantilla base de Gael (lo que suele comer y sus suplementos):\n"
            f"{json.dumps(base, ensure_ascii=False)}"
            + _memoria_txt())


def ai_estimate(client, img_path, tipo_dia, base):
    Estimacion = _modelo_estimacion()
    media, data = encode_image(img_path)
    resp = client.messages.parse(
        model=MODEL, max_tokens=2500, system=f"{PERSONA}\n\n{GUARDRAILS}",
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": data}},
            {"type": "text", "text": _contexto(tipo_dia, base) + "\n\n" + _INSTR},
        ]}],
        output_format=Estimacion,
    )
    return resp.parsed_output


def ai_estimate_texto(client, descripcion, tipo_dia, base):
    """Estima macros a partir de una DESCRIPCIÓN de texto (lo que Carlos escribe)."""
    Estimacion = _modelo_estimacion()
    resp = client.messages.parse(
        model=MODEL, max_tokens=2500, system=f"{PERSONA}\n\n{GUARDRAILS}",
        messages=[{"role": "user", "content":
                   _contexto(tipo_dia, base) + "\n\nGael comió (descrito por Carlos): "
                   f"\"{descripcion}\".\n\n" + _INSTR}],
        output_format=Estimacion,
    )
    return resp.parsed_output


def _hoy():
    return datetime.date.today().isoformat()


# ------------------------- MEMORIA / APRENDIZAJE -------------------------
# El agente no "reentrena": APRENDE guardando cada comida en una bitácora y construyendo,
# a partir de ella, los platillos recurrentes de Gael con sus macros típicos. Eso se le pasa
# como contexto para que autocomplete cuando la foto/el texto vengan sin detalles.

def _norm(txt):
    return " ".join((txt or "").lower().strip().split())


def guardar_historial(est, origen="foto"):
    """Agrega la estimación a la bitácora acumulada (memoria de alimentos)."""
    os.makedirs(os.path.dirname(HISTORIAL_JSON), exist_ok=True)
    hist = []
    if os.path.exists(HISTORIAL_JSON):
        try:
            with open(HISTORIAL_JSON, encoding="utf-8") as fh:
                hist = json.load(fh)
        except Exception:
            hist = []
    m = est.macros
    hist.append({
        "fecha": _hoy(),
        "hora": datetime.datetime.now().strftime("%H:%M"),
        "platillo": est.platillo,
        "alimentos": list(est.alimentos or []),
        "kcal": int(m.kcal_num), "prot_g": int(m.proteina_g_num),
        "carb_g": int(m.carbohidratos_g_num), "grasa_g": int(m.grasa_g_num),
        "confianza": getattr(est, "confianza", ""),
        "origen": origen,
    })
    hist = hist[-HISTORIAL_MAX:]          # memoria acotada
    with open(HISTORIAL_JSON, "w", encoding="utf-8") as fh:
        json.dump(hist, fh, ensure_ascii=False, indent=2)
    return hist


def construir_memoria(top=MEMORIA_TOP):
    """Resume la bitácora en los platillos recurrentes de Gael con sus macros típicos.
    Devuelve una lista compacta (la 'memoria' que se le da al modelo como contexto)."""
    if not os.path.exists(HISTORIAL_JSON):
        return []
    try:
        with open(HISTORIAL_JSON, encoding="utf-8") as fh:
            hist = json.load(fh)
    except Exception:
        return []
    grupos = {}
    for e in hist:
        k = _norm(e.get("platillo"))
        if not k:
            continue
        g = grupos.setdefault(k, {"platillo": e.get("platillo"), "veces": 0,
                                  "kcal": [], "prot_g": [], "carb_g": [], "grasa_g": [],
                                  "alimentos": {}, "ultima_vez": e.get("fecha", "")})
        g["veces"] += 1
        for kk in ("kcal", "prot_g", "carb_g", "grasa_g"):
            if e.get(kk):
                g[kk].append(e[kk])
        for a in e.get("alimentos", []):
            g["alimentos"][_norm(a)] = g["alimentos"].get(_norm(a), 0) + 1
        if e.get("fecha", "") >= g["ultima_vez"]:
            g["ultima_vez"] = e.get("fecha", "")

    def _med(xs):
        return int(sum(xs) / len(xs)) if xs else 0

    memoria = []
    for g in grupos.values():
        alimentos = sorted(g["alimentos"], key=g["alimentos"].get, reverse=True)[:6]
        memoria.append({
            "platillo": g["platillo"], "veces": g["veces"],
            "kcal_tipico": _med(g["kcal"]), "prot_g": _med(g["prot_g"]),
            "carb_g": _med(g["carb_g"]), "grasa_g": _med(g["grasa_g"]),
            "alimentos_frecuentes": alimentos, "ultima_vez": g["ultima_vez"],
        })
    # los más frecuentes primero (los que más vale la pena reconocer)
    memoria.sort(key=lambda x: x["veces"], reverse=True)
    return memoria[:top]


def _meta_hoy():
    """Meta nutricional de hoy (del dataset): kcal y macros objetivo."""
    datos = cargar_nutricion_hoy()
    if not datos or not datos[0]:
        return {}
    n = datos[0]
    return {"kcal": n.get("kcal_objetivo"), "prot_g": n.get("proteina_g"),
            "carb_g": n.get("carbohidratos_g"), "grasa_g": n.get("grasa_g")}


def registrar_consumo(est, origen="foto"):
    """Suma una comida al consumo de HOY (se reinicia solo al cambiar de día)."""
    os.makedirs(os.path.dirname(CONSUMO_JSON), exist_ok=True)
    hoy = _hoy()
    data = {}
    if os.path.exists(CONSUMO_JSON):
        try:
            with open(CONSUMO_JSON, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            data = {}
    if data.get("fecha") != hoy:
        data = {"fecha": hoy, "comidas": []}
    m = est.macros
    data["comidas"].append({
        "hora": datetime.datetime.now().strftime("%H:%M"),
        "platillo": est.platillo,
        "kcal": int(m.kcal_num), "prot_g": int(m.proteina_g_num),
        "carb_g": int(m.carbohidratos_g_num), "grasa_g": int(m.grasa_g_num),
        "origen": origen,
    })
    tot = {"kcal": 0, "prot_g": 0, "carb_g": 0, "grasa_g": 0}
    for c in data["comidas"]:
        for k in tot:
            tot[k] += c.get(k, 0)
    data["totales"] = tot
    data["meta"] = _meta_hoy()
    with open(CONSUMO_JSON, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    # Aprende: guarda esta comida en la memoria acumulada de alimentos.
    guardar_historial(est, origen)
    return data


def avisar_familia():
    """Refresca la tarjeta (con el consumo nuevo) y manda el mensaje corto con el link.
    Se usa con --avisar tras registrar una comida, para no esperar a las horas fijas."""
    import subprocess
    py = sys.executable or "python3"
    print("\n----- Avisar: refresco tarjeta + mensaje con link -----")
    subprocess.run([py, os.path.join(SCRIPT_DIR, "tid_cliente.py"), "--solo-html"],
                   capture_output=True, text=True, timeout=120)
    r = subprocess.run([py, os.path.join(SCRIPT_DIR, "tid_notify.py")],
                       capture_output=True, text=True, timeout=120)
    print((r.stdout or r.stderr or "").strip())


def print_consumo(data):
    t = data.get("totales", {})
    meta = data.get("meta", {})
    mk = meta.get("kcal") or 0
    print("\n----- Consumo de hoy (acumulado, con la info que mandaste) -----")
    for c in data.get("comidas", []):
        print(f"  • {c['hora']} {c['platillo']}: {c['kcal']} kcal "
              f"(C {c['carb_g']} / P {c['prot_g']} / G {c['grasa_g']})")
    linea = f"TOTAL: {t.get('kcal', 0)} kcal"
    if mk:
        linea += f" de {mk} meta ({round(100 * t.get('kcal', 0) / mk)}%)"
    linea += (f" · C {t.get('carb_g', 0)} · P {t.get('prot_g', 0)} · G {t.get('grasa_g', 0)}")
    print(linea)
    if mk:
        falta = max(mk - t.get('kcal', 0), 0)
        fc = max((meta.get('carb_g') or 0) - t.get('carb_g', 0), 0)
        print(f"Faltan ~{falta} kcal y ~{fc} g de carbohidrato para la meta.")


def cargar_nutricion_hoy():
    path = os.path.join(SCRIPT_DIR, "datos", "procesado", "dataset.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        ds = json.load(f)
    return ds.get("nutricion_hoy"), ds.get("plan_dias", {}).get("hoy")


def ai_plan_comidas(client, nutri, plan_hoy, base):
    kpc = nutri.get("kcal_por_comida", {})
    prompt = (
        "Arma el PLAN DE COMIDAS de HOY para Gael usando SOLO (o casi solo) sus alimentos "
        "preferidos. Objetivo del día:\n"
        f"- {nutri['kcal_objetivo']} kcal · Proteína {nutri['proteina_g']} g · "
        f"Carbohidratos {nutri['carbohidratos_g']} g · Grasa {nutri['grasa_g']} g\n"
        f"- Nado de hoy: {plan_hoy.get('km_dia') if plan_hoy else '—'} km\n"
        f"- Reparto por comida (kcal): {json.dumps(kpc, ensure_ascii=False)}\n\n"
        f"Sus alimentos preferidos:\n{json.dumps(base.get('alimentos_preferidos', {}), ensure_ascii=False)}\n\n"
        "Devuelve el plan en TEXTO claro para leer (NADA de JSON): una línea de resumen y luego "
        "DESAYUNO, COMIDA y CENA (cada uno con su kcal objetivo, el platillo armado con sus "
        "alimentos y porciones caseras aproximadas), más un SNACK de entreno. Concreto y breve; "
        "las porciones deben acercarse a las kcal de cada comida. Atleta de 19 con gasto muy alto: "
        "cubrir energía, sin restringir."
    )
    resp = client.messages.create(
        model=MODEL, max_tokens=1600, system=f"{PERSONA}\n\n{GUARDRAILS}",
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()


def print_plan(nutri, texto):
    print("\n============== TID-MAX · PLAN DE COMIDAS DEL DÍA ==============")
    print(f"Objetivo: ~{nutri['kcal_objetivo']} kcal · P {nutri['proteina_g']}g · "
          f"C {nutri['carbohidratos_g']}g · G {nutri['grasa_g']}g  (nado {nutri.get('km_dia')} km)")
    if texto:
        print("\n" + texto)
    print("\n(Estimaciones para orientar; ajústalas con un nutriólogo del deporte.)")


def print_memoria():
    mem = construir_memoria(top=99)
    if not mem:
        print("\nAún no hay memoria de alimentos. Sube algunas comidas (foto o --texto) y el "
              "agente irá aprendiendo los platillos recurrentes de Gael.")
        return
    print("\n============== TID-MAX · MEMORIA DE ALIMENTOS (lo aprendido) ==============")
    print("Platillos que el agente ya reconoce y autocompleta cuando faltan detalles:\n")
    for m in mem:
        al = ", ".join(m["alimentos_frecuentes"][:4])
        print(f"  • {m['platillo']}  —  {m['veces']}× · ~{m['kcal_tipico']} kcal "
              f"(C {m['carb_g']} / P {m['prot_g']} / G {m['grasa_g']}) · últ. {m['ultima_vez']}")
        if al:
            print(f"      alimentos: {al}")
    print("\n(El agente usa esto para reconocer una foto sin detalles y estimar como 'de siempre'.)")


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

    if "--memoria" in args:
        print_memoria()
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
        print_plan(nutri, plan)
        return

    if "--consumo" in args:
        if os.path.exists(CONSUMO_JSON):
            with open(CONSUMO_JSON, encoding="utf-8") as fh:
                d = json.load(fh)
            if d.get("fecha") == _hoy():
                print_consumo(d)
            else:
                print("Aún no hay consumo registrado HOY. Manda una comida con foto o --texto.")
        else:
            print("Aún no hay consumo registrado. Manda una comida con foto o --texto.")
        return

    if "--reset-consumo" in args:
        if os.path.exists(CONSUMO_JSON):
            os.remove(CONSUMO_JSON)
        print("Consumo de hoy reiniciado.")
        return

    if "--texto" in args:
        i = args.index("--texto")
        desc = args[i + 1] if i + 1 < len(args) else ""
        if not desc:
            sys.exit('Uso: python tid_nutricion.py --texto "6 huevos con frijoles, licuado, 50 g totopos"')
        client = ai_client() if have_api() else None
        if not client:
            sys.exit("Necesito ANTHROPIC_API_KEY (y el SDK) para estimar por texto.")
        est = ai_estimate_texto(client, desc, tipo_dia, base)
        print_estimacion(est)
        print_consumo(registrar_consumo(est, "texto"))
        if "--avisar" in args:
            avisar_familia()
        return

    fotos = [a for a in args if not a.startswith("--")]
    if not fotos:
        sys.exit("Uso: python tid_nutricion.py <foto.jpg> [--tipo doble|sencilla] | --plantilla")
    img_path = os.path.expanduser(fotos[0])
    if not os.path.exists(img_path):
        # Si diste solo el nombre, búscalo en las carpetas típicas del Mac
        base_name = os.path.basename(img_path)
        for cand in (os.path.expanduser(f"~/Downloads/{base_name}"),
                     os.path.expanduser(f"~/Descargas/{base_name}"),
                     os.path.expanduser(f"~/Desktop/{base_name}"),
                     os.path.expanduser(f"~/Escritorio/{base_name}")):
            if os.path.exists(cand):
                img_path = cand
                print(f"(Foto encontrada en: {img_path})")
                break
        else:
            sys.exit(f"No encuentro la foto: {fotos[0]}\n"
                     "Tip: arrastra la imagen desde Finder a la terminal para pegar su ruta, "
                     "o guárdala en ~/Downloads y usa solo el nombre.")

    client = ai_client() if have_api() else None
    if client:
        try:
            est = ai_estimate(client, img_path, tipo_dia, base)
            print_estimacion(est)
            print_consumo(registrar_consumo(est, "foto"))
            if "--avisar" in args:
                avisar_familia()
            return
        except Exception as e:
            print(f"(Aviso: falló la llamada IA: {e}. Caigo a modo base.)")
    fallback(base, tipo_dia)


if __name__ == "__main__":
    main()
