#!/usr/bin/env python3
"""
hrv_rr.py — Pipeline de HRV sobre R-R CRUDO (latido a latido).

Toma la serie de intervalos R-R (ms) tal como la captura el Polar (H10 / Verity Sense)
y saca las métricas que WHOOP NO expone por API y que hoy TID-MAX tiraba (sólo contaba
las muestras). Inspirado en lo que NOOP hace y enseña ("rMSSD por ventanas", Poincaré,
DFA-α1): parte del R-R crudo, filtra latidos raros (ectópicos) y de ahí deriva todo.

Flujo:
    R-R crudo → filtra_ectopicos (Malik 20%) → métricas de dominio temporal
    (RMSSD, SDNN, pNN50), Poincaré (SD1/SD2), DFA-α1 (Plews) y RMSSD por ventanas.

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
                })
        inicio += paso_s
    return salida


# ------------------------------------------------------- orquestador

def analiza_rr(rr_ms, umbral_ectopicos=0.2):
    """
    Pipeline completo sobre una serie de R-R crudos. Devuelve un dict con las métricas
    y metadatos de calidad (cuántos latidos se descartaron). Campos en None cuando no
    hay suficientes datos para calcularlos con sentido.
    """
    limpio, descartados = filtra_ectopicos(rr_ms, umbral_ectopicos)
    n = len(limpio)
    pct_desc = round(100.0 * descartados / len(rr_ms), 1) if rr_ms else None
    res = {
        "n_latidos_crudos": len(rr_ms),
        "n_latidos_limpios": n,
        "descartados": descartados,
        "pct_descartados": pct_desc,
        "rmssd_ms": round(rmssd(limpio), 2) if n >= 2 else None,
        "sdnn_ms": round(sdnn(limpio), 2) if n >= 2 else None,
        "pnn50": round(pnn50(limpio), 2) if n >= 2 else None,
        "poincare": poincare(limpio) if n >= 3 else None,
        "dfa_alpha1": dfa_alpha1(limpio),
        "rmssd_ventanas": rmssd_por_ventanas(limpio),
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
    print("RMSSD (ms):       ", r["rmssd_ms"])
    print("SDNN (ms):        ", r["sdnn_ms"])
    print("pNN50 (%):        ", r["pnn50"])
    print("Poincaré:         ", r["poincare"])
    print("DFA-α1:           ", r["dfa_alpha1"])
    print("Ventanas RMSSD:   ", len(r["rmssd_ventanas"]), "ventanas")
    assert r["n_latidos_limpios"] < r["n_latidos_crudos"], "debió descartar ectópicos"
    assert r["rmssd_ms"] is not None and r["rmssd_ms"] > 0
    assert r["dfa_alpha1"] is not None
    print("\nOK — pipeline de R-R funcional.")
