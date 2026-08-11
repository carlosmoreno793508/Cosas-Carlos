# TID-MAX — Project Tracker

Seguimiento vivo del proyecto por fases e ítems. Se actualiza conforme avanzamos.

## Cómo se usa
- **Estado:** ⬜ Pendiente · 🟡 En progreso · ✅ Completo · ⚠️ Acción correctiva
- Al terminar un ítem, cambia su estado a ✅.
- Si un ítem se traba o sale mal, ponlo en ⚠️ y describe la **acción correctiva** en su columna.
- Una fase se marca **completa** cuando todos sus ítems están en ✅.

## ⏳ Pendientes de aprobación (Carlos revisando)

Cambios que afectan datos del cliente y **no se aplican** hasta que Carlos apruebe.

| Tema | Qué falta aprobar | Estado | Doc |
|---|---|---|---|
| ~~Corrección umbrales VT1/VT2/FATmax~~ | **✅ APLICADO** (confirmado del PDF): 143=VT1, 167=VT2, 173=FATmax. Config, perfil, motor de zonas (reordenado VT1<VT2<FATmax) y tarjeta actualizados. | ✅ Hecho | `perfil-gael.md`, `nutricion-gael.json`, `tid_data.py`, `tid_cliente.py` |
| Estudio de sueño → integración | Aprobar rangos (Tabla A) y 2 lógicas: **%+minutos absolutos** y **"despertares" informativos**; luego cablear a motor/tarjeta/coach | ⏳ Carlos revisando | `analisis/estudio-sueno-gael.md` |

## 🧭 Decisiones estratégicas (aprobadas 2026-08-03)

Dirección de fondo tras 3 revisiones externas (ver `analisis/plataforma-multideporte.md`). **Aprobadas por Carlos.**

| # | Decisión | Implicación en el tracker |
|---|---|---|
| E1 | **TID-MAX = plataforma de rendimiento humano**, no "pulsera para nadadores". El activo es el motor de IA; la banda es el nodo de captura. | Reencuadre de GTM (Fase L) y de la narrativa de producto. |
| E2 | **Core universal + ediciones.** `TID-MAX Core` (PPG+IMU, todos los deportes de tierra) y `TID-MAX Aqua` (Core + sensor de profundidad, natación). Mismo PCB/carcasa. **Gael = design partner de Aqua.** | H0.1 (RFQ v2.1) · H1/H3 validan; el sensor de profundidad NO es requisito del core. |
| E3 | **IAs por deporte = especializaciones del patrón actual** (`tid_agent.py`): mismo motor, distinto system prompt + contexto. **Orden ajustado (pressure-test NORTE):** natación = **I+D + moat desde el día 1** con Gael (subacuático×recovery + patente), pero el **rollout comercial del software lidera con Running → Triatlón → Ciclismo** (más dato de terceros hoy; natación completa exige Aqua). Fútbol/básquet al final (peor caso de PPG en contacto). | Ítem **2.6**; roadmap en `analisis/roadmap-modulos-deporte.md`. |
| E4 | **Acelerar la IA de Rendimiento** (pico de forma/tapering) de "planeada" a **en desarrollo** — sirve ya al tapering de Gael y une natación/running/triatlón. | Ítem **4.2** elevado a prioridad. |
| E5 | **Gate #1 del hardware: validar PPG en BÍCEPS** (auto-gain, off-body, piel oscura, sudor). Sin esto, la ventaja multideporte se cae. Se evalúa con los primeros prototipos. | Nuevo ítem **H1.6** (gate). |
| E6 | **NO perseguir aún** mercado ocupacional/seguridad (bomberos, policía, militar, choferes): otra venta, otra regulación, roza "no medicina". | Fase 3+ (fuera de alcance del beta). |

## Resumen de avance y presupuesto

Presupuesto INDICATIVO en USD (a validar con cotizaciones reales: RFQ H0.4, lab IFT R0.1, abogado IP H2.3).

