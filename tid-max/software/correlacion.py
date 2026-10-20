#!/usr/bin/env python3
"""
correlacion.py — Motor de correlación N-of-1 (el panel "qué se correlaciona").

Port de `CorrelationEngine` de NOOP (código abierto; ver dossier). Puro, determinista, sin
dependencias. Calcula la correlación de Pearson r entre dos series diarias, una recta OLS
(pendiente/intercepto de y sobre x) y un p-valor aproximado de dos colas.

  r = Σ(x−x̄)(y−ȳ) / sqrt( Σ(x−x̄)²·Σ(y−ȳ)² )          (Pearson)
  slope = Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²,  intercept = ȳ − slope·x̄   (OLS, y sobre x)
  t = r·sqrt((n−2)/(1−r²)) → p de dos colas por aprox NORMAL (2·(1−Φ(|t|)))

El p-valor es una aproximación (para n chico las colas t reales son más pesadas, así que
subestima ligeramente p), pero es determinista y sin tablas. Φ usa `math.erf`.

`alinea_por_dia` hace inner-join de dos series indexadas por día. `lagged` desplaza y en
`lag_dias` para probar efectos dirigidos/retardados (p. ej. esfuerzo de hoy vs recuperación de
mañana — la capa causal con lag por hallazgo).

`que_se_correlaciona` reproduce el panel de NOOP: correlaciona un score/métrica objetivo contra
varios candidatos, conserva los de **|r| ≥ 0.30 y n ≥ 10** y los ordena por |r| descendente.
Esto es N-of-1 (asociación con tu propio historial), NO causalidad ni diagnóstico.

Validado contra los datos reales de Carlos: en la app, Carga↔HRV +0.96, Carga↔RHR −0.79,
Descanso↔necesidad +0.82, Esfuerzo↔calorías +0.82.

Sólo stdlib (`math`, `datetime`).
"""
import math
from datetime import datetime, timedelta

# Umbrales del panel "qué se correlaciona" (de la UI de NOOP).
MIN_ABS_R = 0.30
MIN_N = 10


def pearson(xy):
    """
    Pearson r + recta OLS + p-valor aprox sobre los pares (x,y). Devuelve dict o None
    (<3 pares, o varianza cero en alguna variable → r indefinido).
    """
    n = len(xy)
    if n < 3:
        return None
    nd = float(n)
    sum_x = sum(p[0] for p in xy)
    sum_y = sum(p[1] for p in xy)
    mean_x = sum_x / nd
    mean_y = sum_y / nd
    sxx = syy = sxy = 0.0
    for x, y in xy:
        dx = x - mean_x
        dy = y - mean_y
        sxx += dx * dx
        syy += dy * dy
        sxy += dx * dy
    if sxx <= 0 or syy <= 0:
        return None
    r = sxy / (math.sqrt(sxx) * math.sqrt(syy))
    r = max(-1.0, min(1.0, r))  # recortar overshoot de punto flotante
    slope = sxy / sxx
    intercept = mean_y - slope * mean_x
    return {"r": round(r, 4), "n": n, "p": round(_p_value(r, n), 5),
            "slope": slope, "intercept": intercept}


def _p_value(r, n):
    """p de dos colas para H0: r=0, via t y aproximación normal."""
    if n <= 2:
        return 1.0
    one_minus_r2 = 1.0 - r * r
    if one_minus_r2 <= 0:
        return 0.0  # |r| == 1
    t = r * math.sqrt((n - 2) / one_minus_r2)
    return 2.0 * (1.0 - _normal_cdf(abs(t)))


def _normal_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


# ------------------------------------------------------------------ alineación por día + lag

def alinea_por_dia(a, b):
    """
    Inner-join de dos series [(dia, valor)] por la clave de día; devuelve pares (x,y) de los
    días presentes en AMBAS, orden ascendente por día. Último valor gana si hay día duplicado.
    """
    map_a = {}
    for dia, val in a:
        map_a[dia] = val
    map_b = {}
    for dia, val in b:
        map_b[dia] = val
    comunes = sorted(d for d in map_a if d in map_b)
    return [(map_a[d], map_b[d]) for d in comunes]


