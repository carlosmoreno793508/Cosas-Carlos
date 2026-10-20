# Esquema de datos canónico — TID-MAX (v1.1)

El **contrato** entre la ingesta y todo lo demás (dashboard, coach, agentes AI). No importa de qué
dispositivo venga el dato (WHOOP, Polar, Garmin, banda TID-MAX…): se normaliza a este esquema.
Lo produce `software/tid_data.py` en `datos/procesado/`.

> **Por qué importa:** es lo que permite la ingesta multi-fuente (Capa 0). Los agentes AI leen SIEMPRE
> este esquema, no los formatos crudos de cada marca. Cambiar de fuente = cambiar solo el normalizador.

## Objetos

### `atleta`
| campo | tipo | fuente |
|---|---|---|
| nombre | string | WHOOP perfil |
| altura_m | float | WHOOP body |
| peso_kg | float | WHOOP body |
| fc_max | int | WHOOP body |

### `evento` — competencia objetivo (da contexto temporal a los agentes)
| campo | tipo | fuente |
|---|---|---|
| nombre | string | `software/evento.json` (o `datos/evento.json`) |
| sede | string | config |
| fecha_inicio / fecha_fin | YYYY-MM-DD | config |
| fecha_viaje | YYYY-MM-DD | config |
| dias_al_evento / dias_al_viaje | int | **calculado** por el pipeline |
| fase | string | **calculado**: carga (>21 d) · taper (≤21 d) · pico (≤7 d) · post-evento (<0) |
> Es lo que permite que el coach razone el **taper**: en fase de afinamiento la meta es llegar fresco, no acumular carga.

### `plan_semana` — semana del macrociclo que cae hoy (plan vs real)
| campo | tipo | fuente |
|---|---|---|
| semana | string | `plan-macro.json` (macrociclo 2025-26 del entrenador) |
| fase_plan | string | capacidad dominante planeada |
| km_plan / ses_plan | int | km y sesiones **planeados** esa semana |
| comp | string | competencia de la semana |
> El pipeline elige la semana cuya `inicio<=hoy<=fin`. Da al coach el **km objetivo** para contrastar contra el nado real (WHOOP/registro).

### `daily[]` — una fila por día (`fecha` = clave, `YYYY-MM-DD`)
| campo | unidad | fuente |
|---|---|---|
| recovery_pct | % | WHOOP |
| hrv_ms | ms (rMSSD) | **Polar H10 (BLE, medido)** si hay lectura de reposo ese día; si no, WHOOP |
| rhr_bpm | lpm | **Polar H10 (BLE, p10)** si hay lectura de reposo; si no, WHOOP |
| hrv_ms_polar / rhr_bpm_polar | ms / lpm | Polar H10 por BLE (R-R latido a latido, `_polar_ble_diario`) |
| hrv_ms_whoop / rhr_bpm_whoop | ms / lpm | valor de WHOOP **conservado** cuando el H10 lo reemplaza (transparencia) |
| hrv_rr_muestras | # | intervalos R-R que respaldan la HVC del H10 ese día |
| spo2_pct | % | WHOOP |
| skin_temp_c | °C | WHOOP |
| sleep_perf_pct | % | WHOOP |
| sleep_hours | h | WHOOP |
| resp_rate | rpm | WHOOP |
| strain | 0–21 | WHOOP |
| kcal | kcal | WHOOP |
| swim_km | km | registro manual |
| swim_sessions | # | registro manual |
| pesas_min | min | registro manual |
| **carga_tidmax** / carga_banda | 0–100 / rojo·amarillo·verde | **TID-MAX** (`recovery_score`) |
| **descanso_tidmax** | 0–100 | **TID-MAX** (`sleep_score`) |
| **esfuerzo_ref_0_100** | 0–100 | WHOOP (Day Strain re-escalado, **referencia**) |
| **acwr / ctl / atl / tsb** | ratio / carga | **TID-MAX** (`strain_score`, en la fila más reciente) |
| fuentes | [string] | qué fuentes aportaron ese día (incluye `tidmax` si calculamos scores) |
> Los `*_tidmax` los produce el pase `_scores_tidmax` de `tid_data.build_daily` a partir de los
> datos crudos + baselines personales rodantes; `esfuerzo_ref_0_100` es el score AJENO de WHOOP
> re-escalado y marcado **referencia** (recomputamos el nuestro cuando haya stream de HR del Polar).
> **Polar H10 (BLE)**: `_polar_ble_diario` lee `datos/polar_*.csv` (latido a latido). De cada captura
> en **reposo** (sin arranque de esfuerzo sostenido) saca la HVC (RMSSD por calidad de ventanas) y la
> FC en reposo MEDIDAS; al ser grado investigación, **manda sobre la HVC derivada de WHOOP** para los
> scores (Carga/readiness/illness), y el valor de WHOOP se conserva en `*_whoop`. Las capturas de
> entrenamiento NO cuentan como reposo. Fuente `polar_h10` en `fuentes`.