| Fase | Track | Ítems | ✅ | Presupuesto (USD, indic.) |
|---|---|---|---|---|
| 0 · Fundación y datos | Software | 6 | 1 | $8k – $25k |
| 1 · Motor determinista | Software | 5 | 0 | $15k – $40k |
| 2 · Coach conversacional | Software | 6 | 0 | $12k – $35k |
| 3 · Beta software + B2B | Software | 4 | 0 | $20k – $50k |
| 4 · IA predictiva | Software | 3 | 0 | $25k – $60k |
| H0 · Spec + RFQ | Hardware | 4 | 1 | $2k – $8k |
| H1 · EVK primero | Hardware | 6 | 0 | $8k – $25k |
| H2 · ODM + molde + IP | Hardware | 5 | 0 | $20k – $70k |
| H3 · Beta de hardware (DVT) | Hardware | 5 | 0 | $30k – $80k |
| R0 · Regulatorio | Regulatorio | 7 | 0 | $10k – $35k |
| L · Lanzamiento comercial | GTM | 5 | 0 | $60k – $150k |
| **Total** | | **56** | **2** | **~$210k – $580k** |

### Presupuesto por bloque
- **Software (Fases 0–4):** ~$80k – $210k — *llega a beta cobrando; capital ligero*
- **Hardware (H0–H3):** ~$60k – $183k — *capital pesado, etapa 2*
- **Regulatorio (R0):** ~$10k – $35k — *barato pero bloqueante para vender*
- **Lanzamiento (L):** ~$60k – $150k — *inventario de arranque = el cheque más grande*
- **Punto medio de planeación:** ~$350k – $400k hasta lanzamiento.

**Regla de gasto:** no comprometer el capital pesado de hardware+lanzamiento (H2/H3/L, ~$110k–300k) hasta pasar el **go/no-go de H1.5** (EVK valida "mejor dato crudo"). El software valida y, idealmente, ya factura antes de ese cheque.

---

## 🚀 Ecosistema en la nube — LIVE (hito 2026-08-05)

Migración de "script en la Mac de Carlos" a **producto autónomo en la nube.** Todo funcionando, probado end-to-end.

| # | Pieza | Estado | Notas |
|---|---|---|---|
| EC.1 | **Dashboard web** (`tid-max/web/`) | ✅ LIVE | Sitio estático data-driven (`index.html` lee `data.json`), diseño HD. Desplegado en **Vercel** (equipo `natacion-mx` Pro, root `tid-max/web`). **Link fijo 24/7 para la familia (Karla), sin Claude, sin túnel, sin la Mac.** Proteger con Deployment Protection. |
| EC.2 | **Puente pipeline→web** (`software/tid_web.py`) | ✅ | Convierte `coach-hoy.json` → `web/data.json`. Separa diseño de datos: actualizar el tablero = regenerar `data.json`. |
| EC.3 | **Automatización diaria** (`.github/workflows/tid-max-daily.yml`) | ✅ VERDE | **GitHub Actions, cron 8:30 am CDMX** (14:30 UTC). Corre WHOOP→datos→coach→web en la nube y hace commit de `data.json` (Vercel redespliega solo). Secrets: WHOOP_CLIENT_ID/SECRET/REFRESH_TOKEN, ANTHROPIC_API_KEY, GH_PAT (fine-grained, Secrets:write, para reguardar el refresh token que WHOOP rota). Probado 2026-08-05: commit `9554e8f` con datos reales del día. |
| EC.4 | **Regla de oro operativa** | ⚠️ | **La NUBE es el ÚNICO sincronizador de WHOOP.** Carlos NO debe correr `whoop_sync.py` en su Mac (pelea por el token rotativo). |
| EC.5 | Fase 3 del ecosistema (pendiente) | ⬜ | Subir foto/texto de comida sin Python (bot WhatsApp/Telegram o endpoint web) → procesar con Claude → actualizar consumo. Luego: notificación diaria automática (imagen/link) a Carlos y Karla. |

**Features de producto construidos hoy (2026-08-04/05):** sueño con **siestas** sumadas al total + deuda (tid_data.py), **horario de sueño** (acostarse→despertar), nutrición **día-consciente** (detecta sencilla/doble/descanso/taper, calibra el consejo) + genérica para futuros clientes, flag `--hora` para registrar comidas con su hora real.

---

