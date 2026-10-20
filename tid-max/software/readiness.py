#!/usr/bin/env python3
"""
readiness.py — HRV readiness (Plews/Altini, "smallest worthwhile change").

Port fiel del `HRVReadiness` de NOOP (código abierto; ver dossier). PURO, determinista.
Es una lectura de SÓLO LECTURA: NO cambia la Carga ni ningún score — es informativa.

Método (ciencia de resistencia, Plews et al. 2013 / Marco Altini):
  - Trabajar en el dominio LOG (ln RMSSD es más normal y estabiliza la varianza).
  - Baseline corto rodante de 7 noches vs una banda normal personal más larga (±0.5·SD, el SWC).
  - El tier sale de dónde cae el baseline de 7 noches respecto a esa banda:
      primed (arriba) · normal (dentro) · suppressed (debajo).
  - Una sola noche mala apenas mueve el baseline de 7 noches → mucho más robusto que un z de 1 noche.

Honestidad: devuelve None (calibrando) por debajo de 14 noches válidas — nunca inventa.
Es un experimento temprano, aún sin validar contra datos reales variables (n=1). APROXIMADO,
no es consejo médico.

Sin dependencias externas (sólo stdlib `math`).
"""
import math

# ------------------------------------------------------------------ constantes (mirror NOOP)

ROLL_WINDOW = 7            # baseline corto (7 noches, Plews/Altini)
LONG_WINDOW = 60          # ventana "normal personal" larga
LONG_WINDOW_FALLBACK = 30  # fallback si hay <60 noches válidas
SWC_K = 0.5               # media-anchura del SWC: banda = longMean ± 0.5·SD
MIN_NIGHTS = 14           # noches válidas mínimas antes de puntuar (si no → None)
CV_TREND_WINDOW = 28      # noches para la tendencia del CV (overreaching watch)
LONG_SD_FLOOR = 1e-9      # piso de SD para evitar banda de ancho cero
HRV_MIN_MS, HRV_MAX_MS = 5.0, 250.0  # límites fisiológicos (Baselines.hrvCfg)


def _media(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _sd_muestral(xs):
    """Desviación estándar muestral (n−1)."""
    n = len(xs)
    if n < 2:
        return 0.0
    m = _media(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def _pendiente_mc(ys):
    """Pendiente OLS de ys contra el índice 0..n−1."""
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(n))
    mx, my = _media(xs), _media(ys)
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return 0.0
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / den


def evaluate(avg_hrv):
    """
    `avg_hrv`: RMSSD nocturno (ms), más antigua → más reciente; None = noche faltante. Noches
    fuera de rango (5..250 ms) se descartan como artefactos de decodificación.

    Devuelve dict {tier, baseline7_ms, normal_low_ms, normal_high_ms, overreaching_watch} o None
    (calibrando) si hay menos de 14 noches válidas.
    """
    valid = [v for v in avg_hrv if v is not None and HRV_MIN_MS <= v <= HRV_MAX_MS]
    if len(valid) < MIN_NIGHTS:
        return None  # cold-start honesto

    ell = [math.log(max(v, 1.0)) for v in valid]  # dominio log (ln RMSSD)

    baseline7 = _media(ell[-ROLL_WINDOW:])

    long_win = LONG_WINDOW if len(valid) >= LONG_WINDOW else LONG_WINDOW_FALLBACK
    long_ell = ell[-long_win:]
    long_mean = _media(long_ell)
    long_sd_raw = _sd_muestral(long_ell) if len(long_ell) >= 2 else _sd_muestral(ell[-ROLL_WINDOW:])
    long_sd = max(long_sd_raw, LONG_SD_FLOOR)

    swc_half = SWC_K * long_sd
    normal_low = long_mean - swc_half
    normal_high = long_mean + swc_half

    if baseline7 > normal_high:
        tier = "primed"
    elif baseline7 >= normal_low:
        tier = "normal"
    else:
        tier = "suppressed"

    # Overreaching watch (INFORMATIVO, no cambia el tier): tendencia del coeficiente de variación
    # (CV) cayendo mientras el baseline de 7 noches está bajo la media larga (overreach parasimpático).
    cv_series = []
    cv_start = max(ROLL_WINDOW - 1, len(ell) - CV_TREND_WINDOW)
    for i in range(cv_start, len(ell)):
        w = ell[i - ROLL_WINDOW + 1:i + 1]
        m = _media(w)
        cv = 100.0 * _sd_muestral(w) / m if m != 0.0 else 0.0
        cv_series.append(cv)
    overreaching = _pendiente_mc(cv_series) < 0.0 and baseline7 < long_mean

    return {
        "tier": tier,                                  # primed / normal / suppressed
        "baseline7_ms": round(math.exp(baseline7), 1),
        "normal_low_ms": round(math.exp(normal_low), 1),
        "normal_high_ms": round(math.exp(normal_high), 1),
        "overreaching_watch": overreaching,
        "aprox": True,
        "fuente": "HRV readiness (Plews/Altini SWC) · SÓLO LECTURA, no cambia la Carga · APROXIMADO",
    }


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    import random
    random.seed(11)

    # <14 noches → None (calibrando, no inventa).
    assert evaluate([80, 82, 79, 85]) is None
    print("Cold-start (<14 noches): None ✓")

    # Serie estable ~80 ms (30 noches): baseline dentro de la banda → normal.
    estable = [80 + random.gauss(0, 4) for _ in range(30)]
    r = evaluate(estable)
    print("Estable:", r["tier"], "· base7", r["baseline7_ms"], "· banda",
          r["normal_low_ms"], "–", r["normal_high_ms"])
    assert r["tier"] == "normal"

    # Últimas 7 noches ELEVADAS sobre la base → primed.
    subiendo = [80 + random.gauss(0, 3) for _ in range(23)] + [100 + random.gauss(0, 2) for _ in range(7)]
    rp = evaluate(subiendo)
    print("Subiendo:", rp["tier"], "· base7", rp["baseline7_ms"])
    assert rp["tier"] == "primed"

    # Últimas 7 noches DEPRIMIDAS → suppressed.
    bajando = [80 + random.gauss(0, 3) for _ in range(23)] + [58 + random.gauss(0, 2) for _ in range(7)]
    rs = evaluate(bajando)
    print("Bajando:", rs["tier"], "· base7", rs["baseline7_ms"], "· overreach", rs["overreaching_watch"])
    assert rs["tier"] == "suppressed"

    # Noches fuera de rango (artefactos) se descartan.
    con_basura = estable + [999, -5, None]
    assert evaluate(con_basura)["tier"] == evaluate(estable)["tier"]
    print("Artefactos (999/-5/None) descartados ✓")

    print("\nOK — HRV readiness (Plews/Altini SWC) funcional (7n vs banda ±0.5·SD, cold-start honesto).")
