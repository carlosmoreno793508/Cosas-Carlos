#!/usr/bin/env python3
"""
strain_score.py — Score de ESFUERZO (0–100 logarítmico) + carga de entrenamiento (ACWR).

Port fiel de `StrainScorer` y `TrainingLoadEngine` de NOOP (código abierto, PolyForm
Noncommercial; ver dossier `analisis/noop-ipa-teardown.md`). Implementación INDEPENDIENTE de
métodos publicados de fisiología del ejercicio (WHOOP-*like*, no reproducción del algoritmo
propietario; no es consejo médico). APROXIMADO.

Pipeline de Esfuerzo:
  1. Reserva de FC (Karvonen): HRR = FCmáx − RHR. FCmáx = Tanaka 208 − 0.7·edad (o percentil
     99.5 observado si hay ≥600 muestras).
  2. Intensidad por muestra %HRR = (FC − RHR)/HRR · 100, recortada 0..100.
  3. TRIMP acumulado en la ventana:
       a. Edwards 5 zonas (default): peso de zona (1..5 en cortes 50/60/70/80/90 %HRR) × duración.
       b. Banister exponencial (opcional): dur · x · 0.64 · e^(b·x), con línea base sedentaria.
  4. Compresión log a [0,100]: strain = 100 · ln(TRIMP+1)/ln(D). D pertenece al MÉTODO:
     Edwards D=7201 (techo 7200 = zona 5 sostenida 24h); Banister su propio techo sexo-dependiente.

Clave de diseño (confirmada con datos reales de Carlos: Esfuerzo↔calorías +0.82, FC +0.66/+0.60):
  - Edwards no cuenta nada bajo 50% HRR → **una hora de pesas marca ~0** (el volumen de fuerza
    NO toca el Esfuerzo basado en HR; vive en su propio carril).
  - La escala se calcula una vez y se re-escala a la vista (0-100 ↔ 0-21 Day Strain de WHOOP).

Carga de entrenamiento (ACWR / fitness-fatigue, Banister):
  alpha = 1 − e^(−1/tau); estado[t] = estado[t−1] + alpha·(carga[t] − estado[t−1])
  CTL (crónica) tau=42d, ATL (aguda) tau=7d, TSB = CTL − ATL, ACWR = ATL/CTL.
  Prime: primeras 7 obs promediadas para sembrar. Días faltantes NUNCA se rellenan con 0
  (un día de descanso real es una fila con carga 0; nil rompe la contigüidad). Necesita ≥14
  días contiguos para empezar.

Sin dependencias externas (sólo stdlib `math`).
"""
import math

# ------------------------------------------------------------------ constantes StrainScorer (NOOP)

MAX_STRAIN = 100.0            # techo del eje Esfuerzo (re-escalado 21→100; la curva no cambia)
WHOOP_MAX_STRAIN = 21.0       # eje Day Strain de WHOOP
STRAIN_DENOMINATOR = 7201.0   # D Edwards: ln(7201)/ln(7201)=1 (zona 5 · 24h = 7200)

DEFAULT_AGE = 30
DEFAULT_RESTING_HR = 60.0
HRMAX_MIN_SAMPLES = 600
HRMAX_PERCENTILE = 99.5

BANISTER_SCALE = 0.64
BANISTER_B_MEN = 1.92
BANISTER_B_WOMEN = 1.67
BANISTER_SEDENTARY_HRR = 0.10  # "costo de estar vivo" (la única constante afinada)

MAX_SAMPLE_GAP_MIN = 2.0       # tope de duración por muestra (evita inventar esfuerzo en huecos)
FALLBACK_SAMPLE_MIN = 1.0 / 60.0

# Zonas Edwards (umbral %HRR, peso), de mayor a menor.
EDWARDS_ZONES = [(90.0, 5), (80.0, 4), (70.0, 3), (60.0, 2), (50.0, 1)]


# ------------------------------------------------------------------ FCmáx / Karvonen

def tanaka_hrmax(edad):
    """Tanaka 2001: FCmáx = 208 − 0.7·edad (independiente del sexo)."""
    return 208.0 - 0.7 * edad


def _percentil(ordenados, pct):
    n = len(ordenados)
    if n == 0:
        return 0.0
    if n == 1:
        return ordenados[0]
    pos = (pct / 100.0) * (n - 1)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return ordenados[lo] + frac * (ordenados[hi] - ordenados[lo])


