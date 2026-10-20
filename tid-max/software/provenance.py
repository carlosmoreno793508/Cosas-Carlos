#!/usr/bin/env python3
"""
provenance.py — Modelo de PROCEDENCIA de TID-MAX (3 ejes), ejecutable.

Materializa los principios que aprendimos de NOOP (columna `Source` + `scoreInputProvenance`;
ver dossier `analisis/noop-ipa-teardown.md` y `ROADMAP-ESTRUCTURA.md`, Fase 2). Cada valor del
esquema canónico puede llevar su procedencia para que el producto NUNCA muestre un número sin
saber de dónde salió.

Tres ejes:
  1. FUENTE   — de qué dispositivo/ruta vino (whoop_device, import_whoop, apple_health, polar…).
  2. TIPO     — cómo se obtuvo: medido / estimado / importado / derivado / manual.
  3. CONFIANZA + MADUREZ — qué tan asentado está (por nº de noches de baseline).

Reglas de honestidad codificadas:
  - "no disponible ≠ 0": un dato ausente es None, nunca 0.
  - Scores AJENOS (WHOOP/Oura) = REFERENCIA; recomputamos los nuestros (tipo=importado/referencia).
  - Degradación por capacidad de fuente: cada fuente solo provee lo que físicamente puede
    (Polar = HR+R-R en vivo, NO sueño profundo).
  - Fusión "mejor valor por métrica" conservando la procedencia de cada valor.
  - Dedup por solape temporal (una sesión guardada/importada gana a una auto-detectada).

Sin dependencias externas (sólo stdlib).
"""

# ------------------------------------------------------------------ ejes (valores canónicos)

class Fuente:
    WHOOP_DEVICE = "whoop_device"     # banda WHOOP leída en vivo por BLE
    IMPORT_WHOOP = "import_whoop"     # CSV/zip export de WHOOP
    APPLE_HEALTH = "apple_health"     # import de Apple Health
    POLAR = "polar"                   # Polar H10 / Verity (HR + R-R en vivo)
    GARMIN = "garmin"
    OURA = "oura"
    FITBIT = "fitbit"
    MANUAL = "manual"                 # registro a mano (nado, pesas…)
    TIDMAX = "tidmax"                 # score calculado por nuestro motor


class Tipo:
    MEDIDO = "medido"         # sensor directo (HR, R-R)
    ESTIMADO = "estimado"     # derivado en dispositivo de otra señal (temp piel, resp)
    IMPORTADO = "importado"   # viene de un export de otra app
    DERIVADO = "derivado"     # calculado por nosotros a partir de medidos (nuestros scores)
    MANUAL = "manual"         # capturado por una persona
    REFERENCIA = "referencia" # score ajeno que guardamos solo como referencia


class Confianza:
    CALIBRANDO = "calibrando"
    BIEN = "bien"
    FUERTE = "fuerte"
    SOLIDA = "solida"
    GENIAL = "genial"


class Madurez:
    CALIBRANDO = "calibrando"
    CONSTRUYENDO = "construyendo"
    SOLIDA = "solida"


# Umbrales de madurez por nº de noches válidas (alineados con recovery_score).
MIN_NOCHES_SEED = 4     # usable (construyendo) a partir de aquí
MIN_NOCHES_TRUST = 14   # sólida


def madurez_por_noches(n_noches):
    if n_noches < MIN_NOCHES_SEED:
        return Madurez.CALIBRANDO
    if n_noches < MIN_NOCHES_TRUST:
        return Madurez.CONSTRUYENDO
    return Madurez.SOLIDA


# ------------------------------------------------------------------ capacidad por fuente

