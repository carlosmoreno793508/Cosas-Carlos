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

## Resumen de avance y presupuesto

Presupuesto INDICATIVO en USD (a validar con cotizaciones reales: RFQ H0.4, lab IFT R0.1, abogado IP H2.3).

| Fase | Track | Ítems | ✅ | Presupuesto (USD, indic.) |
|---|---|---|---|---|
| 0 · Fundación y datos | Software | 6 | 1 | $8k – $25k |
| 1 · Motor determinista | Software | 5 | 0 | $15k – $40k |
| 2 · Coach conversacional | Software | 5 | 0 | $12k – $35k |
| 3 · Beta software + B2B | Software | 4 | 0 | $20k – $50k |
| 4 · IA predictiva | Software | 3 | 0 | $25k – $60k |
| H0 · Spec + RFQ | Hardware | 4 | 1 | $2k – $8k |
| H1 · EVK primero | Hardware | 5 | 0 | $8k – $25k |
| H2 · ODM + molde + IP | Hardware | 4 | 0 | $20k – $70k |
| H3 · Beta de hardware (DVT) | Hardware | 5 | 0 | $30k – $80k |
| R0 · Regulatorio | Regulatorio | 6 | 0 | $10k – $35k |
| L · Lanzamiento comercial | GTM | 5 | 0 | $60k – $150k |
| **Total** | | **52** | **2** | **~$210k – $580k** |

### Presupuesto por bloque
- **Software (Fases 0–4):** ~$80k – $210k — *llega a beta cobrando; capital ligero*
- **Hardware (H0–H3):** ~$60k – $183k — *capital pesado, etapa 2*
- **Regulatorio (R0):** ~$10k – $35k — *barato pero bloqueante para vender*
- **Lanzamiento (L):** ~$60k – $150k — *inventario de arranque = el cheque más grande*
- **Punto medio de planeación:** ~$350k – $400k hasta lanzamiento.

**Regla de gasto:** no comprometer el capital pesado de hardware+lanzamiento (H2/H3/L, ~$110k–300k) hasta pasar el **go/no-go de H1.5** (EVK valida "mejor dato crudo"). El software valida y, idealmente, ya factura antes de ese cheque.

---

## FASE 0 — Fundación y datos (Software) · arranque

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 0.1 | Decidir Terra vs. Vital (criterio: acceso a IBI/RR crudo) | 🟡 | Recomendación NORTE: **Vital** para beta (cobro por-usuario, barato); **Terra** en banca por su Streaming API BLE (Polar H10). Abrir AMBAS cuentas gratis y comparar el JSON real. |
| 0.2 | Abrir sandbox del agregador + conectar primer atleta (WHOOP + Samsung) | 🟡 | Ruta alterna en marcha: **API directa de WHOOP** (app "GAEL SYNC" creada; código en `software/`, guía `guias/02`). Prueba para ver datos reales de Gael sin agregador. Incluye **dashboard en Excel** (`whoop_dashboard.py`). ⚠️ Hallazgo vigente: WHOOP y Samsung **NO exponen PPG/IBI crudo** por API/nube → el dato crudo para DFA-α1 vendrá del **EVK (H1)** o de correa BLE (Polar H10). 🆕 Hallazgo: WHOOP **no mide distancia de natación** (sin GPS en alberca) → registro manual en el dashboard + **oportunidad OPP-01** (ver `analisis/oportunidades-producto.md`). |
| 0.3 | Definir esquema de datos canónico (PPG/IBI/RR, HRV, sueño, SpO2, temp, carga) | 🟡 | v1.0 definido en `analisis/esquema-canonico.md` — el **contrato** entre ingesta y todo lo demás (dashboard, coach, agentes AI). Objetos `atleta`, `daily[]`, `workouts[]`, `polar_capturas[]`. Falta agregar `hr_stream[]` crudo (Polar Etapa 2 / EVK) y `records[]` de nado. |
| 0.4 | Infra mínima: repo, auth, base de datos de series de tiempo | ⬜ | |
| 0.5 | Pipeline de ingesta y normalización | 🟡 | v0 en `software/tid_data.py`: normaliza TODO lo crudo (WHOOP + Polar + registro de nado) al esquema canónico → `datos/procesado/dataset.json` (+ daily.csv/json, workouts.csv). Es lo que consumen los agentes AI. Probado: 29 días, 25 workouts. Falta base de datos de series de tiempo (0.4) para históricos. |
| 0.6 | NORTE — copiloto del proyecto | ✅ | PR #6 |

