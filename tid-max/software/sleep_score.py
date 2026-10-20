#!/usr/bin/env python3
"""
sleep_score.py — Score de DESCANSO (0–100) + deuda de sueño, sobre datos de sueño.

Port fiel del compuesto Rest de NOOP (`AnalyticsEngine.Rest.composite`) y de `SleepDebt`
(código abierto, PolyForm Noncommercial; ver dossier `analisis/noop-ipa-teardown.md`).
Es APROXIMADO — no reproduce el score propietario de WHOOP; es un compuesto transparente.

Descanso = media ponderada de 4 términos (pesos que suman 1), escalada a 0–100:
    duración (necesidad de sueño, ratio)  W_DURATION    = 0.50  (dominante)
    eficiencia                            W_EFFICIENCY  = 0.20
    reparador (profundo+REM)              W_RESTORATIVE = 0.20
    consistencia de horario               W_CONSISTENCY = 0.10

La validación N-of-1 con datos reales de Carlos confirma el orden: necesidad↔Descanso +0.82
(driver dominante), tiempo dormido +0.78, tiempo en cama +0.76, consistencia +0.51.

Necesidad de sueño PERSONALIZADA con honestidad de cold-start: se ancla al objetivo
poblacional por edad (piso) y solo sube para dormilones genuinos (cuartil-75 de las noches),
nunca por debajo del objetivo; <7 noches → default poblacional (no se aprende de pocas noches).

Deuda de sueño: estimación ponderada por recencia sobre 14 noches; el 55% de la necesidad no
cubierta se arrastra a la noche siguiente; déficits < 10 min se limpian (no accionables).

Sin dependencias externas (sólo stdlib), igual que el resto del motor.
"""

# ------------------------------------------------------------------ constantes Rest (NOOP)

DEFAULT_NEED_HOURS = 8.0
RESTORATIVE_TARGET = 0.50     # share profundo+REM / dormido para "nota completa"
DEEP_SHARE_TARGET = 0.13      # share de profundo que da crédito reparador pleno (~13% adulto)
DEEP_FLOOR_FACTOR = 0.5       # lo más que se escala a la baja el reparador si falta profundo
NEUTRAL_CONSISTENCY = 0.5     # consistencia neutra si no hay señal de regularidad

W_DURATION = 0.50
W_EFFICIENCY = 0.20
W_RESTORATIVE = 0.20
W_CONSISTENCY = 0.10

MIN_NEED_NIGHTS = 7           # noches mínimas antes de confiar una necesidad personal
MAX_NEED_HOURS = 9.5          # tope de necesidad personalizada

# ------------------------------------------------------------------ constantes SleepDebt (NOOP)

DEBT_WINDOW_NIGHTS = 14
DEBT_CARRY_FACTOR = 0.55      # share de la necesidad no cubierta que se arrastra
DEBT_MIN_MIN = 10.0           # deuda menor a esto se considera no accionable → 0


def _clamp01(x):
    return max(0.0, min(1.0, x))


# ------------------------------------------------------------------ necesidad de sueño

def piso_necesidad_poblacional_h(edad=None):
    """Objetivo poblacional de sueño (h) por edad (midpoint rango NSF/AASM). Piso, no mínimo."""
    if edad is None or edad <= 0:
        return 8.0
    if edad < 18:
        return 9.0   # niños/adolescentes necesitan más
    return 8.0       # adultos y mayores: objetivo ~8h