## FASE 0 — Fundación y datos (Software) · arranque

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 0.1 | Decidir Terra vs. Vital (criterio: acceso a IBI/RR crudo) | 🟡 | Recomendación NORTE: **Vital** para beta (cobro por-usuario, barato); **Terra** en banca por su Streaming API BLE (Polar H10). Abrir AMBAS cuentas gratis y comparar el JSON real. **DECIDIDO (2026-08-10): arrancar con Junction (ex-Vital).** Polar directo se queda como respaldo gratis del R-R crudo del H10 (lo que el agregador no da). Falta: comparar el JSON real de workouts con las llaves de sandbox de Carlos. |
| 0.2 | Abrir sandbox del agregador + conectar primer atleta (WHOOP + Samsung) | 🟡 | Ruta alterna en marcha: **API directa de WHOOP** (app "GAEL SYNC" creada; código en `software/`, guía `guias/02`). Prueba para ver datos reales de Gael sin agregador. Incluye **dashboard en Excel** (`whoop_dashboard.py`). ⚠️ Hallazgo vigente: WHOOP y Samsung **NO exponen PPG/IBI crudo** por API/nube → el dato crudo para DFA-α1 vendrá del **EVK (H1)** o de correa BLE (Polar H10). 🆕 Hallazgo: WHOOP **no mide distancia de natación** (sin GPS en alberca) → registro manual en el dashboard + **oportunidad OPP-01** (ver `analisis/oportunidades-producto.md`). 🆕 **Fase 1 del agregador CONSTRUIDA (2026-08-10, PR #9):** `agregador_connect.py` (registra atleta + link "Conéctate" con logos, se manda por WhatsApp), `agregador_sync.py` (baja de TODOS los atletas, modelo pull, una API = todas las marcas), y `agregador_webhook.py` (scaffold del push/Svix para Fase 2). Espeja el flujo de Polar (connect→sync→normalizador). **Pendiente = Carlos: pegar `JUNCTION_API_KEY` + `JUNCTION_API_BASE` de su dashboard y correr el primer connect.** ✅ **HECHO Y PROBADO (2026-08-11):** cuenta Junction creada (TID Mexico, sandbox US), llaves en Vercel, y el flujo **"Conectar desde la app" verificado end-to-end en el iPhone** → widget de Junction cargó ("Success · device connected"). `api/connect.js` usa `link_web_url` que devuelve Junction. **Paso 1 de "todo por la app, cero Mac" COMPLETO.** Falta: (a) `GH_TOKEN` en Vercel para persistir el mapeo atleta→user_id; (b) paso 2 = sync automático en la nube (cron); (c) llaves de production para dato real de un reloj. 🆕 **(2026-08-11, nocturno):** `api/connect.js` pasa `redirect_url` (el "Continue" del widget regresa a la app con `?connected=<marca>` → toast); el **cron ya trae el paso de `agregador_sync.py`** (guardado, no rompe el pipeline verde de WHOOP si faltan llaves/atletas). **Pasos accionables de Carlos en `tid-max/PENDIENTE-CARLOS.md`.** |
| 0.3 | Definir esquema de datos canónico (PPG/IBI/RR, HRV, sueño, SpO2, temp, carga) | 🟡 | v1.0 definido en `analisis/esquema-canonico.md` — el **contrato** entre ingesta y todo lo demás (dashboard, coach, agentes AI). Objetos `atleta`, `daily[]`, `workouts[]`, `polar_capturas[]`. Falta agregar `hr_stream[]` crudo (Polar Etapa 2 / EVK) y `records[]` de nado. |
| 0.4 | Infra mínima: repo, auth, base de datos de series de tiempo | ⬜ | |
| 0.5 | Pipeline de ingesta y normalización | 🟡 | v0 en `software/tid_data.py`: normaliza TODO lo crudo (WHOOP + Polar + **agregador** + registro de nado) al esquema canónico → `datos/procesado/dataset.json` (+ daily.csv/json, workouts.csv). Es lo que consumen los agentes AI. Probado: 29 días, 25 workouts. 🆕 **(2026-08-10)** `build_workouts_agregador()` + `merge_workouts()`: los workouts del agregador entran al MISMO `workouts[]` con dedup por `(fecha, inicio, deporte)` y `fuente` = la marca real; probado con payload sintético de Junction. **Gaps abiertos:** (a) base de datos de series de tiempo (0.4) para históricos; ~~(b) normalizador Polar-directo → canónico~~ ✅ **CERRADO (2026-08-10):** `build_workouts_polar_flow()` ingiere `datos/polar_flow/<cuenta>/` al `workouts[]` canónico (parsea start-time/duration ISO8601/heart-rate, filtra los sub-recursos `_zonas_fc`/`_muestras`, `atleta` = cuenta, `fuente` = polar); probado con el básket real (6 min, 67/80) + un run (65 min, 12.3 km). (c) `daily[]` desde el agregador (sueño/actividad) — hoy solo mapea `workouts[]`. |
| 0.6 | NORTE — copiloto del proyecto | ✅ | PR #6 |

## FASE 1 — Motor determinista (Software)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 1.1 | Cálculo CTL/ATL/TSB (carga) | 🟡 | v0 en `tid_agent.py` (`carga_forma`): Fitness(CTL EWMA-42d) / Fatiga(ATL EWMA-7d) / Forma(TSB) sobre el **strain de WHOOP**. ⚠️ Honesto: es **proxy** (no TSS de potencia) → tendencia, no valor absoluto. Alimenta la IA de Rendimiento (4.2). Falta TSS real cuando llegue potencia/ritmo. |
| 1.2 | HRV (rMSSD/SDNN) + DFA-α1 | ⬜ | |
| 1.3 | Zonas y umbrales personalizados | ⬜ | |
| 1.4 | Sueño + VO2max estimado | ⬜ | |
| 1.5 | Semáforo Preventivo v0 (vigilar→descarga→fisio) | 🟡 | v0 por reglas en `software/tid_coach.py`: semáforo verde/amarillo/rojo combinando Recovery, HRV vs base, FC reposo vs base, sueño y ACWR (agudo:crónico). Corre sobre datos reales de WHOOP. |

## FASE 2 — Coach conversacional (Software)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 2.1 | Integración LLM (Claude API) sobre las métricas | 🟡 | v0 en `software/tid_agent.py`: lee el esquema canónico (`dataset.json`), el **motor** calcula los hechos duros y el **agente (Claude)** los convierte en coach conversacional. Regla de oro: el LLM no inventa números (código calcula, modelo interpreta). Modelo `claude-opus-5`, pensamiento adaptativo, fallback por reglas sin API key. Arquitectura en `analisis/agentes-ai.md`. Falta salida estructurada (Pydantic) y persona nombrada (2.5). |
| 2.2 | Plan diario 5 pilares (entreno, sueño, hidratación, nutrición, recuperación) | 🟡 | v0 por reglas en `software/tid_coach.py` (genera `reporte-diario.html`) **y** vía Claude API en `tid_agent.py` (ítem 2.1). |
| 2.3 | Modo adaptable Rendimiento ↔ Bienestar | 🟡 | v0: `software/tid_plan.py` genera el plan semanal (estilo Runna) con **adaptación diaria** — si el Recovery de WHOOP baja, cambia la sesión de hoy a recuperación/técnica. Falta el eje Rendimiento↔Bienestar explícito. |
| 2.4 | Guardrails COFEPRIS (rendimiento/bienestar, no diagnóstico) | 🟡 | v0: guardrails en el system prompt de `tid_agent.py` (no diagnóstico, no fármacos, no inventar datos, menor de edad, trazable). Documentados en `analisis/agentes-ai.md`. Falta suite de pruebas de los guardrails. |
| 2.5 | Nombrar y definir el asistente de usuario (persona) | ⬜ | |
| 2.6 | **Módulos de IA por deporte** (especializaciones de `tid_agent.py`) | ✅ | Decisión E3. Mismo motor fisiológico, distinto system prompt + contexto por deporte; el usuario elige deporte en su perfil. **Orden (roadmap NORTE):** 1) Running/Maratón · 2) Triatlón · 3) Ciclismo · 4) Natación/Aqua (I+D con Gael desde día 1) · 5) Fuerza/CrossFit · 6) Fútbol/Básquet. ✅ **Scaffold + los 7 módulos CONSTRUIDOS** (`tid_agent.py` sport-aware: `load_sport`/`build_system`/`--deporte`; `deportes/`: **natacion, running, triatlon, ciclismo, fuerza, futbol, basquet**). El motor no se toca; el módulo solo cambia persona + enfoque + prioridad de contexto. Probado (carga de los 7, reglas + selección/override + fallback a natación). **Alcance recortado con honestidad** en fuerza (readiness-first; sin VBT/1RM) y equipo (readiness + carga interna; **NO** PlayerLoad/saltos/GPS desde el brazo — R1/R4). Pendiente: validar con dato real de cada deporte y captar OUTCOMES para el moat (R3). Detalle: `analisis/roadmap-modulos-deporte.md`. |

