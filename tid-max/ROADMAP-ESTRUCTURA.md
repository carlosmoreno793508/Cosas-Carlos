# TID-MAX — Roadmap de estructuración (post-teardown NOOP)

> **Premisa.** Terminamos el teardown completo de NOOP (binario `.ipa` + código fuente
> `github.com/ryanbr/noop` + UI en vivo + validación con datos reales de Carlos). Ya sabemos
> cómo construye NOOP sus 3 scores, su modelo de datos/procedencia, su capa de inteligencia y
> su UX. Este documento convierte todo eso en un plan de 5 fases para estructurar TID-MAX.
>
> Fuentes: `analisis/noop-ipa-teardown.md` (teardown completo, Anexos A y B),
> `analisis/esquema-canonico.md` (procedencia), y el código en `software/`.
>
> **Licencia:** NOOP es PolyForm **Noncommercial**. Lo usamos como **referencia/estudio
> técnico y validación**, NO como copia para un producto comercial. Reimplementamos con
> nuestras propias decisiones y ciencia publicada.

---

## Principios transversales (aplican a TODAS las fases)

Destilados de NOOP; son la "marca de calidad" del producto:

1. **Retener, no inventar.** "Nunca mostrar un número que hubo que inventar." En código:
   cold-start → `None` (no un valor fabricado); `no disponible ≠ 0`; término ausente se cae
   y los pesos se renormalizan.
2. **Procedencia por dato.** Cada valor lleva su fuente (`Source`) y si es **medido /
   estimado / importado**. Los scores ajenos (WHOOP/Oura) se guardan como **referencia**,
   recomputamos los nuestros.
3. **APROXIMADO, no diagnóstico.** Los scores se etiquetan como aproximaciones; no es un
   dispositivo médico. (Relevante también para cumplimiento COFEPRIS — ver
   `analisis/estrategia-regulatoria-cofepris.md`.)
4. **Capas independientes y no-destructivas.** `detección → estadificación → puntuación`, más
   anotaciones manuales que NO mutan la detección. Cambiar un parámetro re-puntúa el
   historial reciente sin destruirlo.
5. **Calcular una vez, re-escalar a la vista.** Un solo cálculo interno; la escala es de
   presentación (0-100 ↔ 0-21). Guardar **absoluto + delta** (p. ej. temp de piel).
6. **Degradación por capacidad de fuente.** WHOOP = completo; Polar = HR+R-R en vivo (sin
   sueño profundo). El motor degrada con gracia según lo que la fuente puede dar.

---

## Estado actual (lo ya hecho)

