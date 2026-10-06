# Rangos de referencia — Analizador de técnica de nado (`swim_form.py`)

Honestidad primero: un video **2D sobre el agua** da **rangos poblacionales y tendencia**, no un
laboratorio. Lo que de verdad pasa bajo el agua (catch, agarre, patada, rotación 3D) necesita
cámara subacuática y un técnico. Esta herramienta mide lo que una toma lateral sí resuelve bien y
es honesta sobre lo demás.

## Qué gradúa (y qué solo reporta)

| Métrica | Verde | Ámbar | Rojo | Nota |
|---|---|---|---|---|
| **Consistencia de tempo (CV %)** | ≤ 8 | 8–14 | > 14 | Lo más confiable. Brazada pareja = buen ritmo; CV alto = se descompone al fatigarse. |
| **Línea del cuerpo (°)** hombro→cadera vs horizontal | ≤ 8 | 8–14 | > 14 | Cadera caída = más arrastre. La segunda palanca robusta en 2D lateral. |
| **Frecuencia de brazada (br/min)** | — (reporta) | — | — | Depende MUCHO de distancia/velocidad; se reporta, no se gradúa. Banda típica entreno ~55–95 br/min. |
| **Simetría L/R (codos)** | — (reporta) | — | — | Útil si ambos brazos son visibles (mejor desde una toma frontal); en lateral es orientativa. |

## Por qué estas y no "estilo perfecto"

- **No calificamos una brazada "ideal"** (altura de codo exacta, timing del catch) desde 2D lateral:
  la cámara no ve la profundidad y se inventaría certeza. Igual que el de running mide *overstride*
  en vez de pelear "heel vs midfoot", aquí medimos **lo que el ángulo lateral sí resuelve**.
- **Tempo** y **línea del cuerpo** son las dos que aguantan el ruido de un clip de teléfono.

## Cómo filmar (el 90% del resultado)

- **Lateral**, cámara a la **altura del agua** (no desde arriba), perpendicular al carril.
- **Todo el cuerpo en cuadro** (cabeza a cadera al menos; idealmente a los pies).
- **Luz buena**, sin reflejos fuertes; **60 fps** si el teléfono puede (menos *motion blur*).
- **Recorta** el clip a solo el tramo de nado (quita el empuje de pared y el giro).
- 3–5 ciclos limpios bastan para una lectura estable (se usa la mediana).

## Límites conocidos

- **Agua y salpicadura** confunden la pose: en tramos con mucha espuma la confianza baja y esos
  frames se descartan. Por eso conviene luz buena y toma lateral limpia.
- **Submarino**: la brazada subacuática y la patada no se miden aquí (otra herramienta/cámara).
- **No es consejo médico ni técnico definitivo.** Es una ayuda cuantitativa para ver tendencia
  sesión a sesión (¿mejora el tempo?, ¿sube la cadera?), no un reemplazo del entrenador.

## Siguiente nivel (si se valida con clips reales de Gael)

- Afinar los umbrales con video real de Gael (su rango normal de tempo/línea).
- Toma **frontal** adicional para simetría L/R y cruce de línea media.
- Correlacionar frecuencia de brazada con la velocidad del carril (DPS = distancia por brazada).
