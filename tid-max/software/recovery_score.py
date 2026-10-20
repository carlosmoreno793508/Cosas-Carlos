#!/usr/bin/env python3
"""
recovery_score.py — Score de CARGA / Recuperación (0–100) sobre datos crudos del Polar.

Port fiel del `RecoveryScorer` del proyecto NOOP (código abierto, PolyForm Noncommercial),
que a su vez porta `server/ingest/app/analysis/recovery.py`. Ver el dossier
`analisis/noop-ipa-teardown.md` (sección del código fuente de NOOP) para la cadena completa.

Es un compuesto z-score + logística, HRV-dominante, normalizado contra el baseline PERSONAL.
Es APROXIMADO — NO reproduce el número propietario de WHOOP; es un proxy transparente y
explicable. Cada término se estandariza a un z-score robusto contra el baseline personal
(media + spread EWMA de la desviación absoluta); los términos ausentes se CAEN y los pesos se
RENORMALIZAN, así que el score sin un término es idéntico a como si ese término no existiera.

Pesos (los mismos de NOOP; ver dossier A.12):
    HRV vs baseline      ↑ → mejor   W_HRV       = 0.55  (dominante)
    RHR vs baseline      ↓ → mejor   W_RHR       = 0.20
    calidad de sueño     ↑ → mejor   W_SLEEP     = 0.15
    respiración          ↓ → mejor   W_RESP      = 0.05
    desviación temp piel |Δ| → peor  W_SKIN_TEMP = 0.05  (penalización SIMÉTRICA)
  opcionales (nil por defecto; cierran el hueco con Oura Readiness):
    pendiente de caída RHR nocturna  W_RECOVERY_INDEX   = 0.05
    Effort del día previo vs base    W_ACTIVITY_BALANCE = 0.05

Regla de honestidad (la misma de NOOP): si el baseline de HRV (driver dominante) aún no es
usable (< MIN_NOCHES_SEED noches válidas), `carga()` devuelve None en vez de inventar un
número. El llamador puede usar MEDIA_POBLACIONAL (58.0) como respaldo, pero DEBE marcarlo.

Sin dependencias externas (sólo stdlib `math`), igual que el resto del motor.
"""
import math

# ------------------------------------------------------------------ constantes (recovery.py)

W_HRV = 0.55
W_RHR = 0.20
W_SLEEP = 0.15
W_RESP = 0.05
W_SKIN_TEMP = 0.05
W_RECOVERY_INDEX = 0.05
W_ACTIVITY_BALANCE = 0.05

# Escala de la penalización por temp de piel (°C): 1 °C de desviación ≈ 1 z-unit. Simétrica.
ESCALA_TEMP_PIEL_C = 1.0
# Escala del "Recovery Index" (bpm/hora): una pendiente así de pronunciada ≈ 1 z-unit.
# El SIGNO lleva el significado: negativo (RHR cayendo durante la noche) = bueno.
ESCALA_RECOVERY_INDEX_BPM_H = 2.0

# Logística: ±2 z ≈ banda Rojo–Verde completa (15%–95%).
LOGISTIC_K = 1.6
# Offset para que z=0 → 58% (media poblacional publicada por WHOOP).
LOGISTIC_Z0 = -0.20
MEDIA_POBLACIONAL = 58.0

# Bandas (esquema de color WHOOP).
BANDA_ROJO_MAX = 34.0
BANDA_AMARILLO_MAX = 67.0

# Sueño: centro "buena noche" ≈ 85% de eficiencia; escala ±2 z abarca el rango normal.
SUENO_CENTRO = 0.85
SUENO_ESCALA = 0.12

# Baseline personal (EWMA). Vidas medias en NOCHES (de Baselines.swift de NOOP).
VIDA_MEDIA_CENTRO = 14.0   # media personal
VIDA_MEDIA_SPREAD = 21.0   # spread (más lento que el centro)
MIN_NOCHES_SEED = 4        # usable (provisional) a partir de aquí
MIN_NOCHES_TRUST = 14      # plenamente confiable