## FASE 3 — Beta software + piloto B2B (Software)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 3.1 | App con 30–100 atletas reales | ⬜ | |
| 3.2 | 1 piloto B2B (equipo / universidad) | ⬜ | |
| 3.3 | Freemium + premium (cobro activo) | ⬜ | |
| 3.4 | Instrumentación de retención / engagement | ⬜ | |

## FASE 4 — IA predictiva (Software)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 4.1 | Modelos de riesgo de lesión / sobreentrenamiento | ⬜ | Requiere dataset acumulado de Fase 3 |
| 4.2 | Momento de pico / pronóstico de rendimiento (**IA de Rendimiento**) | 🟡 | **v0 CONSTRUIDO** (`tid_agent.py --rendimiento`): lee la Forma (CTL/ATL/TSB, ítem 1.1) + fase/días al evento y da estado de pico (en_pico / afinando / atrasado / construyendo) con lógica de taper, IA (Claude) + fallback por reglas. Probado con escenario de taper (TSB subiendo → "llegando fresco"). Sirve **ya** al tapering de Gael rumbo a Vancouver. Falta: TSS real (potencia/ritmo) y validación con más histórico. 5ª IA del producto. |
| 4.3 | Backtesting honesto (validado vs. hipótesis) | ⬜ | |

## FASE H0 — Spec + RFQ (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H0.1 | Congelar spec técnico (RFQ v2.3) | ✅ | **RFQ v2.3** (ES+EN, PDF) en `analisis/especificacion-pulsera-rfq.md`. Incorpora todo el diseño del pod/banda (`analisis/diseno-pod-banda.md`): carcasa **funcional (polímero + bisel)**, **unión sin pernos + retención mecánica**, desgaste en **banda reemplazable (SKU)**, **carga magnética al pod sin quitarlo**, **feedback en vivo** (luz por zona + **vibración N×zona accesible** + broadcast BLE HR/ANT+, on/off por doble-toque), sensor de profundidad + ECG **hardware-ready** (Carriles Aqua/médico), y **Compliance Matrix** (§13). |
| H0.2 | Enviar RFQ (correo NDA-first) a ODMs | 🟡 | **CORREOS ENVIADOS por Carlos (2026-08).** Flujo NDA-first (`correo-rfq-fabricas-EN.md`, Rev. B): Correo 1 = scope + NDA (sin adjunto) → NDA → RFQ. **Shortlist por fit** (`checklist-fabricas-rfq.md`): **J-Style/Jointcorp**, **Vositone**, **MOKOSmart**. Filtro clave = **raw PPG/IBI + SDK**. **Respuestas recibidas (2026-08):** ⬇️ ver H0.2a/H0.2b/H0.3. **Riesgo mitigado (2026-08-07):** ya hay **2 candidatos viables** — **Vositone** (H0.2a) y **VVDN** (H0.3, full-cycle) → poder de negociación. Seguir esperando 1-2 respuestas más. |
| H0.2a | **Vositone** (Jack Ho, sales@vositone.com) — ODM full-link + SDK | 🟡 | **CANDIDATO ACTIVO.** Confirma raw PPG ≥100 Hz + IBI/RR + IMU vía **SDK propietario**; acepta Mutual NDA; ODM full-link (NRE bajo, plataforma reusable). **🚩 Bandera:** su SDK exige **pago completo del fee ANTES** de validar/ver dato ("no free trial/partial/temporary access"). **Contra-respuesta ENVIADA por Carlos (2026-08-04, `correo-rfq-fabricas-EN.md` Correo 3):** NDA primero → **muestra/spec del SDK antes de pagar** → **costo del SDK** + qué incluye → **producto/plataforma existente como base de prototipo** (menos NRE) → **costo prototipos/EVK + NRE + MOQ** → fee **acreditable/escrow/reembolsable**. **Respuesta de Jack Ho (2026-08):** favorable — NDA mutuo OK, SDK fee 100% acreditable al NRE, plataforma existente + EVK disponibles; **pero NO da spec/muestra del SDK antes del pago**. En un correo posterior **pivoteó a ALIANZA COMERCIAL**: (1) referidos MX/LATAM (comisión por referido cerrado) y (2) usar la **decoración/impresión de TID México** para complementar sus productos aquí (piloto conjunto); pidió papeles de TID (razón social, RFC, acta, referencias, catálogo/precios). **Respuesta ENVIADA por Carlos (2026-08-07):** abierto a ambas direcciones; comparte legitimidad básica (razón social/RFC) pero deja **precios y referencias detrás del NDA con reciprocidad**, y **re-ancla el track TID-MAX** (ver SDK sample + costos por fase antes de comprometerse). **En espera de:** SDK sample + outlook de costos por fase. |
| H0.2b | **Nicholas Xu** (Sales Engineer) — EMS/CM puro | ⬜ (Fase 2) | **NO encaja etapa actual:** "we do not offer design/development, only manufacturing after designs ready". Es contract manufacturer, **sin plataforma/SDK/raw data**. **Archivado para Fase de producción** (fabricar diseño propio ya maduro). Correo de cortesía ENVIADO por Carlos (2026-08-04). Recontactar en H-producción. |
| H0.3 | **VVDN Technologies** (Kalpeshkumar Chauhan + Shruti Sahu) — ODM full-cycle | 🟡 **CANDIDATO ACTIVO (FUERTE)** | Ingeniería ODM real (no solo ensamble): **diseño + desarrollo + manufactura**; se declaran alineados con el enfoque por fases del RFQ. Diversificación de cadena (India). **Mutual NDA recibido y REVISADO (2026-08-07, `VVDN_MNDA_Draft_A001.docx`):** NDA mutuo **estándar y balanceado**, **IP protegida** (cláusula *No License* — no cede tu IP). 🚩 Banderas: (a) **ley/jurisdicción = India, Nueva Delhi**, excluye otras cortes → opción pedir **arbitraje neutral SIAC**; (b) cláusula **Independent Development** — pueden desarrollar wearables similares → no revelar la "salsa secreta" bajo solo NDA (la protección fuerte va en el contrato de manufactura/IP); (c) término 2 años + **5 años** de sobrevivencia de confidencialidad; (d) solo protege lo marcado "Confidential" (oral: confirmar por escrito en 30 días). **Respuesta ENVIADA por Carlos (2026-08-07)** acusando recibo del NDA. **Siguiente:** decidir firmar tal cual vs. pedir SIAC → firmar → **llamada de intro** (agenda con Kalpesh: costos por fase, roadmap técnico, EVK/SDK, IP, timeline EVT/DVT/PVT, experiencia wearables). **Pendiente:** definir **entidad firmante** (TID LLC vs. TID México). |
| H0.4 | Recibir y comparar cotizaciones + **Compliance Matrix** | ⬜ | Al llegar respuestas: firmar NDA → enviar RFQ v2.3 → reunión técnica → pedir **Compliance Matrix** (Compliant/Partial/Not/Alternative) para comparar ODMs objetivo. |

