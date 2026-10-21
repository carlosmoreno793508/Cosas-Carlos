#!/usr/bin/env python3
"""
valida_motor.py — Validación numérica del motor contra una referencia INDEPENDIENTE,
con la MISMA metodología que los *agreement tests* de NOOP (ryanbr/noop, estudio técnico):

  • HRV  (≙ HrvGoldAgreementTest): RMSSD / SDNN / pNN50 vs una referencia textbook
    Task Force (1996) / neurokit2 reimplementada aquí DESDE CERO (no reusa `hrv_rr`) →
    debe coincidir a 1e-9. Prueba que nuestra matemática de HVC es correcta, independiente
    de cualquier etiqueta de WHOOP.
  • Carga (≙ RecoveryAgreementTest): el composite z-score + logística vs una
    reimplementación INDEPENDIENTE de la misma fórmula (pesos/constantes de
    `recovery_score`) → coincide a la precisión de presentación (0.01), PINEANDO las 11
    constantes (pesos, K/Z0 de la logística, centro/escala de sueño, escala de temp de piel,
    el factor 1.253 del spread) y la semántica de nulos (cold-start, renormalización).

Las fixtures "gold" de NOOP son datos de investigación locales (NO se publican; sus propios
tests hacen SKIP si faltan). Igual que ellos, generamos series/casos propios y comparamos
contra la referencia independiente: esto valida CORRECCIÓN DE FÓRMULA, no un ajuste a un número
mágico. Confirmado además por lectura directa del fuente de NOOP (HrvAnalyzer.rmssdRaw/sdnnRaw/
pnn50GapAware y RecoveryScorer.recovery/logisticScore): misma fórmula y mismas constantes.

Sin dependencias externas (sólo stdlib). Autoprueba por `__main__`.
"""
import math
import random

import hrv_rr
import recovery_score as rs

TOL = 1e-9


# ------------------------------------------------ referencia HRV independiente (Task Force 1996)

def ref_rmssd(nn):
    """RMSSD = raíz de la media de las diferencias sucesivas al cuadrado (÷ nº de diferencias)."""
    if len(nn) < 2:
        return None
    d = [nn[i] - nn[i - 1] for i in range(1, len(nn))]
    return math.sqrt(sum(x * x for x in d) / len(d))


def ref_sdnn(nn):
    """SDNN = desviación estándar MUESTRAL de los NN (ddof=1, ÷(n−1); = neurokit2 HRV_SDNN)."""
    if len(nn) < 2:
        return None
    m = sum(nn) / len(nn)
    return math.sqrt(sum((x - m) ** 2 for x in nn) / (len(nn) - 1))


def ref_pnn50(nn):
    """pNN50 = % de diferencias sucesivas con |Δ| > 50 ms."""
    if len(nn) < 2:
        return None
    d = [abs(nn[i] - nn[i - 1]) for i in range(1, len(nn))]
    return 100.0 * sum(1 for x in d if x > 50.0) / len(d)


def gen_nn(n, base, sd, seed):
    """Serie NN limpia sintética (ms), fisiológica, acotada."""
    r = random.Random(seed)
    return [max(300.0, min(2000.0, base + r.gauss(0, sd))) for _ in range(n)]


# ------------------------------------------------ referencia Carga independiente (z + logística)

def _zr(v, mean, spread):
    return (v - mean) / max(1.253 * spread, 1e-9)


def ref_carga(hrv, rhr, hb, resp=None, rb=None, respb=None,
              sueno=None, tdev=None, ris=None, eff=None, effb=None):
    """Reimplementación independiente del composite de Carga (mismos pesos/constantes/signos)."""
    if hb is None or not hb.get("usable", False):
        return None
    T = [(_zr(hrv, hb["mean"], hb["spread"]), 0.55)]            # HVC: más alto mejor
    if rb is not None:
        T.append((_zr(rb["mean"], rhr, rb["spread"]), 0.20))    # FC reposo: más bajo mejor
    if resp is not None and respb is not None:
        T.append((_zr(respb["mean"], resp, respb["spread"]), 0.05))
    if sueno is not None:
        T.append(((sueno - 0.85) / 0.12, 0.15))
    if tdev is not None:
        T.append((-abs(tdev) / 1.0, 0.05))                      # penalización simétrica
    if ris is not None:
        T.append((-ris / 2.0, 0.05))
    if eff is not None and effb is not None:
        T.append((_zr(effb["mean"], eff, effb["spread"]), 0.05))
    if not T:
        return None
    w = sum(x for _, x in T)
    if w <= 0:
        return None
    z = sum(zt * wt for zt, wt in T) / w
    s = 100.0 / (1.0 + math.exp(-1.6 * (z - (-0.20))))
    return max(0.0, min(100.0, s))


