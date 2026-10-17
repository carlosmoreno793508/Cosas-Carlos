# Dossier — NOOP (app WHOOP offline) · qué métricas robarle a TID-MAX

**Fecha:** 2026-10-17 · **Fuente:** repo público `github.com/ryanbr/noop` (README) + análisis previo.
**Encargo (Carlos):** analizar NOOP y ver **qué le podemos mejorar al nuestro en cuanto a MÉTRICAS**.

> Contexto: NOOP es la app open-source que lee el strap WHOOP por Bluetooth **sin membresía** (se
> sideloadea con Sideloadly; no está en App Store porque no está notarizada por Apple). Es la vía
> **gratis + R-R crudo** para Gael. Pero además resultó ser un **referente de métricas muy serio** —
> esta nota se enfoca en eso.

---

## 0. TL;DR — el hallazgo

NOOP no es solo "WHOOP gratis". Es una **masterclass de métricas de ciencia deportiva** hecha por un
indie: cada score cita su método (Plews, Lamberts, Gabbett, Foster, Task Force 1996…) y **etiqueta con
honestidad qué puede y qué no** según el dispositivo. Varias las tenemos; **5 no**, y son baratas de sumar.

**Y el foso que NOOP NO cruza: DFA-α1.** NOOP captura el R-R crudo (`rrInterval.rrMs`) pero **no calcula
DFA-α1 en ningún lado**. Nosotros sí tenemos ese camino. Entonces la jugada es: **NOOP nos da el dato crudo
de Gael gratis, y TID-MAX saca el umbral (LT1/VT1) que NOOP deja sobre la mesa.**

---

## 1. Qué CAPTURA NOOP (crudo, del strap por BLE)

Tablas SQLite (GRDB), cada una con `deviceId` + `ts`:

| Tabla | Campo | Qué es |
|---|---|---|
| `hrSample` | `bpm` | Frecuencia cardiaca (~1 Hz en vivo) |
| `rrInterval` | `rrMs` | **Intervalo R-R crudo** (latido a latido) → la joya para HRV/DFA |
| `spo2Sample` | `red`, `ir` | PPG crudo de dos longitudes de onda (para SpO₂) |
| `skinTempSample` | `raw` | Temperatura de piel cruda |
| `respSample` | `raw` | Respiración cruda |

Caveats honestos del propio NOOP en WHOOP 5.0/MG: SpO₂ "no recuperable offline del PPG multiplexado
actual"; temp de piel "no consistente entre firmwares"; HRV/respiración nocturnas "incompletas salvo que
se capturen suficientes R-R". Esto importa para Gael según su modelo de strap.

## 2. Qué COMPUTA NOOP (derivado) — y si lo tenemos

| Métrica NOOP | Método que cita | ¿TID-MAX lo tiene? |
|---|---|---|
| **Recovery 0–100** | z-score HRV-dominante + composite logístico vs baseline personal | ✅ Sí (semáforo/recovery) |
| **HRV RMSSD + SDNN** | Task Force 1996 + **filtrado ectópico Malik** | ⚠️ RMSSD/SDNN sí; **filtrado ectópico NO** |
| **Strain 0–21** | %HRR (**Karvonen**) + TRIMP Edwards/Banister | ✅ TRIMP sí (Karvonen por nombre, no) |
| **Readiness (4 estados)** | HRV vs base (**Plews/Buchheit**) + drift de FC reposo (**Lamberts**) + drift de frec. respiratoria + ACWR (**Gabbett**) + **monotonía (Foster)** | ⚠️ Parcial: ACWR sí, readiness sí; **monotonía NO**, drift de respiración NO |
| **Sueño** (hipnograma, etapas 4-clases, eficiencia, FC reposo, HRV) | stager on-device sleep/wake | ✅ Sí (etapas, siestas, horario) |
| **Resting HR** | drift como input de readiness | ✅ Sí (vs base) |
| **Respiratory rate** | input de readiness (drift nocturno) | ✅ Sí (lo mostramos) |
| **Stress / carga autonómica** | viz a nivel día | ❌ **No** |
| **Baselines rolling + sparkline 14 días por tile** | `Baselines.swift` | ⚠️ Tenemos `vs_base_pct`; **sparkline por tile no** |
| **Activity Cost** (Insights) | aprende cuánto te cuesta cada tipo de sesión en la recuperación del día siguiente y cuánto tardas en rebotar | ❌ **No** (y es oro predictivo) |
| **Correlaciones** (Compare) | Pearson r + OLS + correlación con lag entre 2 series | ❌ **No** |
| **Workouts** | strain, **tiempo en cada zona FC**, curva FC, avg/max, "Effort añadido" | ⚠️ Zonas sí; por-workout/"effort" parcial |
| **DFA-α1 / umbral** | — | **NOOP NO lo hace** → nuestro foso |
| **Breathe (biofeedback)** | Relax 4-6 / Coherence 5.5 / Box 4-4 + **RMSSD en vivo + HRV pre/post** | ❌ **No** |

---

## 3. Lo que le MEJORAMOS al nuestro (priorizado, enfocado en métricas)