def necesidad_personalizada_h(horas_por_noche, edad=None):
    """
    Necesidad nocturna personalizada, anclada a la población y con piso por edad.
    El componente personal es el **cuartil 75** de la duración (las noches menos restringidas),
    NO la media (que un déficit crónico arrastra a la baja). Solo ajusta HACIA ARRIBA.
    <MIN_NEED_NIGHTS noches escrutables → default poblacional (cold-start honesto).
    """
    piso = piso_necesidad_poblacional_h(edad)
    xs = sorted(h for h in horas_por_noche if h is not None and h > 0)
    if len(xs) < MIN_NEED_NIGHTS:
        return min(max(DEFAULT_NEED_HOURS, piso), MAX_NEED_HOURS)
    pos = 0.75 * (len(xs) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    q = xs[lo] + (pos - lo) * (xs[hi] - xs[lo])
    return min(max(q, piso), MAX_NEED_HOURS)


# ------------------------------------------------------------------ compuesto de Descanso

def descanso(tst_s, in_bed_s, efficiency, restorative_s, need_hours,
             consistency=None, deep_s=None):
    """
    Compuesto de Descanso en [0,100]. APROXIMADO.
      tst_s          tiempo total dormido (segundos)
      in_bed_s       tiempo en cama (segundos) — no entra en el compuesto directamente,
                     pero se conserva por paridad con NOOP / para diagnósticos
      efficiency     eficiencia de sueño 0..1
      restorative_s  profundo+REM (segundos)
      need_hours     necesidad de sueño (h)
      consistency    0..1 regularidad de horario (None → neutra 0.5)
      deep_s         profundo (segundos); None → sin ajuste de adecuación profunda
    """
    need_s = max(need_hours, 0.1) * 3600.0
    duration_score = _clamp01(tst_s / need_s)
    efficiency_score = _clamp01(efficiency)

    # Factor de adecuación de profundo en [DEEP_FLOOR_FACTOR, 1]; nil deep → 1.0 (sin ajuste).
    if deep_s is not None and tst_s > 0 and DEEP_SHARE_TARGET > 0:
        adequacy = _clamp01((deep_s / tst_s) / DEEP_SHARE_TARGET)
        deep_factor = DEEP_FLOOR_FACTOR + (1.0 - DEEP_FLOOR_FACTOR) * adequacy
    else:
        deep_factor = 1.0

    restorative_score = (_clamp01((restorative_s / tst_s) / RESTORATIVE_TARGET) * deep_factor
                         if tst_s > 0 else 0.0)
    consistency_score = _clamp01(consistency if consistency is not None else NEUTRAL_CONSISTENCY)

    weighted = (W_DURATION * duration_score
                + W_EFFICIENCY * efficiency_score
                + W_RESTORATIVE * restorative_score
                + W_CONSISTENCY * consistency_score)
    score = round(weighted * 10000.0) / 100.0  # [0,1] → [0,100], 2 dp
    return {
        "score": score,
        "banda": "sólido" if score >= 70 else ("medio" if score >= 50 else "bajo"),
        "terminos": {
            "duracion": round(duration_score, 4),
            "eficiencia": round(efficiency_score, 4),
            "reparador": round(restorative_score, 4),
            "consistencia": round(consistency_score, 4),
            "deep_factor": round(deep_factor, 4),
        },
        "aprox": True,
        "fuente": "Descanso (compuesto 0.50/0.20/0.20/0.10) · APROXIMADO, no es el score de WHOOP",
    }


def descanso_de_noche(total_sleep_min, efficiency, need_hours=DEFAULT_NEED_HOURS,
                      deep_min=None, rem_min=None, consistency=None):
    """
    Conveniencia desde los totales de una noche (minutos). Devuelve None si no hay sueño,
    igual que NOOP (retener-no-inventar). `restorativo = profundo + REM`.
    """
    if not total_sleep_min or total_sleep_min <= 0 or efficiency is None:
        return None
    tst_s = total_sleep_min * 60.0
    deep_s = (deep_min or 0) * 60.0
    restorative_s = ((deep_min or 0) + (rem_min or 0)) * 60.0
    in_bed_s = tst_s / max(efficiency, 0.01)
    return descanso(tst_s, in_bed_s, efficiency, restorative_s, need_hours,
                    consistency=consistency, deep_s=(deep_s if deep_min is not None else None))


# ------------------------------------------------------------------ deuda de sueño

def deuda_sueno(series_total_min, need_hours=DEFAULT_NEED_HOURS, window=DEBT_WINDOW_NIGHTS):
    """
    Libro de deuda de sueño sobre la ventana final (14 noches). `series_total_min` es una lista
    cronológica de minutos dormidos por noche (None/<=0 se SALTAN, sin rellenar con cero).

    Recurrencia (port exacto de SleepDebt.ledger):
        deuda = 0
        por cada noche (ventana): deuda = 0.55 * max(0, necesidad + deuda - dormido)
                                  si deuda < 10 min → 0
        balance = -deuda  (negativo = deuda)

    Devuelve {balance_min, magnitud_min, es_deuda, need_min, n_noches, noches:[{dormido,delta}]}.
    """
    need_min = max(need_hours, 0.0) * 60.0
    cap = max(window, 1)
    usables = [m for m in series_total_min if m is not None and m > 0]
    ventana = usables[-cap:]

    noches = []
    deuda = 0.0
    for dormido in ventana:
        delta = dormido - need_min
        calc = DEBT_CARRY_FACTOR * max(0.0, need_min + deuda - dormido)
        deuda = 0.0 if calc < DEBT_MIN_MIN else calc
        noches.append({"dormido_min": round(dormido, 1), "delta_min": round(delta, 1)})
    balance = round(-deuda * 10.0) / 10.0
    return {
        "balance_min": balance,
        "magnitud_min": abs(balance),
        "es_deuda": balance < 0,
        "need_min": need_min,
        "n_noches": len(noches),
        "noches": noches,
    }


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    # 1) Noche de Carlos (anoche, dom 18 oct): 6h54 dormido, 84% efic, profundo 1h58, REM 1h52.
    r = descanso_de_noche(total_sleep_min=6 * 60 + 54, efficiency=0.84,
                          deep_min=118, rem_min=112, consistency=0.81)
    print("Descanso (noche real Carlos):", r["score"], r["banda"], r["terminos"])
    assert 70 <= r["score"] <= 90  # la app mostró Descanso 80%

    # 2) Noche perfecta: cumple necesidad, 95% efic, mucho reparador, consistente.
    rp = descanso_de_noche(total_sleep_min=8 * 60, efficiency=0.95,
                           deep_min=130, rem_min=120, consistency=0.95)
    print("Descanso (noche ideal):      ", rp["score"], rp["banda"])
    assert rp["score"] > r["score"] and rp["banda"] == "sólido"

    # 3) Sin sueño → None (no inventa).
    assert descanso_de_noche(total_sleep_min=0, efficiency=None) is None
    print("Sin sueño:                    None (correcto)")

    # 4) Necesidad personalizada: dormilón (cuartil-75 alto) sube; déficit crónico NO baja del piso.
    dormilon = [8.5, 9.0, 8.8, 9.2, 8.6, 9.1, 8.9, 9.0, 8.7, 9.3]
    assert necesidad_personalizada_h(dormilon, edad=18) > 9.0  # sube hacia su cuartil-75
    deficit = [5.5, 6.0, 5.8, 6.2, 5.6, 6.1, 5.9, 6.0]
    assert necesidad_personalizada_h(deficit, edad=16) == 9.0   # piso adolescente (<18) = 9h
    assert necesidad_personalizada_h(deficit, edad=18) == 8.0   # 18 = adulto → piso 8h, no baja al déficit
    assert necesidad_personalizada_h([7, 8, 6], edad=30) == 8.0  # <7 noches → default/piso adulto
    print("Necesidad personalizada:      dormilón↑, déficit anclado al piso ✓")

    # 5) Deuda de sueño: 14 noches con ~1h de déficit medio (necesidad 8h).
    noches14 = [7 * 60] * 7 + [6 * 60 + 30] * 7  # mezcla de 7h y 6h30
    d = deuda_sueno(noches14, need_hours=8.0)
    print("Deuda de sueño:               ", d["magnitud_min"], "min · es_deuda=", d["es_deuda"],
          "· noches=", d["n_noches"])
    assert d["es_deuda"] and d["magnitud_min"] > 10 and d["n_noches"] == 14
    # Noche que cumple la necesidad limpia la deuda mostrada.
    d2 = deuda_sueno([8 * 60] * 14, need_hours=8.0)
    assert d2["magnitud_min"] == 0.0 and not d2["es_deuda"]
    print("Deuda tras cumplir necesidad:  0 (limpia) ✓")

    print("\nOK — score de Descanso + deuda de sueño funcional (0.50/0.20/0.20/0.10, deuda 14n/0.55).")
