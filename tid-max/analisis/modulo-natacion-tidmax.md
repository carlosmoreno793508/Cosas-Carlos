# Módulo de Natación TID-MAX — mini-spec

> Consolida `aprendizajes-fr965.md` (cómo capturar el dato) + `metricas-nadadores-elite.md`
> (qué métricas importan) en el alcance del módulo de nado de TID-MAX. Incluye el análisis de
> **funcionalidad por estilo, con foco en DORSO (backstroke)**. Fecha: 2026-08.

## 1. Qué mide / deriva TID-MAX (y qué NO)

**Desde el IMU (acelerómetro + giroscopio) — fiable:**
- Largos y splits, **frecuencia de brazada (SR)**, **distancia por brazada (DPS)**, conteo, **SWOLF**,
  **Stroke Index (Vel×DPS)**, reconocimiento de **estilo**, virajes.

**Derivado en la nube/IA — el diferenciador:**
- **Velocidad Crítica de Nado (VCN) / test T30** = umbral **sin pinchazos** (el equivalente de nado a
  las zonas FC VT1/VT2). Tendencias de eficiencia (VCN sube, frecuencia crítica baja = mejora técnica).
- **Carga interna** por FC (requiere banda de pecho para FC precisa en agua) y **recovery/readiness**.

**Fuera de alcance de una banda de muñeca/bíceps (importante para el posicionamiento):**
- **Fuerza/potencia propulsiva** (nado atado + célula de carga, SmartPaddle).
- **Fase subacuática fina** (velocidad/aceleración intra-ciclo) — eso es de **vídeo/velocity meter**.
- El **"tiempo subacuático" del IMU es ruidoso** (CV ~18–25%).

> **Posicionamiento:** TID-MAX es la capa de **carga interna + eficiencia + pacing + recuperación en
> tiempo real**, no la de fuerza ni la de vídeo. Complementa, no reemplaza, el análisis biomecánico.

## 2. Colocación: bíceps/pecho > muñeca

La literatura es clara: para conteo de brazada, la **muñeca es la posición MENOS precisa**
(~75% de aciertos sin error) frente a espalda baja/sacro (~86%). La **FC óptica de muñeca en agua es
poco confiable** en todos los relojes. → Para nado, **bíceps** (decisión TID-MAX) da mejor PPG que
muñeca, y para FC precisa se usa **banda de pecho que almacena** (BLE no atraviesa el agua).

## 3. Funcionalidad por estilo — ¿funciona para un DORSISTA?

| Estilo | Detección IMU | Notas |
|---|---|---|
| Crol (freestyle) | ✅ Alta (~98%) | El más fácil |
| **Dorso (backstroke)** | 🟡 **El más difícil para IMU** | Ver abajo |
| Pecho | ✅ Buena | Patrón marcado |
| Mariposa | ✅ Buena | Patrón marcado |

### El caso del dorsista (análisis)

**Lo que SÍ funciona para dorso** (igual que otros estilos):
- Carga interna (FC con banda de pecho), splits/largos, SWOLF, VCN/T30, recuperación y readiness.
  Todo el valor de "carga interna + pacing + recuperación" aplica al dorsista.

**Los 2 puntos débiles reales para dorso:**
1. **La detección de brazada por IMU es JUSTO la más difícil en dorso.** Estudios de un solo IMU
   reportan datos válidos "para la mayoría de los estilos, **con la excepción del dorso**"; y la
   muñeca es la peor colocación. → SR/DPS/conteo tendrán **menor precisión en dorso** que en crol.
   Mitigación: **bíceps** (mejor que muñeca) + algoritmos afinados por estilo.
2. **La palanca #1 del dorsista es la patada de delfín subacuática — y es lo que la banda mide
   PEOR.** En dorso, alargar/acelerar el subacuático da mejoras enormes: +1–2 m de subacuático en
   virajes ≈ **~1% en 200 m**; un subacuático largo en el último viraje ≈ **2.3%** de mejora. Y el
   diferenciador de élite es la **velocidad** de la patada bajo el agua, no solo la distancia.
   **Nada de eso lo captura bien una banda** (el IMU subacuático es ruidoso y no mide velocidad de
   patada desde el brazo). Para eso siguen mandando **vídeo/velocity meter**.

**Veredicto para un dorsista:**
TID-MAX es **funcional y útil** para su **carga interna, pacing, eficiencia (SWOLF/VCN) y
recuperación** — que es mucho. Pero **no es la herramienta para lo que más define su carrera** (la
velocidad de patada subacuática). Con un dorsista hay que **poner la expectativa correcta**: la banda
optimiza el "motor" y la recuperación; el subacuático se pule con vídeo. Recomendación de uso:
**bíceps + banda de pecho** para maximizar precisión.

## 4. Implicaciones para el roadmap TID-MAX
- **Firmware/IA:** modelo de detección de estilo con **rama afinada para dorso**; captura de largos,
  SR, DPS, SWOLF; y **VCN/T30** en la nube como diferenciador.
- **Hardware:** validar el pod en **bíceps** con rotación amplia de brazo (dorso mueve mucho el brazo).
- **Producto:** comunicar honestamente el alcance (carga/eficiencia/recuperación, **no** subacuático).
- Ingesta: FIT/agregador (Terra/Vital) para benchmark contra Garmin FR965 + HRM-Pro (ver H1.3).

## Fuentes
- Validation of Quantified Swim Stroke Mechanics Using IMU (Paralympic; "excepción del dorso") — PMC10813451
- Macro-Micro IMU swimming analysis (muñeca = peor colocación) — PMC7841373
- Dolphin kick en finales de dorso (regional→olímpico; ~2.3% / ~1%) — Frontiers Sports 2025 (PMC11868261)
- "How far underwater should you kick" (velocidad > distancia) — yourswimlog
- Ver también `aprendizajes-fr965.md` y `metricas-nadadores-elite.md`.