def estima_hrmax(hr_history, edad=None):
    """(FCmáx, fuente) donde fuente ∈ {observed, tanaka, unknown}."""
    tanaka = tanaka_hrmax(edad) if edad is not None else None
    if len(hr_history) >= HRMAX_MIN_SAMPLES:
        observed = _percentil(sorted(hr_history), HRMAX_PERCENTILE)
        if tanaka is None:
            return observed, "observed"
        return (observed, "observed") if observed >= tanaka else (tanaka, "tanaka")
    if tanaka is not None:
        return tanaka, "tanaka"
    return 0.0, "unknown"


def _pct_hrr(bpm, rhr, hrr):
    pct = (bpm - rhr) / hrr * 100.0
    return 0.0 if pct < 0 else (100.0 if pct > 100 else pct)


def _zone_weight(bpm, rhr, hrr):
    pct = (bpm - rhr) / hrr * 100.0
    for threshold, weight in EDWARDS_ZONES:
        if pct >= threshold:
            return weight
    return 0


# ------------------------------------------------------------------ duraciones + TRIMP

def _duraciones_min(ts_list):
    """Minutos por muestra: cada lectura cubre el hueco a la SIGUIENTE, recortado a 2 min;
    la última reusa el hueco previo. Fallback 1 s si no hay timestamps útiles."""
    n = len(ts_list)
    if n == 0:
        return []
    if n == 1:
        return [FALLBACK_SAMPLE_MIN]
    out = []
    for i in range(n - 1):
        delta_s = abs(ts_list[i + 1] - ts_list[i])
        minutes = delta_s / 60.0 if delta_s > 0 else FALLBACK_SAMPLE_MIN
        out.append(min(minutes, MAX_SAMPLE_GAP_MIN))
    out.append(out[-1])
    return out


def edwards_trimp(bpms, rhr, hrr, duraciones):
    return sum(_zone_weight(b, rhr, hrr) * d for b, d in zip(bpms, duraciones))


def zone_minutes(bpms, rhr, hrr, duraciones):
    """Minutos en cada zona Edwards, indexados por peso: [0]=bajo zona 1, [1..5]=zonas 1-5."""
    out = [0.0] * 6
    for b, d in zip(bpms, duraciones):
        out[_zone_weight(b, rhr, hrr)] += d
    return out


def _banister_b(sexo):
    return BANISTER_B_WOMEN if str(sexo).lower().startswith("f") else BANISTER_B_MEN


def _banister_floor_rate(b):
    return BANISTER_SCALE * BANISTER_SEDENTARY_HRR * math.exp(b * BANISTER_SEDENTARY_HRR)


def banister_trimp(bpms, rhr, hrr, duraciones, b, floor_rate=0.0):
    """Banister exponencial. `floor_rate` (TRIMP/min sedentario) se resta por muestra, floor 0."""
    acc = 0.0
    for bpm, d in zip(bpms, duraciones):
        x = _pct_hrr(bpm, rhr, hrr) / 100.0
        raw = d * x * BANISTER_SCALE * math.exp(b * x)
        acc += max(0.0, raw - floor_rate * d)
    return acc


def _log_map_denominator(metodo, sexo):
    if metodo == "edwards":
        return STRAIN_DENOMINATOR
    b = _banister_b(sexo)
    ceiling = 24.0 * 60.0 * 1.0 * BANISTER_SCALE * math.exp(b)
    baseline = _banister_floor_rate(b) * (24.0 * 60.0)
    return ceiling - baseline + 1.0


# ------------------------------------------------------------------ score de Esfuerzo