### `workouts[]` — una fila por sesión
`fecha, inicio, fin, dur_min, deporte, strain, fc_prom, fc_max, kcal, km_whoop, fuente[, atleta]`
> `km_whoop` no es confiable en natación (ver OPP-01). El volumen real de nado va en `daily.swim_km`.
> `fuente` identifica el origen real: `whoop` (directo), `polar` (Polar Flow directo vía `polar_sync.py`),
> o la marca vía **agregador** (`polar`, `garmin`, `oura`, `fitbit`…). Con agregador/Polar directo,
> `km_whoop` guarda la distancia que reporta el dispositivo (sea la
> marca que sea) y `strain` viaja `null` (solo WHOOP lo calcula). `atleta` aparece cuando el workout
> viene por agregador (multi-atleta); se deduplica por `(fecha, inicio, deporte)`.

### `polar_capturas[]` — resumen de cada captura BLE del Polar
`archivo, sujeto, muestras, hr_prom, hr_max, rr_muestras`
> El sujeto sale del nombre del archivo (`polar_<sujeto>_...csv`) para no mezclar pruebas vs. Gael.

## Procedencia (3 ejes) — `software/provenance.py`

Inspirado en NOOP (columna `Source` + tabla `scoreInputProvenance`; ver dossier). Todo valor puede
llevar su procedencia para que el producto **nunca muestre un número sin saber de dónde salió**.

- **Eje 1 · Fuente** — `whoop_device` (BLE en vivo), `import_whoop`, `apple_health`, `polar`,
  `garmin`, `oura`, `fitbit`, `manual`, `tidmax` (calculado por nosotros).
- **Eje 2 · Tipo** — `medido` (sensor directo: HR, R-R) · `estimado` (derivado en dispositivo:
  temp de piel, respiración) · `importado` · `derivado` (nuestros scores) · `manual` ·
  `referencia` (score ajeno que solo guardamos como referencia).
- **Eje 3 · Confianza + Madurez** — madurez por nº de noches de baseline:
  `calibrando` (<4) → `construyendo` (<14) → `solida` (≥14).

**Reglas de honestidad (codificadas + con tests en `provenance.py`):**
1. **`no disponible ≠ 0`**: un dato ausente es `null`/`None`, jamás `0`. `marca(None, …)` → `None`.
2. **Scores ajenos = referencia**: el recovery/strain de WHOOP u Oura se guarda como `referencia`
   y **nunca gana** una fusión; recomputamos los nuestros (`tidmax`, tipo `derivado`).
3. **Degradación por capacidad de fuente**: cada fuente solo provee lo que puede —
   `polar` da HR+R-R en vivo pero **no** sueño profundo; WHOOP no da SpO₂ en vivo (necesita import).
4. **Fusión "mejor valor por métrica"**: `medido > manual > importado > estimado/derivado >
   referencia`, empatando por confianza, conservando la procedencia del valor elegido.
5. **Dedup por solape temporal**: una sesión auto-detectada que pisa una guardada/importada
   (incl. Apple Health) se omite.

## Reglas de normalización
- Fechas: todo a `YYYY-MM-DD`; horas de sesión en **hora local** (aplicando `timezone_offset`).
- Energía: kilojoules → kcal (×0.239).
- Fusión diaria: recovery/sueño/strain de WHOOP + nado del registro manual se unen por `fecha`.
- Campos ausentes = `null` (no romper si falta una fuente).
- `schema_version` viaja en el dataset para poder evolucionar sin romper a los agentes.

## Extensiones futuras
- `hr_stream[]` (Polar Etapa 2 / banda): FC latido a latido, PPG y ACC crudos → zonas de FC, TRIMP por
  sesión, splits, DFA-α1.
- `records[]` (nado): mejores tiempos por distancia (50/100/200/400…).
- Nuevas fuentes (Garmin/Apple/Samsung) → solo se agrega su normalizador; el esquema no cambia.