## FASE H1 — EVK primero (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H1.1 | Ordenar 3–5 EVK (nRF52840/nRF5340 + MAX86141) | ⬜ | |
| H1.2 | Banco de pruebas óptico (puede arrancar YA, antes del EVK) | 🟡 | ✅ Confirmado en inventario: **Polar Verity Sense (Model 4J, WR50)** — óptico de brazo con PPG+ACC crudo por BLE SDK y FC bajo agua. Falta comprar **Polar H10 (~$105, referencia ECG)** + Scosche Rhythm24. Ver `analisis/bandas-dato-crudo.md` y `analisis/oportunidades-producto.md` (OPP-01). |
| H1.3 | Comparar calidad de dato vs. **Polar H10 (referencia ECG)** | ⬜ | WHOOP no sirve de referencia (dato cocinado). 🆕 Evaluar también **Garmin FR965 + HRM-Pro** como dispositivo de referencia (nado por IMU + RR crudo en FIT). Aprendizajes de ingeniería en `analisis/aprendizajes-fr965.md`; catálogo de métricas de nado en `analisis/metricas-nadadores-elite.md`. |
| H1.4 | Validar pipeline DFA-α1 sobre el óptico Polar (adelanta sin EVK) | ⬜ | Protocolo: reposo, esfuerzo, sudor/movimiento; RR del H10 como verdad |
| H1.5 | Decisión go/no-go de molde | ⬜ | No fundir molde sin esto |
| H1.6 | **GATE #1 — Validar señal PPG en BÍCEPS** (auto-gain / corriente LED dinámica / off-body / **piel oscura** / sudor) | ⬜ | **Decisión E5. Prioridad #1: condiciona toda la tesis multideporte** (§9.2 del RFQ). Sin buena PPG en bíceps bajo movimiento, se cae la ventaja en deportes de tierra. Se evalúa con los **primeros prototipos/EVK**. |