# Qué métricas provee cada fuente, y con qué TIPO. "sleep_deep"/"spo2" ausentes => no disponible.
CAPACIDAD_FUENTE = {
    Fuente.WHOOP_DEVICE: {"hr": Tipo.MEDIDO, "rr": Tipo.MEDIDO, "hrv": Tipo.MEDIDO,
                          "rhr": Tipo.MEDIDO, "skin_temp": Tipo.ESTIMADO, "resp": Tipo.ESTIMADO,
                          "sleep_stages": Tipo.ESTIMADO},  # SpO2 NO en vivo (necesita import)
    Fuente.IMPORT_WHOOP: {"hr": Tipo.IMPORTADO, "hrv": Tipo.IMPORTADO, "rhr": Tipo.IMPORTADO,
                          "spo2": Tipo.IMPORTADO, "sleep_stages": Tipo.IMPORTADO,
                          "strain": Tipo.REFERENCIA, "recovery": Tipo.REFERENCIA},
    Fuente.APPLE_HEALTH: {"hr": Tipo.IMPORTADO, "steps": Tipo.IMPORTADO, "sleep_stages": Tipo.IMPORTADO},
    Fuente.POLAR: {"hr": Tipo.MEDIDO, "rr": Tipo.MEDIDO},  # en vivo: HR + R-R; NO sueño profundo
    Fuente.MANUAL: {"swim_km": Tipo.MANUAL, "pesas_min": Tipo.MANUAL},
    Fuente.TIDMAX: {"carga": Tipo.DERIVADO, "descanso": Tipo.DERIVADO, "esfuerzo": Tipo.DERIVADO,
                    "acwr": Tipo.DERIVADO, "hrv_rmssd": Tipo.DERIVADO},
}


def fuente_provee(fuente, metrica):
    """Tipo con que `fuente` provee `metrica`, o None si esa fuente NO la provee (degradación)."""
    return CAPACIDAD_FUENTE.get(fuente, {}).get(metrica)


# ------------------------------------------------------------------ valor con procedencia

def marca(valor, fuente, metrica=None, confianza=Confianza.BIEN, n_noches=None, ts=None):
    """
    Envuelve un valor con su procedencia. Si `valor is None` devuelve None (no disponible ≠ 0):
    no fabricamos una envoltura para un dato que no existe.
    El TIPO se deriva de la capacidad de la fuente para esa métrica (si se da `metrica`).
    """
    if valor is None:
        return None  # "no disponible" se queda ausente, jamás 0
    tipo = fuente_provee(fuente, metrica) if metrica else None
    out = {"valor": valor, "fuente": fuente, "tipo": tipo, "confianza": confianza}
    if n_noches is not None:
        out["madurez"] = madurez_por_noches(n_noches)
    if ts is not None:
        out["ts"] = ts
    return out


# ------------------------------------------------------------------ fusión multi-fuente

# Prioridad de TIPO para elegir "el mejor valor por métrica".
_PRIORIDAD_TIPO = {
    Tipo.MEDIDO: 5, Tipo.MANUAL: 4, Tipo.IMPORTADO: 3, Tipo.ESTIMADO: 2,
    Tipo.DERIVADO: 2, Tipo.REFERENCIA: 0,  # un score ajeno nunca gana: es solo referencia
}
_PRIORIDAD_CONFIANZA = {
    Confianza.GENIAL: 4, Confianza.SOLIDA: 3, Confianza.FUERTE: 2,
    Confianza.BIEN: 1, Confianza.CALIBRANDO: 0,
}


def _prioridad(v):
    return (_PRIORIDAD_TIPO.get(v.get("tipo"), 1),
            _PRIORIDAD_CONFIANZA.get(v.get("confianza"), 1))


def fusion_mejor_valor(valores):
    """
    De varias lecturas de la MISMA métrica (cada una con procedencia vía `marca`), elige la mejor:
    medido > manual > importado > estimado/derivado > referencia; empata por confianza. Conserva
    la procedencia del valor elegido. None/ausentes se ignoran. Devuelve None si no hay ninguno.
    """
    candidatos = [v for v in valores if v is not None]
    if not candidatos:
        return None
    return max(candidatos, key=_prioridad)


# ------------------------------------------------------------------ dedup por solape temporal

def _solapan(a, b):
    return a["inicio"] < b["fin"] and b["inicio"] < a["fin"]


