#!/usr/bin/env python3
"""
coach_llm.py — Coach IA "BYOK local-first" (trae tu propia clave).

Reproduce el patrón del Entrenador de NOOP (ver dossier): el coach usa TU propia clave de API;
eliges proveedor y modelo; **es la única función que sale del dispositivo**, y sólo cuando lo
pides explícitamente (llamando `pregunta_coach`). Apuntándolo a un servidor local
(Ollama / LM Studio / llama.cpp, todos compatibles con OpenAI) todo se queda en tu máquina.

Privacidad por diseño:
  - La clave viene por parámetro o variable de entorno; NUNCA se guarda en el repo ni se registra.
  - Sólo se envía un RESUMEN de métricas + tu pregunta; nada más.
  - `construye_peticion` arma la petición SIN enviarla (testeable offline). `pregunta_coach` es
    la única que abre red (stdlib `urllib`).

Proveedores: `openai` y cualquier servidor compatible con OpenAI vía `base_url`
(Ollama `http://localhost:11434/v1`, LM Studio, llama.cpp, tu pasarela), y `anthropic`.

Sólo stdlib (`json`, `os`, `urllib`).
"""
import os
import json
import urllib.request
import urllib.error

SYSTEM_PROMPT = (
    "Eres el entrenador de TID-MAX. Respondes sobre carga, esfuerzo, descanso y entrenamientos "
    "a partir de los NÚMEROS del atleta que se te pasan. Los scores son APROXIMADOS (no son de "
    "WHOOP ni diagnóstico médico). Sé concreto y accionable; si falta un dato, dilo en vez de "
    "inventarlo."
)

DEFAULT_OPENAI_BASE = "https://api.openai.com/v1"
ANTHROPIC_BASE = "https://api.anthropic.com"
ANTHROPIC_VERSION = "2023-06-01"


def construye_resumen(metricas):
    """
    Resumen compacto y legible de las métricas recientes para enviar al modelo. `metricas` es un
    dict (p. ej. la última fila de `tid_data.build_daily`, o varias). Sólo incluye lo presente
    (no disponible ≠ 0: un campo ausente simplemente no aparece). NO incluye claves ni PII.
    """
    campos = [
        ("carga_tidmax", "Carga"), ("carga_banda", "banda Carga"),
        ("descanso_tidmax", "Descanso"), ("esfuerzo_ref_0_100", "Esfuerzo(ref)"),
        ("acwr", "ACWR"), ("hrv_ms", "VFC ms"), ("rhr_bpm", "FC reposo"),
        ("sleep_asleep_noche_h", "sueño h"), ("deuda_sueno_min", "deuda sueño min"),
    ]
    partes = []
    for k, label in campos:
        v = metricas.get(k)
        if v is not None:
            partes.append(f"{label}={v}")
    return "; ".join(partes) if partes else "(sin métricas disponibles)"


def construye_peticion(proveedor, modelo, resumen, pregunta,
                       base_url=None, api_key=None, header_clave="bearer", max_tokens=600):
    """
    Arma la petición HTTP SIN enviarla. Devuelve {method, url, headers, body(dict)}.
      proveedor      "openai" (o compatible) | "anthropic".
      base_url       servidor compatible-OpenAI (p. ej. Ollama local); None → OpenAI oficial.
      header_clave   "bearer" (Authorization: Bearer) | "x-api-key" (pasarelas que la piden ahí).
    La clave va SOLO en la cabecera, nunca en el cuerpo ni en el resumen.
    """
    contenido_usuario = f"Mis números de hoy: {resumen}\n\nPregunta: {pregunta}"

    if proveedor == "anthropic":
        url = f"{base_url or ANTHROPIC_BASE}/v1/messages"
        headers = {"content-type": "application/json", "anthropic-version": ANTHROPIC_VERSION}
        if api_key:
            headers["x-api-key"] = api_key
        body = {
            "model": modelo,
            "max_tokens": max_tokens,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": contenido_usuario}],
        }
        return {"method": "POST", "url": url, "headers": headers, "body": body}

    # openai / compatible (Ollama, LM Studio, llama.cpp, pasarela)
    url = f"{(base_url or DEFAULT_OPENAI_BASE).rstrip('/')}/chat/completions"
    headers = {"content-type": "application/json"}
    if api_key:
        if header_clave == "x-api-key":
            headers["x-api-key"] = api_key
        else:
            headers["authorization"] = f"Bearer {api_key}"
    body = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": contenido_usuario},
        ],
    }
    return {"method": "POST", "url": url, "headers": headers, "body": body}