# ------------------------------------------------------------------ z-score robusto + baseline

def z_robusto(valor, media, spread):
    """z robusto con spread EWMA de desviación absoluta: (x − μ) / (1.253 × spread).

    1.253 × MAD ≈ σ para una normal (E|X−μ| = σ·√(2/π) ≈ 0.7979σ)."""
    sigma = max(1.253 * spread, 1e-9)
    return (valor - media) / sigma


def _lambda(vida_media):
    """Factor de suavizado EWMA a partir de una vida media en noches."""
    return 1.0 - math.pow(0.5, 1.0 / vida_media)


def baseline_ewma(valores, vida_media_centro=VIDA_MEDIA_CENTRO,
                   vida_media_spread=VIDA_MEDIA_SPREAD, floor_spread=1e-6,
                   min_val=None, max_val=None):
    """
    Baseline personal rodante: centro EWMA + spread EWMA de la desviación absoluta.

    Versión núcleo del modelo de NOOP (`Baselines.update`): media robusta ponderada por
    recencia + rastreador de dispersión. (La versión de producción añade winsorización y un
    arranque rápido del baseline joven; aquí dejamos el núcleo EWMA + el gate de cold-start,
    que es lo que `carga()` necesita. Se puede endurecer después.)

    `valores`: noches en orden cronológico (más antigua → más reciente). None/fuera de rango
    se saltan y no cuentan como noche válida.
    Devuelve {mean, spread, n_valid, usable, status} o None si no hay ninguna noche válida.
    """
    lb = _lambda(vida_media_centro)
    ls = _lambda(vida_media_spread)
    media = None
    spread = floor_spread
    n_valid = 0
    for v in valores:
        if v is None:
            continue
        if min_val is not None and v < min_val:
            continue
        if max_val is not None and v > max_val:
            continue
        n_valid += 1
        if media is None:
            media = v
            spread = floor_spread
            continue
        dev = abs(v - media)
        media = (1 - lb) * media + lb * v
        spread = max(floor_spread, (1 - ls) * spread + ls * dev)
    if n_valid == 0 or media is None:
        return None
    if n_valid < MIN_NOCHES_SEED:
        status = "calibrando"
    elif n_valid < MIN_NOCHES_TRUST:
        status = "provisional"
    else:
        status = "confiable"
    return {
        "mean": media,
        "spread": spread,
        "n_valid": n_valid,
        "usable": status in ("provisional", "confiable"),
        "status": status,
    }


# ------------------------------------------------------------------ logística + banda

def logistic_score(composite_z):
    """z compuesto → 0–100, recortado."""
    score = 100.0 / (1.0 + math.exp(-LOGISTIC_K * (composite_z - LOGISTIC_Z0)))
    return max(0.0, min(100.0, score))


def banda(score):
    if score <= BANDA_ROJO_MAX:
        return "rojo"
    if score <= BANDA_AMARILLO_MAX:
        return "amarillo"
    return "verde"


# ------------------------------------------------------------------ score de Carga