def bl(m, s, usable=True):
    return {"mean": m, "spread": s, "usable": usable}


# ------------------------------------------------ autoprueba

if __name__ == "__main__":
    # --- 1) HVC: primitivas (rmssd/sdnn/pnn50) vs referencia textbook, a 1e-9 ---
    maxR = maxS = maxP = 0.0
    series = [(300, 900, 40, 1), (250, 1050, 60, 2), (120, 800, 25, 3),
              (60, 1200, 90, 4), (40, 1000, 15, 5), (500, 950, 50, 6)]
    for n, base, sd, seed in series:
        nn = gen_nn(n, base, sd, seed)
        r1, s1, p1 = hrv_rr.rmssd(nn), hrv_rr.sdnn(nn), hrv_rr.pnn50(nn)
        r0, s0, p0 = ref_rmssd(nn), ref_sdnn(nn), ref_pnn50(nn)
        assert abs(r1 - r0) < TOL, f"RMSSD {r1} vs {r0}"
        assert abs(s1 - s0) < TOL, f"SDNN {s1} vs {s0}"
        assert abs(p1 - p0) < TOL, f"pNN50 {p1} vs {p0}"
        maxR, maxS, maxP = max(maxR, abs(r1 - r0)), max(maxS, abs(s1 - s0)), max(maxP, abs(p1 - p0))
    print(f"[HVC] {len(series)} series · maxErr RMSSD={maxR:.1e} SDNN={maxS:.1e} pNN50={maxP:.1e}  ✓ (<{TOL:.0e})")

    # gap-aware coincide con el plano en una serie contigua (sin huecos)
    nn = gen_nn(200, 950, 45, 9)
    assert abs(hrv_rr.rmssd_gap([nn]) - hrv_rr.rmssd(nn)) < TOL
    assert abs(hrv_rr.pnn50_gap([nn]) - hrv_rr.pnn50(nn)) < TOL
    print("[HVC] gap-aware == plano en serie contigua ✓")

    # --- 2) Carga: composite vs referencia independiente + semántica de nulos ---
    hb, rb, respb, effb = bl(90, 12), bl(52, 4), bl(14, 1.2), bl(50, 10)
    casos = [
        dict(hrv=100, rhr=50, resp=13, rb=rb, respb=respb, sueno=0.9, tdev=0.2, ris=-1.0, eff=40, effb=effb),
        dict(hrv=70,  rhr=58, rb=rb),                              # caen los opcionales
        dict(hrv=90,  rhr=52),                                     # sólo HVC
        dict(hrv=120, rhr=48, rb=rb, respb=respb, resp=12, sueno=0.95),
        dict(hrv=60,  rhr=62, rb=rb, sueno=0.6, tdev=1.5),
        dict(hrv=85,  rhr=55, rb=rb, ris=0.8),                     # recovery index positivo
    ]
    maxC = 0.0
    for c in casos:
        got = rs.carga(c["hrv"], c["rhr"], hb, resp=c.get("resp"), rhr_baseline=c.get("rb"),
                       resp_baseline=c.get("respb"), sueno_calidad=c.get("sueno"),
                       temp_piel_dev=c.get("tdev"), recovery_index_slope=c.get("ris"),
                       effort_dia_previo=c.get("eff"), effort_baseline=c.get("effb"))
        ref = ref_carga(c["hrv"], c["rhr"], hb, resp=c.get("resp"), rb=c.get("rb"), respb=c.get("respb"),
                        sueno=c.get("sueno"), tdev=c.get("tdev"), ris=c.get("ris"),
                        eff=c.get("eff"), effb=c.get("effb"))
        assert got is not None and ref is not None
        d = abs(got["score"] - round(ref, 2))
        assert d < TOL, f"Carga {got['score']} vs {round(ref, 2)}"
        maxC = max(maxC, d)
    print(f"[Carga] {len(casos)} casos · coincide con la referencia a presentación (0.01), maxErr={maxC:.1e}  ✓")

    # cold-start honesto: baseline HVC no usable / None → None (no inventa)
    assert rs.carga(90, 52, bl(90, 12, usable=False)) is None
    assert rs.carga(90, 52, None) is None
    print("[Carga] cold-start (baseline HVC no usable / None) → None ✓")

    # renormalización de pesos al caer términos
    r_full = rs.carga(100, 50, hb, rhr_baseline=rb)
    assert abs(r_full["peso_total"] - (rs.W_HRV + rs.W_RHR)) < 1e-9
    print("[Carga] renormalización de pesos al caer términos ✓")

    print("\nOK — motor verificado contra referencia independiente (metodología agreement de NOOP, a 1e-9).")