def esfuerzo(hr_samples, edad=DEFAULT_AGE, rhr=DEFAULT_RESTING_HR, sexo="m",
             metodo="edwards", hr_history=None):
    """
    Score de Esfuerzo 0–100. APROXIMADO.
      hr_samples   lista de (ts_segundos, bpm) en orden cronológico.
      metodo       "edwards" (default) o "banister".
    Devuelve dict, o None si no hay HRR válida / sin muestras.
    """
    if not hr_samples:
        return None
    ts_list = [s[0] for s in hr_samples]
    bpms = [float(s[1]) for s in hr_samples]

    hrmax, fuente_hrmax = estima_hrmax(hr_history if hr_history is not None else bpms, edad)
    hrr = hrmax - rhr
    if hrr <= 0:
        return None  # HRR no válida → no se puntúa (no inventa)

    duraciones = _duraciones_min(ts_list)

    if metodo == "banister":
        b = _banister_b(sexo)
        floor_rate = _banister_floor_rate(b)
        trimp = banister_trimp(bpms, rhr, hrr, duraciones, b, floor_rate=floor_rate)
    else:
        metodo = "edwards"
        trimp = edwards_trimp(bpms, rhr, hrr, duraciones)

    D = _log_map_denominator(metodo, sexo)
    strain = 100.0 * math.log(trimp + 1.0) / math.log(D)
    strain = max(0.0, min(MAX_STRAIN, strain))

    return {
        "esfuerzo": round(strain, 2),
        "esfuerzo_0_21": round(strain * (WHOOP_MAX_STRAIN / MAX_STRAIN), 2),
        "trimp": round(trimp, 1),
        "metodo": metodo,
        "hrmax": round(hrmax, 1),
        "hrmax_fuente": fuente_hrmax,
        "hrr": round(hrr, 1),
        "zonas_min": [round(z, 1) for z in zone_minutes(bpms, rhr, hrr, duraciones)],
        "aprox": True,
        "fuente": "Esfuerzo (Karvonen→TRIMP→log) · APROXIMADO, no es el Day Strain de WHOOP",
    }


def esfuerzo_efectivo(live, stored):
    """La cifra de Esfuerzo que SIEMPRE muestra Hoy: max(live, stored) para que nunca BAJE
    visiblemente (el recompute en vivo puede sub-leer con HR escaso). None si ambos None."""
    if live is None:
        return stored
    if stored is None:
        return live
    if live == 0.0 and stored == 0.0:
        return 0.0
    return max(live, stored)


# ------------------------------------------------------------------ carga de entrenamiento (ACWR)

CTL_TAU_DAYS = 42.0
ATL_TAU_DAYS = 7.0
PRIME_DAYS = 7
MIN_DAYS = 14
ESTABLISHED_DAYS = 42


def _contiguous_suffix(daily_loads):
    """Sufijo contiguo final con carga no-None (días faltantes/None rompen la contigüidad)."""
    run = []
    for day, load in daily_loads:
        if load is None:
            run = []
        else:
            run.append((day, float(load)))
    return run


