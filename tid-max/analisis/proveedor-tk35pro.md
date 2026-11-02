# Expediente de proveedor — Shenzhen Tiankang Medical (TK35Pro → **TK36**)

> **Fecha:** 2026-11-02 · **Estado:** candidato fuerte. **Modelo elegido: TK36.** Falta (a) confirmar que el **RRI viene en el SDK gratis**, y (b) **validar una muestra** contra el Polar H10.
> Contacto: **Xuelian Liu** (sales). Canal: WhatsApp.
> Ligado a la guía `guias/09-sourcing-hardware.md` (checklist genérico) y a `analisis/competencia.md`.

---

## ⭐ Actualización 2026-11-02 — TK36 (modelo elegido) + fees aclarados

### Modelo elegido: **TK36** (no TK35Pro)
Recomendado por el proveedor para "mayor detección"; producción en masa desde oct-2026.
- **Sensor: 4PD** (4 fotodiodos) — **confirmado por foto y video** del reverso (4 ventanas + LED verde + contactos de carga). Sigue siendo **familia Goodix** (GH3220S+GH3220T), pero el 4PD es mejora óptica real (más captación / mejor rechazo de movimiento) + firmware más nuevo ("estilo WHOOP" = marketing, irrelevante porque corremos NUESTRO motor sobre el R-R crudo).
- **Batería 7–10 días** (vs 3–5 del TK35Pro). Mismo SoC JL7073A8, BLE 5.3, sin pantalla, IP68, mismo SDK (YCProductSDK).
- Video/foto confirman producto físico real y bien terminado (módulo delgado + correa nylon tejida).
- **Sin mínimo de muestras** (TK36 en stock) → se puede pedir **1 unidad**.

### Fees ACLARADOS (clave)
- **Integración del SDK = GRATIS si la hacemos nosotros** (somos técnicos → **$0**, sin el fee de $4,700 de soporte).
- **$7,600 USD = licencia de ACCESO A DATOS del PPG**, cobrada por su **software company** (no la fábrica). Ambos fees reembolsables a 10,000 unidades (política indefinida).
- **PREGUNTA ABIERTA (decisiva):** ¿el **RRI (R-R)** viene en el **SDK gratis**, y los $7,600 son **solo por la onda PPG cruda**? Si el RRI es gratis → **desarrollamos (y quizá lanzamos) con $0 de software**, porque el RRI solo alimenta `hrv_rr` (RMSSD/SDNN/HVC). El fee de PPG crudo se pagaría **solo si** queremos la onda cruda para nuestra propia detección gap-aware. *(Nuestro análisis del código del SDK apoya que el RRI es accesible sin candado; confirmar por escrito.)*
- **Sample rate:** el software company solo lo da tras ordenar muestra. **No es bloqueo** → lo **medimos nosotros** del PPG/RRI de la muestra.

### Estructura de la empresa
**Fábrica** (Shenzhen Tiankang Medical) + **su propio software company** (SDK/app, cobra el PPG) + **brazo comercial** (Shenzhen Hongyou Trading, el del catálogo). Normal en China; saber con quién negocias.

### Customización / cotización
- **Correas:** silicón $0.50/pza · piel $1/pza · tejida $0.50/pza — **MOQ $1,000 de valor** (≈1,000–2,000 pzas).
- **Banda custom desde cero:** la difieren — *"wait for the order to come in"* (no cotizan OEM a medida en especulativo). Falta el **precio del TK36 por volumen** (100/500/1,000).
- **Decisión v1:** **TK36 de stock + logo + correa con marca** (white-label), **sensor stock**. Packaging, sensor premium (Maxim/ADI = custom desde cero, caro, 1–2 meses) y **solar** → v2/más adelante.

### Siguiente paso
Enviar mensaje que: adopta **TK36**, confirma **RRI gratis vs PPG $7,600**, pide **1 muestra TK36** → validar R-R contra **Polar H10** con `software/valida_motor.py`. **Ese número decide.**

---

## Identidad del fabricante (consistente en TODOS los documentos)
- **Shenzhen Tiankang Medical Technology Co., Ltd** — Room 602, Building A5, Anle Industrial Zone, No.172 Hangcheng Avenue, Sanwei Community, Hangcheng Street, Bao'an District, Shenzhen.
- Fabricante real y documentado (no revendedor opaco). Buena señal.

## Producto: TK35Pro
- **Banda SIN pantalla** ("Screen-free ECG high-end smart health sports bracelet") → forma tipo WHOOP ✅ (foto en el reporte de seguridad: módulo + correa de nylon tejida + opción brazalete elástico).
- **BLE 5.3**. SoC **JL7073A8** (Jieli, económico). Acelerómetro **SC7A20H**. Temp **NTC** (termistor básico).
- **PPG: Goodix GH3228T + GH3220S** (HR/SpO₂, gama media de consumo).
- Batería **180 mAh, 3–5 días**, carga magnética, **IP68** (⚠️ no confirmado 5ATM para nado).
- App **HealthWear** (iOS 12+/Android 8+). OTA sí. Peso módulo ~23 g, con correa ~39 g.