### 🟢 Quick wins (métricas baratas, alto valor)
1. **Filtrado de latidos ectópicos (Malik)** antes de calcular HRV. Hoy calculamos RMSSD/SDNN sin
   limpiar latidos anómalos → un ectópico infla el HRV y ensucia el score. Es un filtro de pocas líneas
   y **sube la integridad del dato** (nuestro ethos de auditor). *Alto impacto, casi cero costo.*
2. **Monotonía de entrenamiento (Foster)** = media/desviación de la carga diaria de la semana. Marca
   "entrenas mucho pero todo igual" (riesgo de estancamiento/lesión). Complementa el ACWR que ya tenemos.
3. **Drift de frecuencia respiratoria nocturna** como señal de readiness (ya mostramos la respiración;
   falta usar su tendencia, no solo el valor).
4. **"Effort añadido" + tiempo en cada zona POR entreno** en el reporte (ya tenemos zonas globales).

### 🟡 Features de métrica más grandes (diferenciadores)
5. **Activity Cost** — aprender, del historial, cuánto cuesta cada tipo de sesión a la recuperación del
   día siguiente y cuánto tarda el atleta en rebotar. Esto es **IA predictiva real** (nuestro edge sobre
   Muse) y encaja con la "memoria del atleta" del dossier de la comunidad.
6. **Motor de correlaciones** (Pearson/OLS/lag) entre dos series (p. ej. "sueño → recovery del día
   siguiente", "alcohol → HRV"). El "¿por qué?" que ningún rival del panorama da.
7. **Breathe / biofeedback de HRV** — sesión guiada (4-6, 5.5, box) que mide **RMSSD en vivo y HRV
   pre/post**. Métrica accionable + feature de bienestar que retiene.
8. **Stress / carga autonómica a nivel día** — viz de activación simpática.

### ⭐ El foso (lo que NOOP deja servido)
9. **DFA-α1 desde el R-R de NOOP.** NOOP captura `rrMs` crudo y lo exporta, pero **no calcula DFA-α1**.
   Nosotros ya tenemos el camino de DFA. Flujo: Gael corre NOOP (gratis) → importamos su R-R →
   **TID-MAX saca LT1/VT1 no invasivo** que ni WHOOP ni NOOP dan. Ese es el metro que nadie más tiene.

---

## 4. El patrón de PRODUCTO a robar: honestidad por fuente

Lo más elegante de NOOP no es una métrica: es que **cada número viene etiquetado** con lo que ese
dispositivo sí puede ("Blood Oxygen candidate: round-matched 4/4 nights", "Sleep duration: Experimental",
"HRV: Not possible from this data on Oura"). Es exactamente nuestro **ethos de integridad de dato
(agente auditor)**. Propuesta: **matriz de capacidad por fuente** en la app — cada métrica marcada
`MEDIDO / ESTIMADO / NO DISPONIBLE` según sea WHOOP(NOOP) / Polar(intervals) / banda propia. Convierte
una limitación en **confianza de marca** (justo donde Muse sangra).

## 5. Importación: cómo entra el dato de NOOP a TID-MAX

NOOP importa/exporta por archivos, no API:
- **Entra a NOOP:** CSVs de WHOOP (`physiological_cycles.csv`, `sleeps.csv`, `workouts.csv`,
  `journal_entries.csv`), Apple Health `export.xml`, CSVs de nutrición (Cronometer/MacroFactor).
- **Sale de NOOP:** PDF de una página (Trends) + "Export for Shortcuts" (iOS). **No** hay export JSON/CSV
  del store crudo documentado.
- **Implicación:** para el R-R crudo de Gael probablemente haya que leer el **`.noopbak`** / SQLite local
  (vía la capa `NoopLocalAccess` on-device, o el backup), no un export limpio. A validar cuando Gael
  sideloadee. El importador NOOP→TID-MAX es trabajo aparte (mapear `rrInterval.rrMs` → nuestro pipeline).

---

## Resumen para decidir

| Add | Tipo | Costo | Por qué |
|---|---|---|---|
| Filtrado ectópico (Malik) | quick | muy bajo | HRV limpio = score confiable |
| Monotonía (Foster) | quick | bajo | riesgo de estancamiento, junto al ACWR |
| Drift respiratorio nocturno | quick | bajo | readiness más fina |
| Effort + zona por workout | quick | bajo | lectura por sesión |
| **Activity Cost** | grande | medio | **IA predictiva (edge real)** |
| Correlaciones (Pearson/OLS/lag) | grande | medio | el "por qué" |
| Breathe + HRV pre/post | grande | medio | métrica accionable + retención |
| Stress diario | medio | bajo-medio | activación autonómica |
| **DFA-α1 desde R-R de NOOP** | foso | ya casi hecho | **umbral que nadie más da** |
| Matriz de capacidad por fuente | producto | bajo | integridad = confianza de marca |

**Veredicto:** NOOP es nuestro **mejor donante de ideas de métrica** (más que Athyx o Muse) porque
habla el mismo idioma (ciencia deportiva, dato crudo). Robar los 4 quick wins ya; construir
Activity Cost + correlaciones como diferenciador predictivo; y usar el R-R gratis de NOOP para el
DFA-α1 que NOOP mismo no calcula.