def dedup_sesiones(sesiones, prioridad=None):
    """
    Elimina sesiones que se solapan en el tiempo (como NOOP: una auto-detectada se omite si pisa
    una guardada/importada, incl. Apple Health). `sesiones` = lista de dicts con `inicio`/`fin`
    (comparables). `prioridad(sesion)` → mayor gana (default: guardada/importada > auto-detectada).
    Mantiene las no-solapadas; ante solape, conserva la de mayor prioridad.
    """
    if prioridad is None:
        orden = {"manual": 3, "importado": 2, "medido": 2, "auto": 0}
        def prioridad(s):
            return orden.get(s.get("origen"), 1)

    # Mayor prioridad primero; a igualdad, la más larga primero (más información).
    ordenadas = sorted(sesiones, key=lambda s: (prioridad(s), s["fin"] - s["inicio"]), reverse=True)
    conservadas = []
    for s in ordenadas:
        if not any(_solapan(s, k) for k in conservadas):
            conservadas.append(s)
    conservadas.sort(key=lambda s: s["inicio"])  # devolver en orden cronológico
    return conservadas


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    # 1) "no disponible ≠ 0": marcar None devuelve None, no una envoltura con 0.
    assert marca(None, Fuente.WHOOP_DEVICE, "hrv") is None
    print("no disponible ≠ 0: ✓ (None se queda None)")

    # 2) Tipo derivado de la capacidad de la fuente.
    m = marca(95.0, Fuente.WHOOP_DEVICE, "hrv")
    assert m["tipo"] == Tipo.MEDIDO
    mt = marca(33.1, Fuente.WHOOP_DEVICE, "skin_temp")
    assert mt["tipo"] == Tipo.ESTIMADO            # temp de piel = estimada en dispositivo
    assert fuente_provee(Fuente.POLAR, "sleep_stages") is None  # Polar NO da sueño profundo
    assert fuente_provee(Fuente.POLAR, "rr") == Tipo.MEDIDO     # pero sí R-R en vivo
    print("capacidad por fuente: ✓ (WHOOP temp=estimado · Polar no da sueño, sí R-R)")

    # 3) Madurez por noches.
    assert madurez_por_noches(2) == Madurez.CALIBRANDO
    assert madurez_por_noches(8) == Madurez.CONSTRUYENDO
    assert madurez_por_noches(20) == Madurez.SOLIDA
    print("madurez por noches: ✓ (2→calibrando · 8→construyendo · 20→sólida)")

    # 4) Fusión: HRV medido por WHOOP gana al importado; un score ajeno (referencia) nunca gana.
    hrv_med = marca(95.0, Fuente.WHOOP_DEVICE, "hrv")
    hrv_imp = marca(93.0, Fuente.IMPORT_WHOOP, "hrv")
    assert fusion_mejor_valor([hrv_imp, hrv_med])["fuente"] == Fuente.WHOOP_DEVICE
    # Nuestro Carga (derivado) gana al recovery de WHOOP (referencia).
    carga_ours = marca(66.0, Fuente.TIDMAX, "carga")
    recov_whoop = marca(66.0, Fuente.IMPORT_WHOOP, "recovery")
    assert fusion_mejor_valor([recov_whoop, carga_ours])["fuente"] == Fuente.TIDMAX
    print("fusión mejor valor: ✓ (medido>importado · nuestro score>referencia ajena)")

    # 5) Dedup por solape: una sesión auto-detectada que pisa una importada se elimina.
    sesiones = [
        {"inicio": 100, "fin": 200, "origen": "importado", "nombre": "WHOOP run"},
        {"inicio": 150, "fin": 220, "origen": "auto", "nombre": "auto-detect solapado"},
        {"inicio": 300, "fin": 400, "origen": "auto", "nombre": "auto-detect limpio"},
    ]
    res = dedup_sesiones(sesiones)
    nombres = [s["nombre"] for s in res]
    assert "WHOOP run" in nombres and "auto-detect limpio" in nombres
    assert "auto-detect solapado" not in nombres
    print("dedup por solape: ✓ (auto-detect solapado con importado se omite)")

    print("\nOK — modelo de procedencia 3 ejes funcional (fuente×tipo×madurez, fusión, dedup).")