## FASE H2 — ODM + molde existente + IP (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H2.1 | Auditoría + muestras + verificación de referencias del ODM | ⬜ | |
| H2.2 | Seleccionar ODM | ⬜ | |
| H2.3 | Contrato de IP granular (abogado) | ⬜ | No firmar manufactura sin esto |
| H2.4 | Confirmar uso de molde/plataforma existente | ⬜ | |
| H2.5 | **"Hardware-ready" para lo médico — ECG incluido en el layout** | 🟡 | Estrategia de 2 carriles (R0.7). **DECIDIDO (2026-08-03): incluir AFE de ECG dedicado (ref. MAX30001) + electrodos** como capacidad hardware-ready. Ya en RFQ v2.2 §4.3 (opcional, sin crecer case, sin comprometer 5 ATM+IP68). En v1 **no** se habilita/anuncia. Pedir a fábrica delta de poblar vs. solo footprint. Doc: `analisis/estrategia-regulatoria-cofepris.md`. |

## FASE H3 — Beta de hardware / DVT (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H3.1 | 20–50 unidades DVT para atletas de beta | ⬜ | |
| H3.2 | Firmware: store-and-forward, OTA, secure boot | ⬜ | |
| H3.3 | Validar 5 ATM (ISO 22810) + carga magnética sellada | ⬜ | |
| H3.4 | Validar autonomía 7–14 días | ⬜ | |
| H3.5 | Importación como muestras / I+D (agente aduanal) | ⬜ | |

