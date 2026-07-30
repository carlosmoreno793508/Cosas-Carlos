# TID-MAX — Project Tracker

Seguimiento vivo del proyecto por fases e ítems. Se actualiza conforme avanzamos.

## Cómo se usa
- **Estado:** ⬜ Pendiente · 🟡 En progreso · ✅ Completo · ⚠️ Acción correctiva
- Al terminar un ítem, cambia su estado a ✅.
- Si un ítem se traba o sale mal, ponlo en ⚠️ y describe la **acción correctiva** en su columna.
- Una fase se marca **completa** cuando todos sus ítems están en ✅.

## Resumen de avance

| Fase | Track | Ítems | Completos |
|---|---|---|---|
| 0 · Fundación y datos | Software | 6 | 1 |
| 1 · Motor determinista | Software | 5 | 0 |
| 2 · Coach conversacional | Software | 5 | 0 |
| 3 · Beta software + B2B | Software | 4 | 0 |
| 4 · IA predictiva | Software | 3 | 0 |
| H0 · Spec + RFQ | Hardware | 4 | 1 |
| H1 · EVK primero | Hardware | 5 | 0 |
| H2 · ODM + molde + IP | Hardware | 4 | 0 |
| H3 · Beta de hardware (DVT) | Hardware | 5 | 0 |
| R0 · Regulatorio | Regulatorio | 6 | 0 |
| L · Lanzamiento comercial | GTM | 5 | 0 |
| **Total** | | **52** | **2** |

---

## FASE 0 — Fundación y datos (Software) · arranque

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 0.1 | Decidir Terra vs. Vital (criterio: acceso a IBI/RR crudo) | ⬜ | |
| 0.2 | Abrir sandbox del agregador + conectar primer atleta (WHOOP + Samsung) | ⬜ | |
| 0.3 | Definir esquema de datos canónico (PPG/IBI/RR, HRV, sueño, SpO2, temp, carga) | ⬜ | Pendiente #1 — es el contrato software↔hardware |
| 0.4 | Infra mínima: repo, auth, base de datos de series de tiempo | ⬜ | |
| 0.5 | Pipeline de ingesta y normalización | ⬜ | |
| 0.6 | NORTE — copiloto del proyecto | ✅ | PR #6 |

## FASE 1 — Motor determinista (Software)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 1.1 | Cálculo CTL/ATL/TSB (carga) | ⬜ | |
| 1.2 | HRV (rMSSD/SDNN) + DFA-α1 | ⬜ | |
| 1.3 | Zonas y umbrales personalizados | ⬜ | |
| 1.4 | Sueño + VO2max estimado | ⬜ | |
| 1.5 | Semáforo Preventivo v0 (vigilar→descarga→fisio) | ⬜ | |

## FASE 2 — Coach conversacional (Software)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| 2.1 | Integración LLM (Claude API) sobre las métricas | ⬜ | |
| 2.2 | Plan diario 5 pilares (entreno, sueño, hidratación, nutrición, recuperación) | ⬜ | |
| 2.3 | Modo adaptable Rendimiento ↔ Bienestar | ⬜ | |
| 2.4 | Guardrails COFEPRIS (rendimiento/bienestar, no diagnóstico) | ⬜ | |
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
| H0.1 | Congelar spec técnico (RFQ v2) | ✅ | Documento entregado |
| H0.2 | Enviar RFQ a JointCorp, Vositone, Bingo, Star King | ⬜ | Ruta crítica — disparar ya |
| H0.3 | (Opcional) cotización India (Dixon/Optiemus) | ⬜ | |
| H0.4 | Recibir y comparar cotizaciones | ⬜ | |

## FASE H1 — EVK primero (Hardware)

| # | Ítem | Estado | Acción correctiva / notas |
|---|---|---|---|
| H1.1 | Ordenar 3–5 EVK (nRF52840/nRF5340 + MAX86141) | ⬜ | |
| H1.2 | Banco de pruebas: PPG en bíceps y muñeca | ⬜ | |
| H1.3 | Comparar calidad de dato vs. WHOOP | ⬜ | |
| H1.4 | Correr pipeline Fase 1 sobre datos del EVK (validar DFA-α1) | ⬜ | |
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