def _shift_day(dia, delta):
    try:
        d = datetime.strptime(dia, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None
    return (d + timedelta(days=delta)).strftime("%Y-%m-%d")


def lagged(x, y, lag_dias):
    """
    Correlaciona x[dia] contra y[dia + lag_dias]. Lag positivo = "¿x de hoy predice y en
    `lag_dias`?". Devuelve dict de pearson o None.
    """
    map_y = {dia: val for dia, val in y}
    pares = []
    for dia, val in sorted(x, key=lambda r: r[0]):
        shifted = _shift_day(dia, lag_dias)
        if shifted is not None and shifted in map_y:
            pares.append((val, map_y[shifted]))
    return pearson(pares)


# ------------------------------------------------------------------ panel "qué se correlaciona"

def que_se_correlaciona(objetivo, candidatos, min_abs_r=MIN_ABS_R, min_n=MIN_N):
    """
    El panel "qué se correlaciona" de un score/métrica objetivo.
      objetivo    serie [(dia, valor)] del score/métrica foco.
      candidatos  dict {nombre: serie [(dia, valor)]} de las demás métricas.
    Correlaciona cada candidato con el objetivo sobre los días comunes; conserva los de
    |r| ≥ min_abs_r y n ≥ min_n; ordena por |r| descendente.
    Devuelve lista de {nombre, r, n, p}.
    """
    salida = []
    for nombre, serie in candidatos.items():
        pares = alinea_por_dia(objetivo, serie)
        res = pearson(pares)
        if res is None:
            continue
        if abs(res["r"]) >= min_abs_r and res["n"] >= min_n:
            salida.append({"nombre": nombre, "r": res["r"], "n": res["n"], "p": res["p"]})
    salida.sort(key=lambda c: abs(c["r"]), reverse=True)
    return salida


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    import random
    random.seed(3)

    # Relación perfecta positiva.
    xy = [(float(i), 2.0 * i + 1.0) for i in range(12)]
    r = pearson(xy)
    print("Pearson lineal perfecto: r =", r["r"], "p =", r["p"], "slope =", round(r["slope"], 2))
    assert r["r"] == 1.0 and r["p"] == 0.0 and abs(r["slope"] - 2.0) < 1e-9

    # Sin relación (ruido) → |r| chico, p alto.
    ruido = [(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(40)]
    rn = pearson(ruido)
    print("Ruido: r =", rn["r"], "p =", rn["p"])
    assert abs(rn["r"]) < 0.4 and rn["p"] > 0.05

    # Varianza cero / pocos pares → None.
    assert pearson([(1.0, 5.0)] * 10) is None
    assert pearson([(1.0, 2.0), (2.0, 3.0)]) is None

    # Alineación por día + lag.
    hoy = [(f"2026-10-{i:02d}", i * 1.0) for i in range(1, 11)]
    man = [(f"2026-10-{i:02d}", i * 1.0) for i in range(2, 12)]  # misma serie +1 día
    lag = lagged(hoy, man, 1)   # x[D] vs y[D+1] = i vs (i+1)-ésimo... relación perfecta
    assert lag is not None and lag["r"] == 1.0
    print("Lag +1 día: r =", lag["r"], "n =", lag["n"])

    # Panel "qué se correlaciona": Carga sintética que sigue a HRV e inverso a RHR.
    dias = [f"2026-09-{i:02d}" for i in range(1, 29)]
    hrv = [(d, 80 + random.gauss(0, 10)) for d in dias]
    carga = [(d, 0.6 * v + random.gauss(0, 3)) for (d, v) in hrv]           # Carga sigue a HRV
    rhr = [(d, 60 - 0.1 * v + random.gauss(0, 1)) for (d, v) in hrv]        # RHR inverso a HRV
    azar = [(d, random.gauss(0, 1)) for d in dias]                          # sin relación
    panel = que_se_correlaciona(carga, {"HRV": hrv, "RHR": rhr, "Azar": azar})
    print("Panel qué-se-correlaciona con Carga:", [(c["nombre"], c["r"]) for c in panel])
    nombres = [c["nombre"] for c in panel]
    assert "HRV" in nombres and "RHR" in nombres                            # los reales salen
    assert panel[0]["nombre"] == "HRV"                                      # el más fuerte primero
    assert next(c for c in panel if c["nombre"] == "RHR")["r"] < 0          # RHR negativo
    # (Nota N-of-1: con n chico una serie aleatoria puede superar 0.30 por azar; el umbral de
    #  la UI es informativo, no una prueba de significancia — por eso además reportamos p.)

    # El umbral filtra lo débil: con |r|≥0.85 solo sobrevive el vínculo fuerte (HRV).
    fuerte = que_se_correlaciona(carga, {"HRV": hrv, "RHR": rhr, "Azar": azar}, min_abs_r=0.85)
    assert [c["nombre"] for c in fuerte] == ["HRV"]
    print("Umbral |r|≥0.85 deja solo:", [c["nombre"] for c in fuerte])

    print("\nOK — motor de correlación N-of-1 funcional (Pearson+OLS+p, lag, panel |r|≥0.30 n≥10).")
