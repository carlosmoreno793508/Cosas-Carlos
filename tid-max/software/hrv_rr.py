#!/usr/bin/env python3
"""
hrv_rr.py — Pipeline de HRV sobre R-R CRUDO (latido a latido).

Toma la serie de intervalos R-R (ms) tal como la captura el Polar (H10 / Verity Sense)
y saca las métricas que WHOOP NO expone por API y que hoy TID-MAX tiraba (sólo contaba
las muestras). Inspirado en lo que NOOP hace y enseña ("rMSSD por ventanas", Poincaré,
DFA-α1): parte del R-R crudo, filtra latidos raros (ectópicos) y de ahí deriva todo.

Flujo:
    R-R crudo → limpieza Malik 20% en SEGMENTOS contiguos (gap-aware) → métricas de
    dominio temporal (RMSSD, SDNN, pNN50), Poincaré (SD1/SD2), DFA-α1 (Plews),
    RMSSD por ventanas y HRV nocturna por selección de CALIDAD (no por etapa de sueño).

Dos mejoras validadas contra datos reales de WHOOP (del `RR-OPTIMIZATION.md` del proyecto
NOOP, código abierto; ver dossier `analisis/noop-ipa-teardown.md`):
  1. RMSSD/pNN50/Poincaré GAP-AWARE: las diferencias sucesivas no cruzan un latido
     descartado (evita el empalme que infla RMSSD). MAE de HRV nocturna vs WHOOP
     8.47 → 5.47 ms (−35%). En datos sin descartes es idéntico al camino plano.
  2. HRV por VARIANZA/CALIDAD: mediana de RMSSD de las ventanas más quietas (no por
     sueño profundo — eso quedó refutado). Corrigió la correlación de recuperación de
     −0.485 a +0.665 (n=20).

Sin dependencias externas (sólo stdlib `math`), igual que el resto del motor.

NOTA DE HONESTIDAD: son estimaciones en el dispositivo, NO un diagnóstico. La calidad
depende del sensor: el H10 (ECG de pecho) da R-R limpio; el Verity Sense (óptico de brazo)
da R-R más ruidoso, por lo que DFA-α1 conviene calcularlo en reposo/quieto. El filtro de
ectópicos ayuda, pero no sustituye una buena captura.
"""
import math

# ------------------------------------------------------------------ utilidades

