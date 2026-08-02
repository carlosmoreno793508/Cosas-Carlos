# Perfil de Gael — análisis de estudios (tarea)

> Contiene datos de salud de Gael. Repositorio privado. La interpretación médica corresponde a su
> médico tratante; aquí se resume lo **relevante para entrenamiento, hidratación y nutrición**.
> Fuentes: (1) Prueba de esfuerzo cardiopulmonar — Somnia Sport Clinic, 26/01/2026. (2) Exámenes
> generales de laboratorio — OLAB / Estudios Clínicos Dr. T.J. Oriard, 30/01/2026.

## Datos generales
| Dato | Valor | Nota |
|---|---|---|
| Nombre | Moreno Sarmiento Carlos Gael | |
| Fecha de nacimiento | **19/03/2008** | **18 años** hoy (cumple 19 en marzo 2027). ✅ Confirmado. |
| Sexo | Masculino | |
| Tipo de sangre | **O Rh Positivo** | |

## Antropometría (⚠️ corrección importante)
| Dato | Valor | Nota |
|---|---|---|
| **Estatura** | **1.86 m** | Dato tuyo. El PE dice "Talla 2.08 m" pero **eso NO es su estatura**. |
| **Envergadura (brazada)** | **2.08 m** | Lo que el PE etiquetó como "Talla" es en realidad su **envergadura** (típico de nadador: brazada > estatura). |
| Peso | **81 kg** | Coincide en PE y WHOOP. |

→ **Acción**: en `nutricion-gael.json` ya puse estatura 1.86 m (para que el cálculo calórico no use 2.08 por error). En WHOOP conviene revisar que la "altura" no esté cargada como 2.08.

## Prueba de esfuerzo (26/01/2026) — lo más útil para el coach
- **VO₂pico: 67.75 mL·kg⁻¹·min⁻¹** → capacidad aeróbica **sobresaliente** (nivel élite de resistencia).
- **FC en reposo: 67 lpm** · TA reposo 100/80 · Frec. respiratoria 18.
- **FC máx alcanzada: 181 lpm** (test en **carrera**; teórica 203, llegó al 89%). En **nado** la FC máx suele ser ~5–10 lpm menor.
- **Recuperación cardiovascular**: FC 1' 169 · 3' 124 · 5' 116. Índice de Dorgo 17.6 → **"Área de mejora"** (reactivación vagal post-esfuerzo algo lenta).
- **ECG en reposo normal**: ritmo sinusal, sin isquemia ni hipertrofia.

### Umbrales fisiológicos (del test de carrera)
| Punto | FC (lpm) | VO₂ (mL/kg/min) | % VO₂pico | Ritmo (min/km) |
|---|---|---|---|---|
| VT1 (umbral aeróbico) | 143 | 43.9 | 65 % | 5:27 |
| VT2 (umbral anaeróbico) | 167 | 56.4 | 83 % | 4:17 |
| FATmax (máx. quema de grasa) | 173 | 61.4 | 91 % | 4:00 |
| VO₂pico (máx) | 181 | 67.75 | 100 % | 3:31 |

> **Corrección (ago-2026):** los rótulos VT1/VT2/FATmax estaban cruzados en una versión previa. Lo correcto (del PDF Somnia): **VT1 143 · VT2 167 · FATmax 173**. El FATmax está **por encima del VT2** (91 % VO₂) — hallazgo notable de alta flexibilidad metabólica que marca el propio laboratorio, no un error.

**Recomendación del reporte**: priorizar la **zona sensible entre VT1 y VT2** (FC ~143–167), con trabajo estratégico de umbral y alta intensidad; sumar aeróbico controlado y recuperación activa para mejorar la reactivación vagal.

## Exámenes de laboratorio (30/01/2026) — lectura para deporte
> Todo consistente con un **atleta joven sano de alta carga**. Los "fuera de rango" son en su
> mayoría adaptaciones de entrenamiento o hidratación, NO enfermedad (a confirmar con su médico).

**Bien / fortalezas:**
- **Perfil lipídico excelente**: colesterol 166, triglicéridos 65, HDL 57 (bueno), LDL 98. Índice aterogénico bajo.
- **Glucosa 88** (normal). Sin inflamación (PCR < 0.5). Inmunológico normal.
- **Hematología buena**: Hemoglobina 17.5, sin anemia, hierro sérico normal, saturación de transferrina 39 % → **buen estado de hierro** (clave para resistencia).

**A vigilar (señales de entrenamiento / hidratación):**
- 💧 **Señales objetivas de DESHIDRATACIÓN al momento de la muestra**: orina turbia, densidad ≥1.030 (muy concentrada), **cristales de urato amorfo abundantes**, y urea/BUN/creatinina ligeramente altas (urea 49, creatinina 1.28, TFG 82). → **Refuerza que la HIDRATACIÓN es una prioridad real, no genérica.**
- **Enzimas de origen muscular elevadas** por la carga de entreno: **CPK 677**, AST/TGO 51, ALT/TGP 58 (GGT y bilirrubina normales → origen muscular, no hepático). Normal en atletas tras entreno fuerte; vigilar que no se disparen con sobrecarga.
- **Hematocrito 50 % y Hb altos-normales**: buen transporte de O₂ (adaptación/altitud); otra razón para cuidar la hidratación.
- Albúmina 3.92 (ligeramente baja): probablemente hemodilución/hidratación; menor.

## Implicaciones para TID-MAX (propuestas para mañana)
1. **Antropometría**: estatura 1.86 m (hecho) · envergadura 2.08 m (dato de nadador) · revisar WHOOP.
2. **FC reales al motor**: reposo 67, máx ~181 (carrera). Definir **zonas por VT1 (143) / VT2 (167)** en vez de solo la teórica.
3. **VO₂máx 67.75** como baseline de forma para el 4º agente (Rendimiento).
4. **Hidratación**: el coach puede subir el peso de este pilar — hay evidencia de laboratorio de que Gael tiende a entrenar deshidratado.
5. **Nutrición**: el metabolismo de grasa/CHO del test (FATmax a 173 lpm, por encima del VT2 = quema grasa aun a alta intensidad) ayuda a afinar la estrategia de carbohidratos por intensidad.
6. **Edad**: 18 años (confirmado; cumple 19 en marzo 2027).

_Pendiente de revisar juntos mañana._