- ✅ `software/hrv_rr.py` — pipeline R-R con **RMSSD/pNN50/Poincaré gap-aware** + **ventana por
  varianza** (`hrv_calidad`). Validado contra el `RR-OPTIMIZATION.md` de NOOP. (PR #53)
- ✅ `software/recovery_score.py` — **score de Carga** (z-score + logística, pesos
  55/20/15/5/5, logística k=1.6/z0=-0.2, baseline EWMA 14/21 noches, gate cold-start,
  detección-no-aplicación de saturación parasimpática). (PR #53)
- ✅ `software/sleep_score.py` — **score de Descanso** (compuesto 0.50/0.20/0.20/0.10 +
  necesidad personalizada cuartil-75/piso poblacional + **deuda de sueño** 14n/0.55). (PR #53)
- ✅ `software/strain_score.py` — **score de Esfuerzo** (Karvonen→Edwards/Banister→log D=7201,
  re-escala 0-21↔0-100) + **ACWR** (EWMA CTL42/ATL7, TSB, estados). (PR #53)
- ✅ `software/live_session.py` — **loop esfuerzo-objetivo** ("guardián silencioso": zona FC
  condicionada por Carga, warmup/stale/dwell/cooldown/histéresis, PUSH/EASE_OFF). (PR #53)
- ✅ `analisis/noop-ipa-teardown.md` — dossier completo (Anexos A: UI; B: código fuente).
- ✅ Validación N-of-1 con datos reales de Carlos: HRV↔Carga +0.96, RHR↔Carga −0.79,
  necesidad↔Descanso +0.82, calorías↔Esfuerzo +0.82 → confirman las jerarquías del motor.

---

## FASE 1 — Motor de scores completo  ⭐ núcleo del producto — ✅ COMPLETADA (PR #53)

Los 3 anillos + el loop, stdlib-only con autoprueba `__main__`. **Pesos/constantes portados
fiel del código fuente de `ryanbr/noop`** (`StrainScorer`, `AnalyticsEngine.Rest`, `SleepDebt`,
`TrainingLoadEngine`, `LiveSessionEngine`) y validados con los datos reales de Carlos.

| Entregable | Archivo | Estado |
|---|---|---|
| **Descanso** (0.50/0.20/0.20/0.10 + deuda 14n/0.55 + necesidad personalizada) | `software/sleep_score.py` | ✅ |
| **Esfuerzo** (Karvonen→Edwards/Banister→log D=7201, 0-21↔0-100) | `software/strain_score.py` | ✅ |
| **ACWR** (EWMA CTL42/ATL7, TSB, estados; ≥14 días contiguos) | en `strain_score.py` | ✅ |
| **Loop esfuerzo-objetivo** (zona FC por Carga, PUSH/EASE_OFF, silencio=ok) | `software/live_session.py` | ✅ |

Validaciones clave en las autopruebas: Descanso de la noche real de Carlos ≈ 88 (app 80);
pesas a 45% HRR → Esfuerzo 0 por Edwards (el volumen de fuerza no toca el Esfuerzo HR);
banda a Charge 66 → **136–158 bpm** (idéntico al Live Session real de Carlos).

✅ **Cableado en `tid_data.py`** (`_scores_tidmax`, pase final de `build_daily`): añade
`carga_tidmax`/`carga_banda` (HRV/RHR + respiración + temp vs baseline EWMA de noches previas,
cold-start honesto), `descanso_tidmax` (necesidad personalizada rodante), `esfuerzo_ref_0_100`
(Day Strain de WHOOP re-escalado, marcado referencia) y `acwr`/`ctl`/`atl`/`tsb` en la fila más
reciente. Marca la fuente `tidmax`. Pendiente real: recompute propio de Esfuerzo desde el stream
de HR del Polar (vive en `build_polar`, requiere captura — Fase 5).

---

## FASE 2 — Procedencia y modelo de datos  (transversal) — ✅ COMPLETADA (PR #53)

Hecho: `software/provenance.py` (modelo de 3 ejes EJECUTABLE con fusión, dedup e invariantes
de honestidad + autoprueba) y `analisis/esquema-canonico.md` v1.1 (sección Procedencia + campos
`*_tidmax` en `daily[]`). Lo entregado:

- **Badge de 3 ejes**: `fuente` (NOOP-device/import-WHOOP/import-AppleHealth/Polar/manual) ×
  `confianza` (Calibrando/Bien/Fuerte/Sólida/Genial) × `madurez` (Calibrando→Construyendo→Sólida).
- **Columna `Source` por valor** + flag **medido / estimado / importado** (temp-piel y resp =
  estimadas en-device; SpO₂ = import WHOOP; HR/R-R = medidos).
- **Fusión multi-fuente**: "mejor valor por métrica" conservando procedencia por valor; **dedup
  por solapamiento temporal** (incl. Apple Health); **scores ajenos = solo referencia**.
- **Invariantes de honestidad** codificados como tests (ver Principios 1–6).

Tabla de procedencia inspirada en `scoreInputProvenance` (migración v29 de NOOP) + columna
`Source` con marca `APPROXIMATE` del export en formato WHOOP.

---

## FASE 3 — Capa de inteligencia — ✅ COMPLETADA (PR #53)

Hecho: `correlacion.py` (motor N-of-1 Pearson+OLS+p, alineación por día, lag, panel
"qué se correlaciona" |r|≥0.30/n≥10), `explica.py` (explicabilidad "¿por qué este número?"
que consume la traza de los scores sin recalcular) y `coach_llm.py` (coach BYOK local-first,
sólo `urllib`, clave sólo en cabecera, apuntable a Ollama/LM Studio local). Lo planeado era:

- **Motor de correlación N-of-1**: Pearson r por métrica/score sobre la ventana visible,
  **|r| ≥ 0.30, n ≥ 10** → panel "qué se correlaciona" (ya descrito en dossier A.10/A.11).
  Extender/consolidar en `software/` (hoy disperso en `tid_coach.py`).
- **Dosis-respuesta / lag por hallazgo** (prior bayesiano poblacional → shrinkage a datos
  propios) — ya bosquejado; formalizar.
- **Coach BYOK local-first** (`software/tid_coach.py`): elegir proveedor
  (OpenAI/Anthropic/Gemini/**Ollama/llama.cpp local**), clave en store seguro, **única
  superficie que sale del dispositivo, solo bajo petición explícita**, envía un resumen de
  métricas. Opción 100% local para privacidad total.
- **Explicabilidad "¿por qué este X?"**: traza por decisión (qué término movió el score).

---

## FASE 4 — UX / estructura de la app (PWA en `app/`) — 🟡 NÚCLEO HECHO (PR #53)

Hecho: `app/tablero.html` — vista "Hoy + Tendencias" autocontenida (lee `daily.json`/`data.json`
o cae a demo embebido con los números reales de Carlos). Incluye los **3 anillos**
(Carga/Esfuerzo/Descanso) con **`no disponible ≠ 0`** (anillo vacío, no 0), **badge de madurez**
y de **fuente** (procedencia visible), **Señales diarias** (tiles prom/mín/máx/tendencia),
**heatmap de Carga** 90 días, panel **"qué se correlaciona"** (Pearson |r|≥0.30/n≥10, replica de
`correlacion.py`), **drill-down** por score/métrica (modal con sparkline + stats + "por qué"), y
etiqueta **APROXIMADO**. Validado por render (Chromium): VFC↔Carga +0.95 ≈ el +0.96 real.

**Pendiente de Fase 4:** nav de 5 pestañas completa, pestaña Sueño con hipnograma, **export PDF**
de 1 página, e integración en `app/index.html` (la PWA grande). Lo planeado completo:

- **5 pestañas**: Hoy · Tendencias · Sueño · Entrenador · Más.
- **Hoy**: 3 anillos (Carga/Esfuerzo/Descanso) + badge de **madurez** + recomendación del día
  ("Mantener"). Acciones rápidas (iniciar entreno, diario, respira). `no disponible` = anillo
  vacío, nunca 0.
- **Drill-down estándar** (reutilizable para cada score y métrica): selector de ventana
  (M/2S/3S/L/3M/6M/1A/TODO) + tiles (prom/mín/máx/Δ vs ant./más reciente) + lista de lecturas
  con **columna `Source`** + panel "qué se correlaciona".
- **Tendencias**: heatmap calendario (Agotado→En su pico), **libro de deuda de sueño** (14n),
  desglose de fases vs típico, **export PDF de 1 página** (recuperación/sueño/VFC/RHR/esfuerzo).
- **Sueño**: score + fases (hipnograma) + marcas manuales no-destructivas + "¿por qué este
  sueño?".
- (Opcional, pulido) lenguaje visual "líquido" tipo Liquid Metal.

---

## FASE 5 — Validación

- **Captura Polar H10** (`software/polar_capture.py`, H10 preferido sobre Verity para DFA-α1
  limpio) → validar `hrv_rr.py` con R-R real; emitir CSV con el mismo esquema de streams que
  el "raw sensor export" de NOOP (HR, R-R, movimiento, pasos, SpO₂, temp, resp, eventos).
- **Contraste contra `ryanbr/noop`**: su suite de tests con replicación numpy
  (`RecoveryAgreementTest`, `HrvGoldAgreementTest`, etc.) como oráculo para pinear constantes.
- Estudiar `PROTOCOL_WHOOP4/5` + `BLE_REVERSE_ENGINEERING` (de dónde sale el R-R y los
  eventos) para nuestra propia captura de banda.

---

## Secuencia recomendada

```
Fase 1 (motor)  →  Fase 2 (procedencia)  →  Fase 3 (inteligencia)  →  Fase 4 (UX)  →  Fase 5 (validación continua)
     core               transversal             diferenciador            producto           calidad
```

Fase 1 primero porque Carga ya aterrizó y los 3 anillos + el loop son el core. Fase 2 es
transversal y barata de hacer temprano. Fase 5 (captura Polar) puede correr en paralelo en
cuanto haya banda disponible.

## Mapeo NOOP → TID-MAX (resumen)

| Lo que hace NOOP | Lo que hacemos en TID-MAX |
|---|---|
| Carga = z-score+logística HRV-dominante (55/20/15/5/5) | `recovery_score.py` ✅ |
| RMSSD gap-aware + ventana por varianza (−35% MAE) | `hrv_rr.py` ✅ |
| Descanso = necesidad+eficiencia+reparador+consistencia+deuda | `sleep_score.py` (Fase 1) |
| Esfuerzo = Karvonen→TRIMP; ACWR crónica/aguda | `strain_score.py` (Fase 1) |
| Guardián silencioso (zona FC gated por Carga) | `live_session.py` (Fase 1) |
| `scoreInputProvenance` + columna `Source`/`APPROXIMATE` | `esquema-canonico` 3 ejes (Fase 2) |
| Panel "qué se correlaciona" (Pearson, \|r\|≥0.30) | motor N-of-1 (Fase 3) |
| Coach BYOK local-first | `tid_coach.py` (Fase 3) |
| 5 pestañas + anillos + drill-down + heatmap + PDF | PWA `app/` (Fase 4) |
| Raw sensor export (streams muestra-a-muestra) | `polar_capture.py` CSV (Fase 5) |
