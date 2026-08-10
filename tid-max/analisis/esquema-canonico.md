# Esquema de datos canónico — TID-MAX (v1.0)

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
| hrv_ms | ms (rMSSD) | WHOOP |
| rhr_bpm | lpm | WHOOP |
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
| fuentes | [string] | qué fuentes aportaron ese día |

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