def carga(hrv, rhr, hrv_baseline,
          resp=None, rhr_baseline=None, resp_baseline=None,
          sueno_calidad=None, temp_piel_dev=None,
          recovery_index_slope=None,
          effort_dia_previo=None, effort_baseline=None):
    """
    Score de Carga/Recuperación en [0,100]. APROXIMADO. Devuelve un dict, o None en cold-start.

    Parámetros:
      hrv               HRV de esta noche (RMSSD, ms) — idealmente el gap-aware de hrv_rr.
      rhr               RHR de esta noche (lpm).
      hrv_baseline      baseline de HRV {mean, spread, usable} — REQUERIDO (None/no-usable → None).
      resp              respiración de la noche (cruda o calibrada; el z es invariante de escala).
      rhr_baseline      baseline de RHR; None cae el término.
      resp_baseline     baseline de respiración; None cae el término.
      sueno_calidad     calidad de descanso (0..1; compuesto de Rest ÷100). None cae el término.
      temp_piel_dev     desviación de temp de piel vs baseline (±°C). Penalización SIMÉTRICA.
      recovery_index_slope  pendiente de caída de RHR nocturna (bpm/hora). Negativo = bueno.
      effort_dia_previo / effort_baseline  Effort de ayer vs su baseline EWMA (ambos o ninguno).

    Nota: cada término es (valor − μ)/σ con el signo que hace "más alto = mejor recuperación".
    """
    # Gate de cold-start: HRV es el driver dominante; sin baseline usable, NO se puntúa
    # (más honesto que un valor fabricado).
    if hrv_baseline is None or not hrv_baseline.get("usable", False):
        return None

    terminos = []  # (nombre, z, w)

    # HRV: más alto es mejor. z crudo (el guard de saturación se detecta pero NO se aplica).
    z_hrv = z_robusto(hrv, hrv_baseline["mean"], hrv_baseline["spread"])
    terminos.append(("hrv", z_hrv, W_HRV))

    # RHR: más bajo es mejor → (μ − x)/σ.
    z_rhr = None
    if rhr_baseline is not None:
        z_rhr = z_robusto(rhr_baseline["mean"], rhr, rhr_baseline["spread"])
        terminos.append(("rhr", z_rhr, W_RHR))

    # Respiración: más baja es mejor, opcional.
    if resp is not None and resp_baseline is not None:
        terminos.append(("resp", z_robusto(resp_baseline["mean"], resp, resp_baseline["spread"]), W_RESP))

    # Sueño / calidad de descanso: sin baseline; centrado en SUENO_CENTRO.
    if sueno_calidad is not None:
        terminos.append(("sueno", (sueno_calidad - SUENO_CENTRO) / SUENO_ESCALA, W_SLEEP))

    # Temp de piel: penalización SIMÉTRICA sobre |desviación| (enfermedad/sobrecarga).
    if temp_piel_dev is not None:
        terminos.append(("temp_piel", -abs(temp_piel_dev) / ESCALA_TEMP_PIEL_C, W_SKIN_TEMP))

    # Recovery Index: pendiente de caída de RHR nocturna. Negativo (cayendo) apoya la recuperación.
    if recovery_index_slope is not None:
        terminos.append(("recovery_index", -recovery_index_slope / ESCALA_RECOVERY_INDEX_BPM_H, W_RECOVERY_INDEX))

    # Activity Balance: Effort de ayer más bajo vs baseline es mejor → (μ − x)/σ. Necesita ambos.
    if effort_dia_previo is not None and effort_baseline is not None:
        terminos.append(("activity_balance",
                         z_robusto(effort_baseline["mean"], effort_dia_previo, effort_baseline["spread"]),
                         W_ACTIVITY_BALANCE))

    if not terminos:
        return None
    peso_total = sum(w for _, _, w in terminos)
    if peso_total <= 0:
        return None

    z = sum(zt * w for _, zt, w in terminos) / peso_total
    score = logistic_score(z)

    # Guard de saturación parasimpática: DETECTADO Y REPORTADO, NO APLICADO (igual que NOOP).
    # Firma candidata: término HRV "malo" (z<0) mientras el término RHR es "bueno" (z>0) → el
    # acoplamiento esperado HRV↔RHR se rompió. No se corrige el score (ver dossier: validation
    # gap + premisa en disputa con el sobre-entrenamiento parasimpático).
    saturacion = (z_rhr is not None) and (z_hrv < 0) and (z_rhr > 0)

    return {
        "score": round(score, 2),
        "banda": banda(score),
        "composite_z": round(z, 4),
        "terminos": [{"nombre": n, "z": round(zt, 4), "w": w} for n, zt, w in terminos],
        "peso_total": round(peso_total, 3),
        "saturacion_parasimpatica_detectada": saturacion,
        "aprox": True,
        "fuente": "Carga (z-score + logística, HRV-dominante) · APROXIMADO, no es el score de WHOOP ni diagnóstico",
    }


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    # 1) Todo EN baseline → z=0 por término → score ≈ 58 (media poblacional WHOOP).
    base_hrv = {"mean": 60.0, "spread": 8.0, "usable": True, "status": "confiable"}
    base_rhr = {"mean": 52.0, "spread": 3.0, "usable": True, "status": "confiable"}
    r0 = carga(hrv=60.0, rhr=52.0, hrv_baseline=base_hrv, rhr_baseline=base_rhr,
               resp=14.0, resp_baseline={"mean": 14.0, "spread": 1.0, "usable": True},
               sueno_calidad=0.85)
    print("En baseline:      ", r0["score"], r0["banda"], "(z=%.3f)" % r0["composite_z"])
    assert 57.0 <= r0["score"] <= 59.0, "z=0 debe mapear ≈ 58%"

    # 2) Noche buena: HRV alta, RHR baja, buen sueño → verde.
    r1 = carga(hrv=84.0, rhr=46.0, hrv_baseline=base_hrv, rhr_baseline=base_rhr,
               sueno_calidad=0.95)
    print("Noche buena:      ", r1["score"], r1["banda"])
    assert r1["score"] > r0["score"] and r1["banda"] == "verde"

    # 3) Noche mala: HRV baja + RHR alta + sueño pobre + temp elevada → rojo/amarillo bajo.
    r2 = carga(hrv=38.0, rhr=60.0, hrv_baseline=base_hrv, rhr_baseline=base_rhr,
               sueno_calidad=0.70, temp_piel_dev=1.5)
    print("Noche mala:       ", r2["score"], r2["banda"])
    assert r2["score"] < r0["score"]

    # 4) Cold-start: baseline de HRV no usable → None (no inventa).
    base_cal = {"mean": 60.0, "spread": 8.0, "usable": False, "status": "calibrando"}
    assert carga(hrv=60.0, rhr=52.0, hrv_baseline=base_cal, rhr_baseline=base_rhr) is None
    print("Cold-start:        None (correcto, no inventa)")

    # 5) Renormalización: sin términos opcionales el score usa sólo los pesos presentes.
    r_solo = carga(hrv=84.0, rhr=46.0, hrv_baseline=base_hrv, rhr_baseline=base_rhr)
    assert abs(r_solo["peso_total"] - (W_HRV + W_RHR)) < 1e-9
    print("Sólo HRV+RHR:     ", r_solo["score"], "peso_total=", r_solo["peso_total"])

    # 6) Baseline EWMA + gate de usable.
    b = baseline_ewma([58, 61, 59, 62, 60, 63, 59, 60, 61, 62, 60, 59, 61, 60])
    print("Baseline HRV:     ", round(b["mean"], 2), "spread", round(b["spread"], 2),
          b["status"], "usable" if b["usable"] else "no-usable")
    assert b["usable"] and b["status"] == "confiable" and b["n_valid"] == 14
    assert baseline_ewma([60, 61, 59])["status"] == "calibrando"  # 3 noches < seed
    assert baseline_ewma([60, 61, 59])["usable"] is False

    # 7) Detección (no aplicación) de saturación parasimpática: HRV baja + RHR baja.
    r_sat = carga(hrv=40.0, rhr=44.0, hrv_baseline=base_hrv, rhr_baseline=base_rhr)
    assert r_sat["saturacion_parasimpatica_detectada"] is True
    print("Saturación:        detectada (no aplicada) ->", r_sat["score"], r_sat["banda"])

    print("\nOK — score de Carga funcional (pesos 55/20/15/5/5, logística k=1.6 z0=-0.2).")