def es_local(url):
    """True si la URL apunta a la propia máquina/red (localhost/127.*/privada): nada sale."""
    u = url.lower()
    return ("://localhost" in u or "://127." in u or "://0.0.0.0" in u
            or "://192.168." in u or "://10." in u or ".local" in u)


def pregunta_coach(proveedor, modelo, metricas, pregunta, base_url=None,
                   api_key=None, header_clave="bearer", timeout=60):
    """
    LA ÚNICA función que abre red. Construye el resumen + la petición y la ENVÍA al servidor que
    elijas (local u oficial), con tu clave. Devuelve el texto de la respuesta.

    La clave se toma de `api_key` o, si es None, de la variable de entorno del proveedor
    (OPENAI_API_KEY / ANTHROPIC_API_KEY) — nunca del código. Apunta `base_url` a un modelo local
    para que nada salga de tu máquina.
    """
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY" if proveedor == "anthropic" else "OPENAI_API_KEY")
    resumen = construye_resumen(metricas)
    pet = construye_peticion(proveedor, modelo, resumen, pregunta,
                             base_url=base_url, api_key=api_key, header_clave=header_clave)
    data = json.dumps(pet["body"]).encode("utf-8")
    req = urllib.request.Request(pet["url"], data=data, headers=pet["headers"], method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    # Extraer el texto según el proveedor.
    if proveedor == "anthropic":
        bloques = payload.get("content", [])
        return "".join(b.get("text", "") for b in bloques if b.get("type") == "text")
    choices = payload.get("choices", [])
    return choices[0]["message"]["content"] if choices else ""


# ------------------------------------------------------------------ autoprueba (offline, sin red)

if __name__ == "__main__":
    metricas = {"carga_tidmax": 66.0, "carga_banda": "amarillo", "descanso_tidmax": 80.0,
                "esfuerzo_ref_0_100": 28.1, "acwr": 1.21, "hrv_ms": 95.0, "rhr_bpm": 50,
                "sleep_asleep_noche_h": 6.9, "deuda_sueno_min": 64}
    resumen = construye_resumen(metricas)
    print("Resumen:", resumen)
    assert "Carga=66.0" in resumen and "VFC ms=95.0" in resumen

    SECRETO = "sk-TEST-no-real-key-123"

    # OpenAI oficial: clave en Authorization Bearer, system+user en messages.
    p = construye_peticion("openai", "gpt-5-mini", resumen, "¿Entreno hoy?", api_key=SECRETO)
    assert p["url"] == "https://api.openai.com/v1/chat/completions"
    assert p["headers"]["authorization"] == f"Bearer {SECRETO}"
    assert p["body"]["messages"][0]["role"] == "system"
    assert SECRETO not in json.dumps(p["body"])          # la clave NUNCA va en el cuerpo
    assert SECRETO not in resumen                        # ni en el resumen de métricas
    print("OpenAI: clave solo en cabecera ✓")

    # Local (Ollama): nada sale de la máquina.
    pl = construye_peticion("openai", "llama3", resumen, "¿Y mañana?",
                            base_url="http://localhost:11434/v1", api_key=None)
    assert pl["url"] == "http://localhost:11434/v1/chat/completions"
    assert es_local(pl["url"]) and "authorization" not in pl["headers"]
    assert not es_local("https://api.openai.com/v1/chat/completions")
    print("Local (Ollama): se queda en la máquina ✓")

    # Anthropic: x-api-key + anthropic-version + system separado.
    pa = construye_peticion("anthropic", "claude-sonnet-4-6", resumen, "¿Descanso?", api_key=SECRETO)
    assert pa["url"] == "https://api.anthropic.com/v1/messages"
    assert pa["headers"]["x-api-key"] == SECRETO and pa["headers"]["anthropic-version"] == ANTHROPIC_VERSION
    assert pa["body"]["system"] == SYSTEM_PROMPT and SECRETO not in json.dumps(pa["body"])
    print("Anthropic: x-api-key en cabecera, system separado ✓")

    # No disponible ≠ 0: un dict vacío no fabrica ceros.
    assert construye_resumen({}) == "(sin métricas disponibles)"

    print("\nOK — coach BYOK local-first funcional (clave solo en cabecera, local se queda local).")