def _media(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _desv_est(xs):
    """Desviación estándar poblacional."""
    n = len(xs)
    if n < 2:
        return 0.0
    m = _media(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / n)


def _mediana(xs):
    """Mediana (robusta a atípicos). Devuelve None si la lista está vacía."""
    if not xs:
        return None
    ys = sorted(xs)
    n = len(ys)
    mid = n // 2
    if n % 2:
        return ys[mid]
    return (ys[mid - 1] + ys[mid]) / 2.0


def _difs_sucesivas(rr):
    """Diferencias entre latidos consecutivos (NN[i+1] - NN[i])."""
    return [rr[i + 1] - rr[i] for i in range(len(rr) - 1)]


# ------------------------------------------------------- filtro de ectópicos

def filtra_ectopicos(rr_ms, umbral=0.2):
    """
    Filtro de Malik: descarta un latido si difiere más de `umbral` (20% por defecto)
    respecto al último latido ACEPTADO. Quita latidos ectópicos/artefactos que inflan
    falsamente la HRV. También tira valores fisiológicamente imposibles (fuera de
    300–2000 ms ≈ 30–200 lpm).

    Devuelve (rr_limpio, n_descartados).
    """
    limpio = []
    descartados = 0
    previo = None
    for x in rr_ms:
        if x is None or x < 300 or x > 2000:
            descartados += 1
            continue
        if previo is None:
            limpio.append(x)
            previo = x
            continue
        if abs(x - previo) > umbral * previo:
            descartados += 1
            continue
        limpio.append(x)
        previo = x
    return limpio, descartados


def limpia_segmentos(rr_ms, umbral=0.2):
    """
    Variante GAP-AWARE del filtro de Malik. Acepta exactamente los MISMOS latidos que
    `filtra_ectopicos` (mismo umbral, mismos rangos), pero en lugar de una lista plana
    devuelve una lista de SEGMENTOS contiguos: cada vez que se descarta ≥1 latido entre
    dos aceptados, se abre un segmento nuevo.

    ¿Por qué importa? (lección del `RR-OPTIMIZATION.md` de NOOP, validada contra datos
    reales de WHOOP): al borrar un latido, sus dos vecinos quedan adyacentes en la lista
    limpia y la diferencia sucesiva a través de ese "empalme" se cuenta como un delta
    latido-a-latido real. Como RMSSD eleva cada delta al cuadrado, UN latido quitado puede
    inflar RMSSD. Calcular las diferencias sucesivas SÓLO dentro de cada segmento evita el
    empalme. En una serie sin descartes hay un único segmento y el resultado es idéntico al
    camino plano (por eso no rompe los vectores de prueba ni los datos limpios).

    Nota de honestidad (misma fuente): el over-read de NOOP vs WHOOP venía de ESTO —
    inflación por artefactos de R-R escaso/recortado— y NO de la ventana de sueño elegida.
    El fix correcto es limpiar gap-aware, no re-ventanear hacia sueño profundo.

    Devuelve (segmentos, descartados) donde `segmentos` es lista de listas de R-R (ms).
    `[x for seg in segmentos for x in seg]` == la salida de `filtra_ectopicos`.
    """
    segmentos = []
    actual = []
    descartados = 0
    previo = None
    hueco = False  # ¿se descartó algún latido desde el último aceptado?
    for x in rr_ms:
        if x is None or x < 300 or x > 2000:
            descartados += 1
            hueco = True
            continue
        if previo is None:
            actual = [x]
            previo = x
            hueco = False
            continue
        if abs(x - previo) > umbral * previo:
            descartados += 1
            hueco = True
            continue
        # Latido aceptado.
        if hueco and actual:
            segmentos.append(actual)
            actual = [x]
        else:
            actual.append(x)
        previo = x
        hueco = False
    if actual:
        segmentos.append(actual)
    return segmentos, descartados


# ------------------------------------------------------- dominio temporal

def rmssd(rr):
    """Raíz de la media de los cuadrados de las diferencias sucesivas (ms). HRV parasimpática."""
    d = _difs_sucesivas(rr)
    if not d:
        return None
    return math.sqrt(_media([x * x for x in d]))


def sdnn(rr):
    """Desviación estándar de los intervalos NN (ms). HRV global."""
    if len(rr) < 2:
        return None
    return _desv_est(rr)


def pnn50(rr):
    """% de diferencias sucesivas > 50 ms."""
    d = _difs_sucesivas(rr)
    if not d:
        return None
    return 100.0 * sum(1 for x in d if abs(x) > 50) / len(d)


def _difs_segmentos(segmentos):
    """Diferencias sucesivas agrupadas SÓLO dentro de cada segmento (nunca cruzan un hueco)."""
    d = []
    for seg in segmentos:
        d.extend(_difs_sucesivas(seg))
    return d


def rmssd_gap(segmentos):
    """RMSSD gap-aware: salta cualquier diferencia que cruce un latido descartado."""
    d = _difs_segmentos(segmentos)
    if not d:
        return None
    return math.sqrt(_media([x * x for x in d]))


def pnn50_gap(segmentos):
    """pNN50 gap-aware: sólo diferencias dentro de segmento."""
    d = _difs_segmentos(segmentos)
    if not d:
        return None
    return 100.0 * sum(1 for x in d if abs(x) > 50) / len(d)


def poincare(rr):
    """
    Gráfico de Poincaré: SD1 (variabilidad latido a latido, ≈ parasimpático) y
    SD2 (variabilidad a largo plazo). Relación SD1/SD2 = balance.
    """
    d = _difs_sucesivas(rr)
    if len(d) < 1 or len(rr) < 2:
        return None
    sdsd = _desv_est(d)
    sd1 = math.sqrt(0.5) * sdsd
    var_nn = _desv_est(rr) ** 2
    arg = 2 * var_nn - 0.5 * sdsd ** 2
    sd2 = math.sqrt(arg) if arg > 0 else 0.0
    return {
        "sd1": round(sd1, 2),
        "sd2": round(sd2, 2),
        "ratio": round(sd1 / sd2, 3) if sd2 > 0 else None,
    }


def poincare_gap(segmentos):
    """
    Poincaré gap-aware: SD1 se deriva de SDSD (diferencias sucesivas), así que usa sólo
    diferencias intra-segmento; SD2 usa la varianza de TODOS los NN (no cruza huecos porque
    es un estadístico global, no latido-a-latido).
    """
    flat = [x for seg in segmentos for x in seg]
    d = _difs_segmentos(segmentos)
    if len(d) < 1 or len(flat) < 2:
        return None
    sdsd = _desv_est(d)
    sd1 = math.sqrt(0.5) * sdsd
    var_nn = _desv_est(flat) ** 2
    arg = 2 * var_nn - 0.5 * sdsd ** 2
    sd2 = math.sqrt(arg) if arg > 0 else 0.0
    return {
        "sd1": round(sd1, 2),
        "sd2": round(sd2, 2),
        "ratio": round(sd1 / sd2, 3) if sd2 > 0 else None,
    }


# ------------------------------------------------------- DFA-α1 (Plews)

def _pendiente_minimos_cuadrados(xs, ys):
    """Pendiente de la recta de mínimos cuadrados y = a·x + b."""
    n = len(xs)
    if n < 2:
        return None
    mx, my = _media(xs), _media(ys)
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    if den == 0:
        return None
    return num / den


def dfa_alpha1(rr, min_box=4, max_box=16):
    """
    Detrended Fluctuation Analysis — exponente de escala de CORTO plazo (α1).
    Marcador de umbral aeróbico (Plews/Rogers): α1≈1.0 en reposo/baja intensidad,
    cae hacia ~0.5 al cruzar el primer umbral ventilatorio.

    Requiere suficientes latidos: con cajas de hasta 16, se piden ≥ 2·max_box = 32
    para tener al menos 2 cajas en la escala mayor. Devuelve None si no alcanza.
    """
    n_total = len(rr)
    if n_total < 2 * max_box:
        return None
    # Serie integrada (random walk) centrada en la media.
    m = _media(rr)
    acum, s = [], 0.0
    for x in rr:
        s += x - m
        acum.append(s)
    escalas, flucts = [], []
    for n in range(min_box, max_box + 1):
        n_cajas = n_total // n
        if n_cajas < 2:
            continue
        xs = list(range(n))
        residuos_cuadrados = []
        for b in range(n_cajas):
            seg = acum[b * n:(b + 1) * n]
            # Ajuste lineal (tendencia local) y residuo.
            mx, my = _media(xs), _media(seg)
            den = sum((xs[i] - mx) ** 2 for i in range(n))
            if den == 0:
                continue
            pend = sum((xs[i] - mx) * (seg[i] - my) for i in range(n)) / den
            inter = my - pend * mx
            for i in range(n):
                tendencia = pend * xs[i] + inter
                residuos_cuadrados.append((seg[i] - tendencia) ** 2)
        if residuos_cuadrados:
            f_n = math.sqrt(_media(residuos_cuadrados))
            if f_n > 0:
                escalas.append(math.log(n))
                flucts.append(math.log(f_n))
    if len(escalas) < 2:
        return None
    alpha = _pendiente_minimos_cuadrados(escalas, flucts)
    return round(alpha, 3) if alpha is not None else None


# ------------------------------------------------------- RMSSD por ventanas

def rmssd_por_ventanas(rr, ventana_s=120, paso_s=60, min_latidos=20):
    """
    RMSSD rodante (como el "rMSSD por ventanas" de NOOP). El eje de tiempo se
    reconstruye con la suma acumulada de los R-R (cada R-R es su propia duración).
    Ventana de `ventana_s` segundos avanzando cada `paso_s`.

    Devuelve lista de {t_s, rmssd, n} por ventana con suficientes latidos.
    """
    if len(rr) < min_latidos:
        return []
    # Tiempo (s) al final de cada latido.
    t_acum, s = [], 0.0
    for x in rr:
        s += x / 1000.0
        t_acum.append(s)
    total_s = t_acum[-1]
    salida = []
    inicio = 0.0
    while inicio < total_s:
        fin = inicio + ventana_s
        ventana = [rr[i] for i in range(len(rr)) if inicio <= t_acum[i] < fin]
        if len(ventana) >= min_latidos:
            v = rmssd(ventana)
            if v is not None:
                salida.append({
                    "t_s": round(inicio, 1),
                    "rmssd": round(v, 2),
                    "n": len(ventana),
                    # SDNN de la ventana = proxy de "quietud" (menor = más estable/limpia).
                    # Base para seleccionar las ventanas menos ruidosas (ver hrv_calidad).
                    "sdnn": round(sdnn(ventana), 2) if sdnn(ventana) is not None else None,
                })
        inicio += paso_s
    return salida


def hrv_calidad(ventanas, frac_quietas=0.5, min_ventanas=3):
    """
    HRV nocturna por SELECCIÓN DE CALIDAD (no por etapa de sueño).

    Hallazgo validado en `RR-OPTIMIZATION.md` de NOOP (n=20 noches): seleccionar las
    ventanas de MENOR varianza (las más quietas) y tomar la MEDIANA de su RMSSD movió la
    correlación leave-one-out con la recuperación de WHOOP de −0.485 a +0.665. Es la misma
    idea de "libre de artefactos" aplicada en la SELECCIÓN de ventana en vez de en la
    limpieza de latidos, así que COMPONE con el camino gap-aware (no compite).

    IMPORTANTE (corrección de NOOP a la hipótesis previa): la selección por ETAPA de sueño
    (sueño profundo / SWS) está DESCARTADA — el sueño profundo tiene la HRV MÁS ALTA (HR
    bajo, tono vagal alto) y correlacionó NEGATIVAMENTE con WHOOP. Lo que vive es la
    selección por VARIANZA/calidad, que es esto.

    `frac_quietas`: fracción de ventanas más quietas a conservar (0.5 = mitad más estable).
    Devuelve dict con la mediana de RMSSD de esas ventanas, o None si no hay suficientes.
    """
    elegibles = [w for w in ventanas if w.get("sdnn") is not None and w.get("rmssd") is not None]
    if len(elegibles) < min_ventanas:
        return None
    elegibles.sort(key=lambda w: w["sdnn"])  # más quietas primero
    k = max(min_ventanas, int(round(len(elegibles) * frac_quietas)))
    k = min(k, len(elegibles))
    quietas = elegibles[:k]
    med = _mediana([w["rmssd"] for w in quietas])
    return {
        "rmssd_mediana_ms": round(med, 2) if med is not None else None,
        "n_ventanas_usadas": k,
        "n_ventanas_total": len(elegibles),
        "frac_quietas": frac_quietas,
        "metodo": "mediana RMSSD de ventanas de menor varianza (selección por calidad, no por etapa)",
    }


# ------------------------------------------------------- orquestador

def analiza_rr(rr_ms, umbral_ectopicos=0.2):
    """
    Pipeline completo sobre una serie de R-R crudos. Devuelve un dict con las métricas
    y metadatos de calidad (cuántos latidos se descartaron). Campos en None cuando no
    hay suficientes datos para calcularlos con sentido.
    """
    # Camino gap-aware: mismos latidos aceptados, pero en segmentos contiguos.
    segmentos, descartados = limpia_segmentos(rr_ms, umbral_ectopicos)
    limpio = [x for seg in segmentos for x in seg]  # == filtra_ectopicos(...) salida plana
    n = len(limpio)
    pct_desc = round(100.0 * descartados / len(rr_ms), 1) if rr_ms else None
    ventanas = rmssd_por_ventanas(limpio)
    res = {
        "n_latidos_crudos": len(rr_ms),
        "n_latidos_limpios": n,
        "descartados": descartados,
        "pct_descartados": pct_desc,
        "n_segmentos": len(segmentos),
        # Camino PLANO (compatibilidad con lo ya construido; idéntico a gap-aware sin huecos).
        "rmssd_ms": round(rmssd(limpio), 2) if n >= 2 else None,
        "pnn50": round(pnn50(limpio), 2) if n >= 2 else None,
        "poincare": poincare(limpio) if n >= 3 else None,
        # Camino GAP-AWARE (recomendado: no sesga RMSSD al alza por empalmes de latidos
        # eliminados; en datos limpios coincide con el plano). Fuente: RR-OPTIMIZATION.md.
        "rmssd_gap_ms": round(rmssd_gap(segmentos), 2) if n >= 2 else None,
        "pnn50_gap": round(pnn50_gap(segmentos), 2) if n >= 2 else None,
        "poincare_gap": poincare_gap(segmentos) if n >= 3 else None,
        # SDNN usa los valores NN (no diferencias sucesivas): no le afectan los empalmes.
        "sdnn_ms": round(sdnn(limpio), 2) if n >= 2 else None,
        "dfa_alpha1": dfa_alpha1(limpio),
        "rmssd_ventanas": ventanas,
        # HRV nocturna por selección de calidad (mediana de ventanas más quietas).
        "hrv_calidad": hrv_calidad(ventanas),
        "fuente": "R-R crudo (Polar) · estimación en dispositivo, no es diagnóstico",
    }
    return res


# ------------------------------------------------------- autoprueba

if __name__ == "__main__":
    import random
    random.seed(7)
    # Serie sintética ~60 lpm (1000 ms) con variabilidad fisiológica + 2 ectópicos.
    base = [1000 + random.gauss(0, 35) for _ in range(300)]
    base[50] = 1500   # latido perdido (ectópico largo)
    base[120] = 600   # latido extra (ectópico corto)
    r = analiza_rr(base)
    print("Latidos crudos:   ", r["n_latidos_crudos"])
    print("Latidos limpios:  ", r["n_latidos_limpios"], f"(descartó {r['descartados']})")
    print("Segmentos:        ", r["n_segmentos"])
    print("RMSSD plano (ms): ", r["rmssd_ms"])
    print("RMSSD gap (ms):   ", r["rmssd_gap_ms"])
    print("pNN50 / gap (%):  ", r["pnn50"], "/", r["pnn50_gap"])
    print("SDNN (ms):        ", r["sdnn_ms"])
    print("Poincaré gap:     ", r["poincare_gap"])
    print("DFA-α1:           ", r["dfa_alpha1"])
    print("Ventanas RMSSD:   ", len(r["rmssd_ventanas"]), "ventanas")
    print("HRV calidad:      ", r["hrv_calidad"])
    assert r["n_latidos_limpios"] < r["n_latidos_crudos"], "debió descartar ectópicos"
    assert r["n_segmentos"] >= 2, "los ectópicos debieron partir la serie en segmentos"
    assert r["rmssd_ms"] is not None and r["rmssd_ms"] > 0
    assert r["rmssd_gap_ms"] is not None and r["rmssd_gap_ms"] > 0
    # Con huecos presentes, gap-aware no cuenta los empalmes → RMSSD ≤ plano.
    assert r["rmssd_gap_ms"] <= r["rmssd_ms"], "gap-aware debió ser ≤ plano al haber descartes"

    # Serie SIN ectópicos: gap-aware debe ser IDÉNTICO al plano (un solo segmento).
    limpia = [1000 + random.gauss(0, 20) for _ in range(200)]
    rc = analiza_rr(limpia)
    assert rc["n_segmentos"] == 1, "sin descartes debe haber un único segmento"
    assert rc["rmssd_gap_ms"] == rc["rmssd_ms"], "sin huecos gap-aware == plano"
    assert rc["pnn50_gap"] == rc["pnn50"]
    assert rc["hrv_calidad"] is not None and rc["hrv_calidad"]["rmssd_mediana_ms"] > 0
    print("\nOK — pipeline de R-R funcional (gap-aware + ventana por calidad).")
