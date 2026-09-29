# Carlos — Línea base "Ruta Escaleras T1+T2"

**Fecha:** 2026-09-28 · **Fuente:** TCX exportado de Polar Flow (FC por segundo, 1016 puntos)
**Ruta:** 5 pisos torre 1 y torre 2, con trote entre torres (indoor).

> Datos estructurados para comparación automática: `software/benchmarks-carlos.json`.

## Resumen

| Métrica | Valor |
|---|---|
| Duración | 16:55 |
| FC promedio | 129 ppm |
| FC máx / mín | 156 / 72 ppm |
| Beneficio (Polar) | Entrenamiento por velocidad |

## Tiempo en zonas de FC

| Zona | Rango | Tiempo | % |
|---|---|---|---|
| 🟥 Z5 | 154+ | 0:49 | 4% |
| 🟧 **Z4** | 137–154 | **6:43** | **39%** |
| 🟨 Z3 | 120–137 | 4:56 | 29% |
| 🟩 Z2 | 103–120 | 3:07 | 18% |
| ⬜ Z1 | <103 | 1:21 | 7% |

**43% en Z4–Z5** → sesión de intensidad seria (cerca/por encima del umbral).

## Forma de la sesión

- **Min 0–9 (arranque + Torre 1):** calentamiento suave (72→115) y una primera subida clara ~min 7–8 (pico 140), con buena recuperación al bajar/trotar (**−13 ppm en 60 s**).
- **Min 10 → final (Torre 2 + repeticiones):** la FC trepó a **156 y se mantuvo sostenida en Z4–Z5** hasta parar → prácticamente **trabajo de umbral continuo**.

## Lecturas

- **Progresión:** 1er tercio 107 ppm → último tercio 147 ppm (+40). Es intensidad creciente, no fatiga a carga constante.
- **Recuperación:** −13 ppm/min tras la Torre 1 — decente para quien retoma; métrica a mejorar.
- **FCmáx 156** submáxima vs estimada 171 → la real probablemente es mayor (sostuvo ~2.5 min cerca del techo).
- ⚠️ **GPS no confiable en escaleras** (distancia 1.96 km y ritmo = ruido). La **FC es el dato válido**.

## Cómo usar esta línea base

Repetir la **misma ruta** cada 2–3 semanas y comparar:
1. Misma FC promedio a igual esfuerzo percibido → mejor forma aeróbica.
2. Recuperación entre torres más rápida (mayor caída de ppm en 60 s).
3. Menos tiempo en Z4–Z5 para completar la ruta → menor costo cardiaco.

## Siguiente nivel (datos crudos)

Para HRV / umbral **DFA-α1** hace falta el **R-R latido-a-latido**, que Polar **no exporta** en TCX/CSV/FIT. Se obtiene con el **Polar H10 + una app logger** (HRV Logger en iPhone, Polar Sensor Logger en Android), o cableando la **API oficial de Polar (AccessLink)** que ya existe a medias en el repo (`polar_auth.py` / `polar_sync.py`).
