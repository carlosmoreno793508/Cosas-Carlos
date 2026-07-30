# Dashboard TID-MAX vs. la competencia — análisis y backlog

Objetivo: hacer que el panel de TID-MAX **iguale las métricas de mesa** de los líderes y **gane** en
nuestro nicho (alto rendimiento, natación, coach con plan). Base: lo que hoy podemos calcular con los
datos de WHOOP (y mañana con dato crudo propio).

## Qué muestra cada quién (métricas estrella)

| Métrica / vista | WHOOP | Garmin | Oura | Polar | **TID-MAX hoy** |
|---|---|---|---|---|---|
| Recuperación diaria | Recovery % | Training Readiness | Readiness | Nightly Recharge | ✅ Recovery % + semáforo |
| HRV | ✅ (rMSSD nocturno) | **HRV Status** (7d vs 60d) | ✅ | ✅ | ✅ valor + vs base |
| FC reposo | ✅ | ✅ | ✅ | ✅ | ✅ + vs base |
| Sueño (detalle) | Perf + fases + deuda | Sleep score + fases | **Sleep score fuerte** | Sleep Plus | ⚠️ solo % y horas |
| Carga aguda:crónica | Strain | **Load Ratio (ACWR)** 0.8–1.3 | — | Training Load Pro | ⚠️ solo en el coach |
| Forma/fitness (CTL/ATL/TSB) | — | Training Status + VO2max | — | ✅ | ❌ falta |
| Frecuencia respiratoria | ✅ (alerta) | ✅ | ✅ | ✅ | ❌ falta |
| Resumen semanal | parcial | ✅ | ✅ | ✅ | ❌ falta |
| **Distancia real de nado** | ❌ | ✅ (reloj) | ❌ | ✅ (reloj) | ✅ **registro real** |
| **Coach con plan diario** | de pago | parcial | parcial | FitSpark | ✅ **integrado (5 pilares)** |
| **Contexto de periodización** (evento) | ❌ | parcial | ❌ | parcial | ✅ carga→taper Vancouver |
| **Dato crudo / DFA-α1** | ❌ | ❌ | ❌ | SDK | 🔜 (Verity Sense/EVK) |

## Lecturas clave
- **Garmin es la vara** en métricas de entrenamiento: su **Load Ratio (ACWR)** con zonas de color
  (0.8–1.3 óptimo, >1.5 riesgo) y su **HRV Status** (rolling 7d vs base 60d) son estándar de facto.
- **Oura/WHOOP** ganan en sueño y simplicidad; el sueño es donde **más flojos estamos** hoy.
- **Nadie** da bien la **distancia de nado en alberca** ni un **coach con plan** integrado — ahí ya
  ganamos, y hay que **hacerlo evidente** en el panel.

## Dónde ganamos (subrayar en el diseño)
1. **Volumen real de nado** (competidores de muñeca no pueden).
2. **Coach con plan de 5 pilares** integrado (WHOOP lo cobra aparte).
3. **Periodización con el evento** (nadie sabe que Gael va a Vancouver).
4. **Semáforo preventivo + ACWR** ya funcionando.
5. 🔜 **Dato crudo/DFA-α1** — ningún consumer band lo expone.

## Backlog de mejoras al dashboard (todo calculable con WHOOP hoy)

**Alta prioridad (paridad + diferenciación):**
- **B1 · Carga (ACWR) en el panel** con zonas de color tipo Garmin (0.8–1.3 verde, >1.5 rojo). Ya se
  calcula en el coach; falta mostrarlo y graficar la tendencia.
- **B2 · Curva de Forma (CTL/ATL/TSB)** = fitness (crónico), fatiga (agudo) y **forma** (fitness−fatiga).
  Es LA gráfica que los entrenadores quieren (ítem 1.1 del tracker).
- **B3 · Resumen de la semana**: strain total, km nadados, recovery promedio, sesiones, sueño promedio.

**Media prioridad (paridad de sueño y salud):**
- **B4 · Detalle de sueño**: fases (profundo/REM/ligero/despierto), deuda de sueño, consistencia
  (WHOOP ya trae `stage_summary` y `sleep_needed`).
- **B5 · Frecuencia respiratoria** (tendencia) — alerta temprana de enfermedad.
- **B6 · HRV Status** clasificado (equilibrado / desequilibrado) como Garmin.

**Cuando haya dato propio:**
- **B7 · Eficiencia de nado** (SWOLF, ritmo/100 m) — requiere distancia por vueltas (banda TID-MAX).

## Mood board — herramientas analizadas e ideas a robar

Revisadas con capturas reales (jul 2026):

| Herramienta | Qué robar |
|---|---|
| **intervals.icu / TrainingPeaks** | Fitness/Fatiga/**Forma** (CTL/ATL/TSB); **% polarizado** / distribución de zonas; carga semanal en calendario |
| **Strava + Elevate** | **Relative Effort**, **HRSS**, **TRIMP** (carga por FC); **splits/parciales**; progreso del **mismo esfuerzo en el tiempo**; **log** con búsqueda/filtros/**etiquetas** (entreno/competencia/recuperación); estadísticas **4 sem/año/total**; **filtro por deporte**; **récords por distancia**; gear; compartir |
| **GoldenCheetah** | **Tiempo en zonas** por sesión; TSS/IF/NP/VI; máximos/promedios/modelo (CP, W′) |
| **Final Surge** | **Calendario del coach** con sesiones planeadas + planes de entrenamiento |
| **SportTracks** | Tiles limpios por actividad + traza FC/ritmo/altitud |

**Ángulo TID-MAX:** casi todas son ciclismo/carrera con **potencia**. Gael es **nadador** → nuestra carga
viene de la **FC (TRIMP/HRSS)**, y ganamos con **distancia real de nado, récords por distancia y coach**.

## Plan de construcción priorizado (v2)

**Fase A — paridad de entrenamiento (YA, con datos WHOOP):**
- **A1** Carga **ACWR** en el panel + colores (0.8–1.3 verde, >1.5 rojo). *(groundwork ya en el código)*
- **A2** **Curva de Forma** (CTL/ATL/TSB). *(groundwork ya en el código)*
- **A3** **Resumen semanal** + acumulados **4 sem / año / total**, con **filtro nado/pesas**.
- **A4** **TRIMP/HRSS** (carga por FC) — aproximado con FC promedio de WHOOP; fino con Polar.

**Fase B — diferenciadores para nadador:**
- **B1** **Récords de nado por distancia** (50/100/200/400/800/1500) — registro manual ahora, auto con dato propio.
- **B2** **Progreso del mismo set/distancia en el tiempo** (rumbo a Vancouver).
- **B3** **Log de sesiones** con etiquetas (entreno / competencia / recuperación).

**Fase C — desbloquea el Polar (dato crudo / Etapa 2 PMD):**
- **C1** **Tiempo en zonas de FC** por sesión (traza latido a latido).
- **C2** **TRIMP real por sesión** + **splits por 100 m**.
- **C3** **DFA-α1** (validación del pipeline vs. Polar H10).

**Extras:** reporte compartible (coach/mamá), gear de nado.

## Fuentes
- Garmin Training Readiness / Load Ratio / Load Focus / SWOLF (the5krunner, shoulditrain, Garmin blog).
- WHOOP vs Oura vs Garmin 2026 (athletedata.health, sensai.fit, baselineathlete).