## FASE R0 — Regulatorio (bloquea la venta, no el beta)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| R0.1 | Contratar lab de homologación IFT | ⬜ | |
| R0.2 | Homologación IFT (NOM-208-SCFI) | ⬜ | |
| R0.3 | Etiquetado NOM-024 + NOM-050-SCFI (español) | ⬜ | |
| R0.4 | Definir etiqueta de origen ("Ensamblado en México") | ⬜ | |
| R0.5 | Registrar marca TID-MAX (IMPI) | ⬜ | |
| R0.6 | Recabar certificados del fabricante (CE/FCC/RoHS/UN38.3) | ⬜ | |
| R0.7 | **Estrategia de dos carriles + claims de producto** | 🟡 | Decisión 2026-08-03: **Carril 1 = deportivo/bienestar** (sin registro médico COFEPRIS) para v1/beta; **lo médico = Carril 2, etapa posterior**, PERO el **hardware se diseña ya "listo para lo médico"** ("hardware-ready, claim-gated"). **NO reclamar "grado médico"** ni diagnóstico. **Temperatura = opcional.** Datos de salud → **LFPDPPP** (aviso de privacidad, aplica desde v1). Confirmar con especialista regulatorio antes de lanzar. Doc: `analisis/estrategia-regulatoria-cofepris.md`; ver también `plataforma-multideporte.md §2` y guardrails 2.4. |

## FASE L — Lanzamiento comercial (GTM)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| L.1 | Inventario de arranque (MOQ ~500) | ⬜ | |
| L.2 | Empaque final + etiqueta NOM | ⬜ | Diseño de empaque pendiente |
| L.3 | GTM México | ⬜ | |
| L.4 | Expansión hispanohablante (Colombia, Chile, Argentina, Perú) | ⬜ | |
| L.5 | Brasil (etapa final) | ⬜ | Pix/Boleto + portugués + entidad local |
