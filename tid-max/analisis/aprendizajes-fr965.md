# Aprendizajes de ingeniería del Garmin Forerunner 965 → TID-MAX

> Qué extraer (y qué NO) de un multideporte de gama alta para el diseño de la banda TID-MAX.
> Benchmarking legal (aprender arquitectura/costo), **no clonar**. Fecha: 2026-08.

## Filtro de identidad (lo que NO copiamos)
Pantalla AMOLED, botones, GPS/mapas, música, pago sin contacto, formato reloj. Va contra la
identidad de TID-MAX (pod sellado, sin pantalla, sin botones). Descartado.

## Qué SÍ extraer

| # | Lo que hace el FR965 | Lo que TID-MAX toma | Encaja con |
|---|---|---|---|
| 1 | **Óptico multi-LED + fusión con IMU** para rechazar artefacto de movimiento; verde=FC, rojo/IR=SpO₂ | El **enfoque de fusión PPG+IMU** y multi-longitud de onda para PPG limpio en esfuerzo (clave para DFA-α1 en carga). Nuestro AFE MAX86141 ya es multicanal | Decisión "dato crudo obligatorio"; EVK H1 |
| 2 | **Métricas de nado desde el IMU sin GPS** (largos, brazada, SWOLF, ritmo, estilo) | Módulo de **detección de nado por IMU** — diferenciador y llena el hueco de WHOOP (no mide alberca). Ver `metricas-nadadores-elite.md` para el catálogo de métricas objetivo | OPP-01; roadmap firmware/IA |
| 3 | **RR latido-a-latido en contenedor abierto (FIT)**, no solo métricas cocinadas | Guardar **IBI/RR crudo** en el store-and-forward, exportable. Lo hacemos mejor que WHOOP (que no lo expone) | Decisión dato crudo; esquema canónico (`hr_stream[]`) |
| 4 | **Amplitud de métricas derivadas** (VO₂max, Training Load, Recovery, HRV Status, Body Battery) — software Firstbeat | El **catálogo de métricas objetivo** para la IA en la nube. ⚠️ **IP: Firstbeat tiene patentes** — se extrae el *qué*, NO el *cómo*; construir algoritmos propios | Capa IA (Fases 1–4) |
| 5 | **Duty-cycling del sensor** = la palanca real de batería (no la pantalla) | Muestreo **por ráfagas vs continuo**; cadencia de medición del óptico | Store-and-forward / modos (spec H0) |
| 6 | **5 ATM + offload a banda de pecho en agua** (BLE no atraviesa el agua) | Valida **bíceps** (PPG más limpio que muñeca) + **pod sellado**; la banda de pecho que almacena es el patrón para FC de nado precisa | Decisión bíceps; agua 5 ATM + IP68 |

## Sinergia con el módulo de natación (`metricas-nadadores-elite.md`)
El aprendizaje #2 (nado por IMU) + ese análisis definen juntos el **módulo de natación de TID-MAX**:
- **Desde el IMU (fiable):** splits/largos, frecuencia de brazada (SR), distancia por brazada (DPS),
  conteo, SWOLF, Stroke Index (Vel×DPS), estilo. (El "tiempo subacuático" es ruidoso, CV ~18–25%.)
- **Derivado (diferenciador):** **Velocidad Crítica de Nado / test T30** — umbral **sin pinchazos**,
  estimable de las sesiones. Sería el equivalente de nado a nuestras zonas FC (VT1/VT2).
- **Fuera de alcance** de una banda de muñeca/bíceps: fuerza en nado atado (célula de carga),
  medidores tipo SmartPaddle, y análisis por vídeo/cámaras. Eso define nuestro **posicionamiento**:
  TID-MAX es la capa de **carga interna + técnica en tiempo real**, no la de fuerza/vídeo.

## Cómo extraerlo (sin desviar la ruta crítica)
- **Reviews/teardown** (iFixit, DC Rainmaker) para arquitectura del óptico y colocación de LEDs.
- **Comprar 965 + HRM-Pro como dispositivo de referencia** y capturar sus **FIT/RR** para
  **comparar la calidad de dato contra el EVK** — igual que el Polar H10. Benchmarking, no clonado.
- **Integración de datos:** vía agregador **Terra/Vital** (soportan Garmin Connect) o parseando FIT
  (traen workouts de nado + stream RR) hacia `tid_data.py`.

## Recomendación
Priorizar #1 (fusión PPG+IMU), #2 (nado por IMU) y #3 (RR crudo). #4 alimenta el roadmap de IA con
algoritmos propios. **Todo se integra al benchmark del EVK (H1), sin reemplazarlo ni frenarlo.**

## Fuentes
- DC Rainmaker — FR965 in-depth review · Garmin FR965 manual (swimming) · Garmin FIT SDK (HRV/RR) ·
  Garmin support (HR while swimming). Ver también `metricas-nadadores-elite.md`.
