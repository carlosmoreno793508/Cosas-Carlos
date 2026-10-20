#!/usr/bin/env python3
"""
fitness_age.py — Edad fitness + VO₂max estimado (modelo HUNT no-ejercicio).

Port fiel del `FitnessAgeEngine` de NOOP (código abierto; ver dossier). APROXIMADO — estimación
poblacional, no una prueba de esfuerzo ni diagnóstico médico.

Basado en:
  • VO₂max: Nes et al. 2011 (HUNT, variante con CIRCUNFERENCIA DE CINTURA). Coeficientes por sexo.
  • Índice de actividad física (PAI): HUNT1 PA-Q (Kurtze 2008), frecuencia×intensidad×duración ∈ [0,15].
  • Edad fitness: invertir la MISMA ecuación de Nes de forma auto-consistente (el término de cintura
    se cancela, así que la edad fitness solo necesita edad, sexo, FC en reposo y el PAI).

La VFC no entra aquí: la edad fitness es un marcador de FITNESS cardiorrespiratorio (FC reposo +
actividad), complementario a la Carga/recuperación (VFC). Validación cruzada con los datos de
Carlos: en la app su VO₂max salía ~59 (muy alto), coherente con RHR ~50 y mucha actividad.

Sin dependencias externas (sólo stdlib).
"""

# ------------------------------------------------------------------ coeficientes Nes 2011 (cintura)

_MEN = dict(intercept=100.27, age=0.296, wc=0.369, rhr=0.155, pai=0.226)
_WOMEN = dict(intercept=74.74, age=0.247, wc=0.259, rhr=0.114, pai=0.198)
SEE_MEN = 5.70      # error estándar del estimado (años/ml·kg⁻¹·min⁻¹)
SEE_WOMEN = 5.14

RHR_REFERENCE = 65.0    # FC reposo de referencia de la cohorte
PAI_REFERENCE = 5.0     # PAI de referencia
DISPLAY_BAND_YEARS = 5.0
MIN_AGE, MAX_AGE = 20.0, 80.0


def _es_mujer(sexo):
    s = str(sexo).lower()
    return s.startswith("f") or s in ("mujer", "femenino")


def _coeffs(sexo):
    return _WOMEN if _es_mujer(sexo) else _MEN


# ------------------------------------------------------------------ índice de actividad física (PAI)

def pai_buckets(dias_activos_semana, min_activos_por_dia, fraccion_alta_intensidad):
    """
    PAI de HUNT (0–15) desde agregados semanales medidos. Bordes = HUNT1 PA-Q (Kurtze 2008).
      frecuencia ∈ {0, 0.5, 1, 2.5, 5}  · intensidad ∈ {1,2,3} · duración ∈ {0.10,0.38,0.75,1.0}
    """
    d = dias_activos_semana
    frecuencia = 0.0 if d < 1 else 0.5 if d == 1 else 1.0 if d == 2 else 2.5 if d <= 4 else 5.0
    if frecuencia == 0:
        return 0.0
    f = fraccion_alta_intensidad
    intensidad = 1.0 if f < 0.15 else 2.0 if f < 0.5 else 3.0
    m = min_activos_por_dia
    duracion = 0.10 if m < 15 else 0.38 if m < 30 else 0.75 if m < 60 else 1.0
    return frecuencia * intensidad * duracion


def pai_desde_esfuerzo(dias_activos_semana, esfuerzo_medio_activo):
    """
    PAI (0–15) desde la carga medida por NOOP/nosotros (ruta UNIVERSAL, funciona en cualquier
    dispositivo porque el Esfuerzo sale solo de HR). El Esfuerzo (0–100, TRIMP) ya integra
    intensidad×duración → se mapea directo al producto HUNT (0–3) y se multiplica por la frecuencia.
    Calibrado para que el par de referencia (~4 días activos, Esfuerzo medio ~60) caiga cerca de PAI 5.
    """
    d = dias_activos_semana
    frecuencia = 0.0 if d < 1 else 0.5 if d == 1 else 1.0 if d == 2 else 2.5 if d <= 4 else 5.0
    if frecuencia == 0:
        return 0.0
    intensidad_duracion = min(3.0, max(0.0, esfuerzo_medio_activo / 30.0))  # 30→1, 60→2, 90→3
    return frecuencia * intensidad_duracion


# ------------------------------------------------------------------ VO₂max + edad fitness