def carga_entrenamiento(daily_loads, chronic_tau=CTL_TAU_DAYS, acute_tau=ATL_TAU_DAYS,
                        prime_days=PRIME_DAYS, min_days=MIN_DAYS, established_days=ESTABLISHED_DAYS):
    """
    Modelo fitness-fatigue EWMA sobre carga diaria (Esfuerzo). `daily_loads` = lista cronológica
    de (dia, carga|None); carga 0 = descanso medido, None = sin observación (rompe contigüidad).

    Devuelve {estado, ctl, atl, tsb, acwr, n_contiguos, puntos:[...]} o estado 'no_disponible'.
    Estados: no_disponible (<14 contiguos) · construyendo (<42) · establecido (≥42).
    """
    run = _contiguous_suffix(daily_loads)
    n = len(run)
    if n < prime_days:
        return {"estado": "no_disponible", "razon": "pocos_dias_contiguos",
                "n_contiguos": n, "ctl": None, "atl": None, "tsb": None, "acwr": None,
                "puntos": []}

    alpha_c = 1.0 - math.exp(-1.0 / chronic_tau)
    alpha_a = 1.0 - math.exp(-1.0 / acute_tau)
    seed = sum(load for _, load in run[:prime_days]) / prime_days
    ctl = seed
    atl = seed
    puntos = []
    for i, (day, load) in enumerate(run):
        if i == 0:
            ctl = seed
            atl = seed
        else:
            ctl = ctl + alpha_c * (load - ctl)
            atl = atl + alpha_a * (load - atl)
        if i >= prime_days - 1:  # puntos definidos desde el final del priming
            puntos.append({"dia": day, "carga": round(load, 2),
                           "ctl": round(ctl, 2), "atl": round(atl, 2),
                           "tsb": round(ctl - atl, 2)})

    if n >= established_days:
        estado = "establecido"
    elif n >= min_days:
        estado = "construyendo"
    else:
        estado = "no_disponible"

    ultimo = puntos[-1] if puntos else {}
    acwr = (round(ultimo["atl"] / ultimo["ctl"], 2)
            if ultimo and ultimo["ctl"] > 0 else None)
    return {
        "estado": estado,
        "n_contiguos": n,
        "ctl": ultimo.get("ctl"),
        "atl": ultimo.get("atl"),
        "tsb": ultimo.get("tsb"),
        "acwr": acwr,          # aguda/crónica: ~0.8–1.3 zona sana; >1.5 riesgo
        "puntos": puntos,
        "fuente": "Carga de entrenamiento (EWMA CTL42/ATL7, fitness-fatigue) · APROXIMADO",
    }


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    # Sintético: 20 min de carrera firme (~80% HRR) a 1 Hz, edad 18, RHR 50.
    edad, rhr = 18, 50.0
    hrmax = tanaka_hrmax(edad)                    # 195.4
    hrr = hrmax - rhr                             # 145.4
    objetivo = rhr + 0.80 * hrr                   # ~166 bpm (zona 4)
    t0 = 1_700_000_000
    run = [(t0 + i, objetivo) for i in range(20 * 60)]  # 20 min @1Hz
    r = esfuerzo(run, edad=edad, rhr=rhr)
    print("Esfuerzo (20min @80%HRR):", r["esfuerzo"], "/100 ·", r["esfuerzo_0_21"], "/21 ·",
          "TRIMP", r["trimp"], "·", r["metodo"])
    assert r is not None and 0 < r["esfuerzo"] < 100
    assert abs(r["esfuerzo_0_21"] - r["esfuerzo"] * 21 / 100) < 0.05  # re-escala consistente

    # Pesas: FC baja (~45% HRR, zona 1) una hora → Edwards marca casi nada.
    bajo = rhr + 0.45 * hrr
    pesas = [(t0 + i, bajo) for i in range(60 * 60)]
    rp = esfuerzo(pesas, edad=edad, rhr=rhr)
    print("Esfuerzo (1h pesas ~45%HRR):", rp["esfuerzo"], "/100 (Edwards ignora <50% HRR)")
    assert rp["esfuerzo"] < 5.0   # el volumen de fuerza no infla el Esfuerzo HR

    # Banister SÍ cuenta la intensidad sub-umbral.
    rb = esfuerzo(pesas, edad=edad, rhr=rhr, metodo="banister")
    print("Esfuerzo (misma hora, Banister):", rb["esfuerzo"], "/100 (sí cuenta sub-umbral)")
    assert rb["esfuerzo"] > rp["esfuerzo"]

    # HRR inválida → None (no inventa).
    assert esfuerzo([(t0, 60)], edad=18, rhr=200.0) is None

    # esfuerzo_efectivo = max (nunca baja visiblemente).
    assert esfuerzo_efectivo(2.3, 38.3) == 38.3 and esfuerzo_efectivo(None, 10.0) == 10.0

    # Carga de entrenamiento (ACWR): 50 días de carga ~50 → establecido, ACWR ~1.0.
    dias = [(f"2026-09-{i:02d}" if i <= 30 else f"2026-10-{i-30:02d}", 50.0) for i in range(1, 51)]
    ct = carga_entrenamiento(dias)
    print("Carga entrenamiento:", ct["estado"], "· CTL", ct["ctl"], "· ATL", ct["atl"],
          "· TSB", ct["tsb"], "· ACWR", ct["acwr"])
    assert ct["estado"] == "establecido" and 0.9 <= ct["acwr"] <= 1.1
    # <14 días → no disponible (como la UI: "necesita 14+ días").
    assert carga_entrenamiento([("2026-10-01", 40.0)] * 10)["estado"] == "no_disponible"
    # None rompe la contigüidad (día faltante ≠ descanso 0).
    rota = [("2026-10-01", 50.0), ("2026-10-02", None)] + [(f"2026-10-{i:02d}", 50.0) for i in range(3, 18)]
    assert carga_entrenamiento(rota)["n_contiguos"] == 15

    print("\nOK — score de Esfuerzo (Edwards/Banister, D=7201) + ACWR (CTL42/ATL7) funcional.")