## FASE 1 — Motor determinista (Software)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 1.1 | Cálculo CTL/ATL/TSB (carga) | ⬜ | |
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
| 4.2 | Momento de pico / pronóstico de rendimiento | ⬜ | |
| 4.3 | Backtesting honesto (validado vs. hipótesis) | ⬜ | |

## FASE H0 — Spec + RFQ (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H0.1 | Congelar spec técnico (RFQ v2) | ✅ | Documento en `analisis/especificacion-pulsera-rfq.md` (RFQ v2, listo para cotizar). Specs verificadas 2026-08-02: nRF52840/nRF5340 y MAX86141 disponibles; ISO 22810:2010 y UN 38.3 vigentes. |
| H0.2 | Enviar RFQ a JointCorp, Vositone, Bingo, Star King | ⬜ | Ruta crítica — disparar ya |
| H0.3 | (Opcional) cotización India (Dixon/Optiemus) | ⬜ | |
| H0.4 | Recibir y comparar cotizaciones | ⬜ | |

## FASE H1 — EVK primero (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H1.1 | Ordenar 3–5 EVK (nRF52840/nRF5340 + MAX86141) | ⬜ | |
| H1.2 | Banco de pruebas óptico (puede arrancar YA, antes del EVK) | 🟡 | ✅ Confirmado en inventario: **Polar Verity Sense (Model 4J, WR50)** — óptico de brazo con PPG+ACC crudo por BLE SDK y FC bajo agua. Falta comprar **Polar H10 (~$105, referencia ECG)** + Scosche Rhythm24. Ver `analisis/bandas-dato-crudo.md` y `analisis/oportunidades-producto.md` (OPP-01). |
| H1.3 | Comparar calidad de dato vs. **Polar H10 (referencia ECG)** | ⬜ | WHOOP no sirve de referencia (dato cocinado). 🆕 Evaluar también **Garmin FR965 + HRM-Pro** como dispositivo de referencia (nado por IMU + RR crudo en FIT). Aprendizajes de ingeniería en `analisis/aprendizajes-fr965.md`; catálogo de métricas de nado en `analisis/metricas-nadadores-elite.md`. |
| H1.4 | Validar pipeline DFA-α1 sobre el óptico Polar (adelanta sin EVK) | ⬜ | Protocolo: reposo, esfuerzo, sudor/movimiento; RR del H10 como verdad |
| H1.5 | Decisión go/no-go de molde | ⬜ | No fundir molde sin esto |

## FASE H2 — ODM + molde existente + IP (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H2.1 | Auditoría + muestras + verificación de referencias del ODM | ⬜ | |
| H2.2 | Seleccionar ODM | ⬜ | |
| H2.3 | Contrato de IP granular (abogado) | ⬜ | No firmar manufactura sin esto |
| H2.4 | Confirmar uso de molde/plataforma existente | ⬜ | |

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

## FASE L — Lanzamiento comercial (GTM)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| L.1 | Inventario de arranque (MOQ ~500) | ⬜ | |
| L.2 | Empaque final + etiqueta NOM | ⬜ | Diseño de empaque pendiente |
| L.3 | GTM México | ⬜ | |
| L.4 | Expansión hispanohablante (Colombia, Chile, Argentina, Perú) | ⬜ | |
| L.5 | Brasil (etapa final) | ⬜ | Pix/Boleto + portugués + entidad local |