### Banderas rojas (no usar en marketing)
- **Pseudociencia**: "glucosa no invasiva", "ácido úrico no invasivo", presión arterial óptica → no son precisas; señal de vendedor que sobrepromete.
- **Claims médicos** ("ECG + AI medical diagnosis / hospital-grade") **sin respaldo**: los certs entregados son de consumo, NO médicos. TID-MAX = **APROXIMADO, no diagnóstico** → no heredar el claim.

---

## Certificados revisados (5 docs — todos legítimos, NINGUNO médico)
| Documento | Cubre | Verificación |
|---|---|---|
| EU Declaration of Conformity (CE) | RED (radio) + EMC + RoHS | Fabricante consistente, firmado 17-abr-2025, lab CTB |
| FCC Grant | Radio EE.UU. (BLE 2.4 GHz) | **FCC ID 2BAXT-TK17** (ID de TK17, familia comparte radio), emitido por **Eurofins** (TCB) |
| RoHS Cert + Report | Sustancias (IEC 62321) | Nombra **TK35Pro**, lab Guangdong Zhonghan |
| Reporte seguridad eléctrica | **GB4943.1-2022** | **PASA**, lab **Honghui** acreditado **CMA/CNAS** |

**Conclusión certs:** set de compliance de **consumo** completo y legítimo. "Certificaciones domésticas" = seguridad/EMC/RoHS, **no** registro médico (NMPA). FDA/CE-MDR solo "en trámite (~jun próximo año)", no garantizado.

---

## Respuestas del proveedor (resumen)
1. **SDK gratis**, integrable con software de terceros. **Cobran por el PPG** + fee único de integración; **reembolsan ambos si pides 10,000 unidades**.
2–5. Specs + certs enviados.
6–7. OEM/ODM sí; costo según requerimientos (requiere discusión).
8. **Muestras/pedidos de prueba flexibles.** Bonus: **fee de muestra 100 % reembolsable en el primer pedido, incl. envío.**

---

## Análisis del SDK (YCProductSDK / "ycbt") — lo más importante

SDK **maduro y documentado** (framework iOS + `.aar`/`.so` Android + apps demo + **doc API en inglés y chino**, `Android_SDK_V1.0.5_EN.pdf`).

**Expone el dato crudo que TID-MAX necesita** (verificado en código/headers del SDK):
- **RRI (intervalos R-R)** — concepto de primera clase (×450 en el código) → **alimenta `software/hrv_rr.analiza_rr` directo**.
- **PPG crudo**: `settingPpgCollect`, `collectPpgDataWithTimestamp`.
- **ECG crudo**: `collectEcgDataWithTimestamp`, `collectEcgList` + algoritmos QRS/HRV (headers iOS `QRSDet.h`, `hrv_index.h`, `YCECGAlgorithmManager.h`, `ECGAnaly.h`).
- Colección en **tiempo real con timestamp** (`appStartMeasurement`, API `collect*`), SpO₂, FC.
- El "AI medical diagnosis" = **clasificador de ritmo del ECG** (fibrilación auricular, tipos QRS, taqui/bradicardia). → Para nosotros **referencia/APROXIMADO**, nunca claim médico.

**Gating del PPG:** **no se encontró** esquema de license/appKey/secret/unlock en el código (solo token BLE + permisos). → El "cobro por PPG" parece **comercial** (ellos lo habilitan/cobran), **no un muro técnico** → **negociable**.

> Binarios `.so` (p. ej. `libEcgAnaly.so`) cerrados — se usan tal cual. Nota: `libEcgAnaly.so` no soporta page size de 16KB en x86/x86-64 (irrelevante para dispositivos ARM reales).

---

## Veredicto
**El "make-or-break" (acceso al dato crudo) está DESTRABADO**: el SDK da RRI + PPG/ECG crudo en tiempo real, con doc. Sumado a fabricante real + certs de consumo + forma correcta + PPG Goodix decente → **candidato serio**.

## Pendientes (técnico/comercial, no papeleo)
1. **¿RRI gratis vs PPG de pago?** Si el **RRI** viene en el SDK gratis, puede que **no necesitemos pagar** el PPG (RRI solo ya da RMSSD/SDNN/HVC). Confirmar qué cubre y cuánto cuesta el fee de PPG + el de integración.
2. **Frecuencia de muestreo** del PPG/ECG crudo (para calidad / DFA-α1).
3. **¿Otras opciones de sensor** aparte de Goodix? (Maxim/ADI MAX86141, ADI ADPD, TI AFE49xx — mejor SNR para HVC en movimiento).
4. **¿5ATM** (nado) o solo IP68?
5. **Muestra** → grabar en paralelo con **Polar H10** y comparar R-R con `software/valida_motor.py`. **Ese número decide**, no el datasheet.

## Marco comercial
- **Dos tracks en paralelo:** (1) cotización OEM a medida (MOQ, precio @100/500/1000, NRE, lead time); (2) **1–2 unidades de stock ahora** para desarrollo.
- **Pedido de colaboración:** habilitar acceso crudo (PPG/RRI) **ahora** (waiver/descuento) a cambio de la relación, con intención de escalar a **10k+** a futuro (somos startup, 10k no es viable hoy).

## México (si se llega a vender aquí)
- Camino **wellness / APROXIMADO** → **evita COFEPRIS** (registro médico).
- Aún se necesitaría **IFT** (homologación de radio) + **NOM** (etiquetado/seguridad). FCC/CE ayudan pero no sustituyen.
