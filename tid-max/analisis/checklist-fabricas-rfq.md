# Checklist de contacto a fábricas — RFQ v2.2 (H0.2)

> A quién contactar, por qué canal, y en qué orden. Datos verificados por web 2026-08-03. **No incluyo
> correos "inventados":** donde no hay un correo público verificable, el canal correcto es el
> **formulario del sitio oficial** o su **tienda B2B** (Alibaba/GlobalSources), pidiendo que te enlacen
> con ventas/ingeniería. Adjuntar a cada uno: `RFQ_TID-MAX_v2.2_EN.pdf`; NDA a la mano.

## Qué mandar a cada fábrica
- **Correo:** la plantilla de `correo-rfq-fabricas-EN.md` (personaliza el contacto).
- **Adjunto:** `RFQ_TID-MAX_v2.2_EN.pdf`.
- **A la mano:** el NDA (por si piden firmar antes de detalle técnico).
- **Filtro #1 (que respondan primero):** ¿su AFE óptico entrega **raw PPG ≥100 Hz + IBI/RR con SDK**? Si
  no, se autodescartan y no pierdes tiempo.

## Prioridad y fit

| # | Fábrica | Qué es (verificado) | Fit con TID-MAX | Canal |
|---|---|---|---|---|
| ⭐ 1 | **JointCorp** (Joint Chinese Group / Shenzhen Youhong / J-Style) | ODM desde 2004; **hace screenless smart bands**, monitores de FC 24 h, smart rings. **ISO 13485 + FDA + ISO 9001/14001.** Clientes: Tanita, Citizen, Walmart, Target. | **El mejor match.** Ya fabrica **bandas sin pantalla** (tu form factor exacto) y tiene **ISO 13485** (clave para tu Carril 2 médico). | `jointcorp.com` (formulario) · `jointcorp.en.alibaba.com` · GlobalSources "Joint Chinese Ltd" |
| ⭐ 2 | **Vositone** | ODM de smartwatch/fitness bands desde 2010, Shenzhen; 300+ empleados, 600k u/año; **CE/FCC/ISO**; vertical **healthcare**. Top-5 OEM de smartwatch en China. | **Muy fuerte.** Experiencia en fitness bands + vertical salud; defect rate <0.3%. | `vositone.com` (About/Contact) |
| 3 | **Bingo** (Bingo Electronics / SZ Bingo Group) | ODM de smart band/watch/ring/glasses; **MOQ bajo**, CE/RoHS. | **Bueno para el beta** (MOQ bajo = piloto barato). Confirmar acceso a dato crudo. | `szbingogroup.com` |
| ⚠️ 4 | **Star King** — *verificar* | Ambiguo. Lo más cercano en smart-wearables es **Kingwear** (`king-wear.com`, Shenzhen Kingwear, smartwatch ODM). "Shenzhen Jieyong **Starking** Clocks & Watches" es de **relojes tradicionales** (no smart) → probablemente **no** es el correcto. | **Aclarar antes de contactar.** Si tu "Star King MOQ 500" venía de un contacto puntual, usa ese; si no, evalúa **Kingwear** en su lugar. | Verificar cuál es. Kingwear: `king-wear.com` |

## Orden recomendado de disparo
1. **JointCorp** y **Vositone** primero (los dos mejores fits, en paralelo).
2. **Bingo** como tercera cotización (ancla de precio + MOQ bajo para beta).
3. **Star King:** resolver identidad; si no se aclara, sustituir por **Kingwear** o dejar solo 3.
> Regla: **mínimo 3 cotizaciones** para comparar (H0.4). Con JointCorp + Vositone + Bingo ya tienes 3 sólidas.

## Después de enviar (seguimiento)
- Sin respuesta en ~1 semana → recordatorio breve.
- Prioriza a quien **confirme raw PPG + SDK** (descalificante).
- Registra respuestas en `PROJECT-TRACKER.md` (H0.2 → H0.4): fecha de envío, respuesta, ¿cumple dato crudo?,
  costo EVK, NRE, lead time.

## Fuentes (verificado 2026-08-03)
- JointCorp — jointcorp.com/about-us · jointcorp.en.alibaba.com · globalsources (Joint Chinese Ltd)
- Vositone — vositone.com/about.html
- Bingo — szbingogroup.com
- Star King / Kingwear — king-wear.com · made-in-china (Jieyong Starking, relojes tradicionales)