def estima_vo2max(edad, sexo, cintura_cm, rhr, pai):
    """VO₂max (ml·kg⁻¹·min⁻¹), Nes 2011 variante cintura. Necesita una medida de cintura."""
    c = _coeffs(sexo)
    return (c["intercept"] - c["age"] * edad + c["pai"] * pai
            - c["wc"] * cintura_cm - c["rhr"] * rhr)


def edad_fitness(edad, sexo, rhr, pai):
    """
    Edad fitness auto-consistente (años, recortada [20,80]). El término de cintura se cancela al
    invertir la ecuación, así que solo necesita edad, sexo, FC en reposo y PAI:
        EF = edad + (rhrC·(RHR − 65) − paiC·(PAI − 5)) / edadC
    """
    c = _coeffs(sexo)
    fa = edad + (c["rhr"] * (rhr - RHR_REFERENCE) - c["pai"] * (pai - PAI_REFERENCE)) / c["age"]
    return min(MAX_AGE, max(MIN_AGE, fa))


def compute(edad, sexo, rhr, pai, cintura_cm=None):
    """
    Edad fitness completa. `cintura_cm` opcional (solo habilita el VO₂max). Devuelve None si falta
    edad o RHR (no inventa).
    """
    if edad is None or rhr is None:
        return None
    fa = edad_fitness(edad, sexo, rhr, pai)
    vo2 = estima_vo2max(edad, sexo, cintura_cm, rhr, pai) if (cintura_cm and cintura_cm > 0) else None
    see = SEE_WOMEN if _es_mujer(sexo) else SEE_MEN
    return {
        "edad_fitness": round(fa, 1),
        "edad_cronologica": edad,
        "delta_anos": round(edad - fa, 1),          # positivo = más joven que tu edad real
        "vo2max": round(vo2, 1) if vo2 is not None else None,
        "banda_anos": DISPLAY_BAND_YEARS,
        "see": see,
        "pai": round(pai, 2),
        "aprox": True,
        "fuente": "Edad fitness / VO₂max (Nes 2011 HUNT) · APROXIMADO, no es prueba de esfuerzo ni diagnóstico",
    }


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    # 1) Par de referencia (RHR 65, PAI 5): edad fitness == edad cronológica (ambos términos 0).
    r = compute(edad=30, sexo="m", rhr=65.0, pai=5.0)
    print("Referencia:", r["edad_fitness"], "vs", r["edad_cronologica"], "años")
    assert abs(r["edad_fitness"] - 30) < 1e-6 and r["vo2max"] is None

    # 2) Carlos (18a, RHR ~50, muy activo): VO₂max alto (la app mostró ~59).
    #    Nota: el modelo Nes es válido [20,80], así que a los 18 la edad fitness se recorta a 20.
    pai = pai_desde_esfuerzo(dias_activos_semana=6, esfuerzo_medio_activo=60)
    c = compute(edad=18, sexo="m", rhr=50.0, pai=pai, cintura_cm=78)
    print("Carlos:", c["edad_fitness"], "años (crono 18, recortado) · VO₂max", c["vo2max"], "· PAI", c["pai"])
    assert c["edad_fitness"] == 20.0            # clamp al mínimo del modelo
    assert 55 <= c["vo2max"] <= 65              # ≈ el ~59 real de la app

    # 2b) Atleta de 30 con RHR baja y activo: edad fitness MENOR que la real (delta > 0).
    a = compute(edad=30, sexo="m", rhr=50.0, pai=pai_desde_esfuerzo(5, 65))
    print("Atleta 30:", a["edad_fitness"], "años (crono 30) · delta", a["delta_anos"])
    assert a["edad_fitness"] < 30 and a["delta_anos"] > 0

    # 3) Sedentario con RHR alta: edad fitness MAYOR que la real.
    s = compute(edad=40, sexo="m", rhr=78.0, pai=pai_desde_esfuerzo(1, 20))
    print("Sedentario:", s["edad_fitness"], "años (crono 40)")
    assert s["edad_fitness"] > 40

    # 4) PAI buckets vs estrés — coherencia de rango.
    assert pai_buckets(0, 0, 0) == 0.0
    assert 0 < pai_desde_esfuerzo(4, 60) <= 15
    assert compute(None, "m", 60, 5) is None    # sin edad → None

    print("\nOK — edad fitness + VO₂max funcional (Nes 2011 HUNT, auto-consistente).")
