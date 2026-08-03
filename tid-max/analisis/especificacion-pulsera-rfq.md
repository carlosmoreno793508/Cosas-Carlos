# TID-MAX — Especificación técnica para cotización (RFQ) · Banda de rendimiento

**Documento:** RFQ v2.2 — Especificación de hardware para ODM/EMS
**Fecha:** 2026-08-03 · **Responsable:** Carlos Moreno (TID México) · carlos.moreno@tidmexico.com.mx
**Destinatarios objetivo:** JointCorp, Vositone, Bingo, Star King (China Tier-1) · alternativa India: Dixon/Dixtel, Optiemus
**Estado del proyecto:** Fase H0 (Spec + RFQ). El EVK (Fase H1) es previo al molde; ver §12.

> **Nota de uso.** Este documento es la fuente de verdad interna en español. Para el envío real a
> fábrica, mandar la versión en inglés (los términos técnicos ya van en inglés entre paréntesis para
> traducción directa). Cada requisito está etiquetado **[DURO]** (decisión congelada, no negociable
> salvo evidencia) o **[EST]** (estimación / objetivo a confirmar por DFM del fabricante). Las
> **preguntas abiertas para la fábrica** están consolidadas en §13.

---

## 1. Resumen del producto (product summary)

TID-MAX es una **banda de rendimiento deportivo de alto nivel** (high-performance sports band), **sin
pantalla y sin botones** (screenless, buttonless). Un **pod de aluminio** con sensor óptico se aloja
en un **loop tejido magnético intercambiable** (magnetic woven loop, quick-swap) y se usa en **muñeca
o bíceps**. Toda la interacción es por **app + doble toque + retroalimentación háptica**; una **luz
oculta que "respira"** en color es el único elemento visual. El valor del producto es la **calidad del
dato crudo** (raw PPG waveform + IBI/RR) que alimenta la IA predictiva en la nube — por eso el
requisito no negociable es el acceso a datos crudos, no a métricas cocinadas. **No es un wellness
band**: es un instrumento de medición para atletas.

**Lo que se cotiza es hardware "tonto pero preciso":** captura, almacena y transmite señal fisiológica
de alta fidelidad. **Toda la inteligencia (HRV, DFA-α1, carga, predicción) vive en la nube/app, NO en
el firmware.** El firmware solo adquiere, comprime, guarda y envía.

---

## 2. Modos de uso (wear modes) · [DURO]

| Modo | Ubicación | Uso principal |
|---|---|---|
| Muñeca (wrist) | Cara ventral/dorsal de muñeca | Uso 24/7, sueño, HRV en reposo |
| Bíceps (upper arm) | Brazo, sobre el bíceps | Esfuerzo/entrenamiento: PPG más limpio para HRV/DFA-α1 bajo movimiento |

El **mismo pod** debe funcionar en ambas posiciones cambiando solo el loop. El diseño óptico debe
priorizar señal limpia en **bíceps bajo movimiento y sudor** (caso de uso de esfuerzo), no solo en
reposo.

---

## 3. Form factor, dimensiones, materiales y acabado

| Ítem | Requisito | Etiqueta |
|---|---|---|
| Concepto | Pod sensor + loop tejido intercambiable (interchangeable band) | [DURO] |
| Dimensiones objetivo del pod | ~**32 × 28 × 11 mm** (envelope objetivo, a optimizar por DFM) | [EST] |
| Carcasa del pod | **Aluminio** (anodizado, grado a proponer) | [DURO] |
| Superficie | **Limpia, sin aberturas ni botones** (surface = mejor sellado, menos fallas) | [DURO] |
| Contacto con piel | Material biocompatible (skin-contact, ISO 10993 / hipoalergénico) | [DURO] |
| Loop / correa | **Tejido (woven), cierre magnético (magnetic clasp), intercambiable** | [DURO] |
| Tallas de loop | Rango muñeca + rango bíceps (al menos 2 largos) | [EST] |
| Peso objetivo | Lo más bajo posible; objetivo del pod ≤ ~25 g s/loop | [EST] |
| Color/acabado | Pod neutro (a definir); estética "Monolito Vivo" | [EST] |

**Pregunta clave a la fábrica:** ¿tienen **molde/plataforma existente** (existing tooling/platform)
cercano a este form factor que podamos usar para el beta y así minimizar NRE? (ver §11–12).

---

## 4. Sensores requeridos (sensors)

### 4.1 PPG óptico — **el corazón del producto** · [DURO]
- **Acceso a la onda PPG cruda (raw PPG waveform), muestreo ≥ 100 Hz**, además de intervalos
  **IBI/RR latido a latido** (beat-to-beat). **NO** se acepta solo HR/métricas cocinadas (cooked
  metrics). Sin dato crudo, la IA (DFA-α1, HRV) no funciona — **este es un criterio de descalificación
  del proveedor.**
- AFE óptico de referencia: **Analog Devices MAX86141 o equivalent-or-better** (AFE dual-channel,
  ADC 19-bit, cancelación de luz ambiental). No amarramos part number: se acepta cualquier AFE que
  entregue **raw waveform ≥100 Hz + IBI/RR** con acceso programable por el MCU.
- Configuración óptica (LEDs verde/rojo/IR y fotodiodos) a proponer por el fabricante para
  **señal limpia en muñeca y bíceps bajo movimiento**.

### 4.2 IMU — movimiento · [DURO]
- **Acelerómetro + giroscopio (6 ejes)**; se prefiere **9 ejes** (con magnetómetro) si no penaliza
  batería/costo. Se usa para detección de esfuerzo, clasificación de deporte y **conteo de largos de
  natación por IMU** (lap counting sin GPS — diferenciador documentado, ver `oportunidades-producto.md`).

### 4.3 Sensores opcionales (optional — cotizar por separado, marcar delta de costo)
- **SpO2** (pulse oximetry) — el MAX86141 lo soporta; confirmar viabilidad. *[Opcional]*
- **Temperatura de piel** (skin temperature sensor). *[Opcional]*
- **Sensor de profundidad / presión** (depth/pressure sensor, p. ej. TE **MS5837-30BA** ~3.3×3.3×2.75 mm,
  I²C, resolución ~2 mm de agua — *o equivalente*). Para análisis del **subacuático en natación**
  (profundidad de streamline/breakout y trayectoria del viraje) — diferenciador documentado, ver
  `analisis/subacuatico-diferenciador.md`. *[Opcional]* con **DOS condiciones [DURO]:**
  1. **SIN cambio de dimensiones del pod:** debe integrarse **dentro del envelope actual
     (~32×28×11 mm, §3) sin aumentar ninguna dimensión**. Si la plataforma del fabricante no lo permite
     sin crecer el case, **se descarta para el beta.**
  2. **SIN comprometer el sellado:** el puerto de presión (pressure port) debe mantener **5 ATM
     (ISO 22810) + IP68** (§9.1). Si compromete el sellado, se descarta.
- **ECG monocanal (single-lead ECG) — capacidad HARDWARE-READY (no se activa/reclama en v1).**
  Requiere un **AFE de ECG dedicado** (el MAX86141 **NO** hace ECG) + **electrodos** de contacto con
  piel. AFE de referencia: Analog Devices/Maxim **MAX30001** (ECG + bioimpedancia) *o equivalent-or-better*.
  Electrodos: p. ej. **electrodo en la carcasa trasera** (contacto en muñeca/bíceps) + electrodo(s)
  accesible(s) para lectura tipo spot-check. **Propósito:** dejar el dispositivo **listo para el Carril 2
  (médico)** sin rediseñar después — en v1 el producto es **deportivo/bienestar** y el ECG **NO** se
  anuncia ni se habilita (ver `analisis/estrategia-regulatoria-cofepris.md`). Mismas condiciones
  **[DURO]** que el sensor de profundidad: **sin crecer el envelope** y **sin comprometer 5 ATM + IP68**.
  Preferencia: **prever footprint/layout y electrodos ahora**, poblado o no en la primera corrida.
  *[Opcional · hardware-ready]*
- Los opcionales **no deben** bloquear el beta ni disparar NRE. Cotizarlos como add-on.

> **Sin GPS en la banda** [DURO]: mata batería, sube costo/tamaño y peso regulatorio. La distancia de
> nado se resuelve por IMU (lap counting), no por GPS.

---

## 5. SoC / MCU · [DURO por capacidad, no por part number]

Especificar **por capacidad mínima ("equivalent-or-better"), no amarrar part number.**

| Requisito | Mínimo | Referencia |
|---|---|---|
| RAM | **≥ 256 KB** | — |
| Flash | **≥ 512 KB** | — |
| Radio | **Bluetooth LE 5.x** (BLE) | — |
| Actualización | **OTA (over-the-air firmware update)** | — |
| Seguridad | **Secure boot + firmware cifrado/firmado** (secure boot, signed FW) | ARM TrustZone / CryptoCell o equiv. |
| SoC de referencia | **Nordic nRF52840** (1 MB flash / 256 KB RAM) o **nRF5340** (1 MB flash / 512 KB RAM, dual Cortex-M33) — **o mejor** | Disponibles en producción 2026 |

**Descartado:** nRF52832 (se queda corto en memoria para el buffering de dato crudo). Se acepta
cualquier SoC BLE que cumpla el piso de RAM/flash + OTA + secure boot.

---

## 6. Almacenamiento a bordo y modos de captura (store-and-forward) · [DURO]

- **Flash a bordo (on-board flash / NAND/NOR)** para **store-and-forward**: la banda **graba en memoria
  y sincroniza por BLE después**. Imprescindible porque **BLE 2.4 GHz no atraviesa el agua** (natación)
  y para no depender de conexión continua.
- **NO se pide streaming continuo 100 Hz por BLE 24/7** — rompe la batería. El streaming continuo solo
  aplica en modo entrenamiento/validación puntual.
- **Dos modos de captura:**
  1. **Ráfaga 24/7 (burst / duty-cycled):** ventanas de PPG crudo periódicas durante el día/sueño para
     HRV en reposo, con bajo consumo.
  2. **Entrenamiento continuo (continuous workout):** PPG crudo ≥100 Hz + IBI + IMU sostenido durante
     la sesión, guardado en flash y sincronizado al terminar.
- **Capacidad de flash [EST]:** dimensionar para **≥ varias horas de PPG crudo ≥100 Hz + IBI + IMU** sin
  sincronizar (caso de uso: sesión larga de nado). *Pregunta a fábrica: ¿cuánto buffer soporta su
  plataforma y con qué esquema de compresión?*

---

## 7. Batería y autonomía (battery) · objetivo por AUTONOMÍA, no por mAh

- **Objetivo de autonomía: 7–14 días** en uso mixto (ráfaga 24/7 + ~1 sesión de entrenamiento/día).
  **[DURO el objetivo de autonomía; el mAh es consecuencia, no requisito.]**
- **Capacidad estimada [EST]:** ~**80–110 mAh** LiPo en el envelope de §3 — a confirmar por el
  fabricante según su plataforma y consumo real.
- Química: **Li-Po / Li-ion recargable**, debe cumplir **UN 38.3** (ver §10).
- *Pregunta a fábrica: ¿qué autonomía real proyectan con su plataforma para nuestros dos modos de
  captura, y qué capacidad de celda recomiendan?*

---

## 8. Carga (charging) · [DURO]

- **Carga magnética sellada (sealed magnetic charging).** **SIN puerto abierto** en el dispositivo
  (no open port) — la superficie limpia es requisito de sellado.
- Dos opciones aceptables:
  1. **Pogo pins magnéticos** con **oro duro ≥ 20 µin (0.5 µm) sobre barrera de Pd/Ni** (hard gold
     ≥20 µin over Pd/Ni) para resistencia a corrosión/sudor.
  2. **Carga inductiva sellada** (sealed inductive/Qi-like).
- **Accesorio incluido:** solo **cable/base magnética con conector USB-C** (USB-C magnetic charging
  cable/dock). **SIN adaptador de pared (no wall adapter / no AC plug)** — evita la NOM-003-SCFI en
  México.
- *Pregunta a fábrica: ¿pogo o inductiva en su plataforma existente? Costo y confiabilidad de cada una.*

---

## 9. Agua, sellado, interacción y estética

### 9.1 Sellado (sealing / water) · [DURO]
- **5 ATM (50 m) conforme ISO 22810:2010** (versión vigente) — resistencia para natación/superficie.
- **IP68 (IEC 60529)** — polvo + inmersión.
- Sin puerto abierto (ver §8). La fábrica debe **validar y certificar** el sellado (ver §10, §12).

### 9.2 Interacción (interaction) · [DURO]
- **App (BLE)** como interfaz principal.
- **Doble toque (double-tap)** sobre el pod como entrada física (via IMU/tap-detect).
- **Retroalimentación háptica (haptic feedback)** — motor vibrador (LRA preferido).
- **Sin pantalla, sin botones mecánicos.**

### 9.3 Estética "Monolito Vivo" · [DURO como gancho, detalle [EST]]
- **Luz oculta que "respira" (hidden breathing light)** — LED(s) RGB bajo la superficie que se
  encienden en patrón/color. Oculta cuando está apagada (superficie limpia). A definir difusor/óptica
  con el fabricante.

---

## 10. Certificaciones que debe entregar la fábrica (compliance deliverables)

La fábrica **entrega los reportes/certificados; la homologación mexicana (IFT/NOM) la tramita TID**
(no es responsabilidad del fabricante). Se solicita a la fábrica:

| Entregable | Detalle |
|---|---|
| **Reportes RF** | Mediciones de RF del módulo/BLE (para soportar homologación **IFT / NOM-208-SCFI** en México) |
| **CE** (radio/EMC/salud) | Marca CE aplicable (RED) |
| **FCC** | FCC ID / reporte del módulo BLE |
| **RoHS** | Cumplimiento de sustancias |
| **UN 38.3** | Test summary de la batería Li (requisito de transporte, obligatorio desde 2020) |
| **Biocompatibilidad** | ISO 10993 del material en contacto con piel |
| **Reporte de sellado** | Evidencia de prueba 5 ATM (ISO 22810) + IP68 |
| Soporte de etiquetado | Datos para etiqueta NOM (ver §14): marca/modelo, país de origen, specs |

---

## 11. Propiedad intelectual (IP ownership) · [DURO — granular]

**Debe negociarse y quedar por escrito la propiedad de cada elemento por separado.** El contrato de IP
lo revisa/firma un abogado de IP (TID prepara requisitos; ver PROJECT-TRACKER H2.3). Para la cotización,
pedir a la fábrica su **postura sobre propiedad y licencia** de:

| Elemento | Nota |
|---|---|
| **PCB (diseño esquemático + layout)** | ¿Propiedad TID o licencia? |
| **Gerbers** (archivos de fabricación de PCB) | |
| **Firmware** (código de adquisición/BLE/OTA) | Crítico: acceso a dato crudo depende de esto |
| **Molde / tooling** (mecánico) | Distinguir molde existente (compartido) vs. custom (¿de quién?) |
| **CAD mecánico** (3D del pod/loop) | |
| **Bootloader** | Ligado a secure boot / OTA |
| **SDK** (para que la app lea el dato crudo) | Imprescindible para TID |
| **Software de test/calibración** (test & calibration) | |
| **Fixtures** de producción/prueba | |

> **Riesgo si no se define:** son fabricantes de marca blanca; por default la IP mecánica/firmware
> tiende a quedarse con ellos. Sin SDK + acceso a firmware/dato crudo, TID queda cautivo de un
> proveedor. **Negociar antes de fundir cualquier molde custom.**

---

## 12. Ruta EVK-primero (no fundir molde a ciegas)

**Antes** del molde y del piloto, TID valida la calidad del dato crudo con dev boards. Esto condiciona
la cotización:

1. **EVK primero (Fase H1):** **3–5 dev boards** (nRF52840/nRF5340 + MAX86141, p. ej. MAXREFDES103 o
   equivalente) para validar captura de **RR-intervals + DFA-α1** contra referencia ECG (Polar H10)
   **antes** de comprometer tooling.
2. **Go/no-go de molde (H1.5):** no se funde molde custom hasta que el EVK valide "mejor dato crudo".
3. **Beta con molde/plataforma existente:** para el piloto se usa el **molde/plataforma existente del
   ODM** para minimizar NRE. El objetivo del beta es **validar función y calidad de dato, no tooling
   custom.**

Por eso el RFQ pide cotizar en **dos tiempos**: (a) EVK/dev boards ya, y (b) piloto sobre plataforma
existente.

---

## 13. Cantidades a cotizar y price breaks (quantities & pricing)

Pedir a la fábrica cotización escalonada:

| Ítem | Cantidad | Propósito |
|---|---|---|
| **EVK / dev boards** | **3–5 unidades** (nRF + MAX86141) | Validación de dato crudo (Fase H1), antes del molde |
| **Piloto beta (DVT)** | **~20–50 unidades** | Beta con atletas reales (Fase H3) |
| **MOQ producción** | **~500 unidades** | Arranque comercial (Star King MOQ 500) |
| **Price breaks** | Cotizar **@500 / @1,000 / @5,000** | Curva de costo por volumen |

**Solicitar por cada nivel:**
- **Costo unitario (unit cost, FOB)** por volumen (500/1k/5k).
- **NRE / tooling** (ingeniería no recurrente): desglosar **molde existente vs. custom**.
- **Lead time**: muestras, tooling, producción.
- **Muestras (samples)**: costo y tiempo de golden samples / pre-producción.
- **DFM feedback**: recomendaciones de diseño para manufactura sobre este spec (form factor, batería,
  carga, sellado).
- **Confirmación explícita**: ¿pueden usar **molde/plataforma existente** para el beta y minimizar NRE?
  ¿Cuál plataforma y qué tan cerca queda del §3?

---

## 14. Etiquetado y empaque (labeling / packaging) — responsabilidad de TID, NO bloqueante

*Informativo para la fábrica; TID provee arte y textos. No condiciona la cotización técnica.*

- Etiqueta en **español** conforme **NOM-024-SCFI + NOM-050-SCFI**: denominación, marca/modelo, país de
  origen, **importador (domicilio fiscal en México)**, instructivo y **póliza de garantía**.
- Origen: etiquetar **"Ensamblado en México con componentes importados"** si aplica ensamble local;
  **"Diseñado en México"** como narrativa. "Hecho en México" es trámite aparte (no automático).
- La fábrica debe **soportar** el etiquetado con datos de producto y dejar espacio/área para etiqueta
  NOM en empaque.
- Empaque: a definir; sin adaptador de pared incluido (ver §8).

---

## 15. Resumen: DATO DURO vs ESTIMACIÓN

**[DURO] (congelado, criterio de descalificación si no se cumple):**
- Acceso a **PPG crudo ≥100 Hz + IBI/RR** (no solo métricas cocinadas).
- **Store-and-forward** con flash a bordo + 2 modos de captura.
- SoC **≥256 KB RAM / ≥512 KB flash + BLE 5.x + OTA + secure boot**.
- **5 ATM (ISO 22810) + IP68**, **sin puerto abierto**, **carga magnética sellada**, **sin adaptador
  de pared**.
- Sin pantalla / sin botones; pod aluminio + loop tejido magnético intercambiable; muñeca y bíceps.
- Objetivo de **autonomía 7–14 días**.
- IP granular negociada (§11).

**[EST] (objetivo / a confirmar por DFM):**
- Dimensiones ~32×28×11 mm y peso ≤~25 g.
- Capacidad de batería ~80–110 mAh.
- Capacidad de flash / horas de buffer.
- SpO2, temperatura de piel, **sensor de profundidad/presión** y **ECG monocanal hardware-ready**
  (opcionales, §4.3). El de profundidad y el ECG, solo si respetan el envelope actual **sin crecer el
  case** y **sin comprometer el sellado**. El ECG es capacidad a futuro (Carril 2 médico); en v1 no se
  habilita ni se anuncia (ver `analisis/estrategia-regulatoria-cofepris.md`).

**Preguntas abiertas para la fábrica (consolidadas):**
1. ¿Molde/plataforma existente cercana al form factor? ¿Cuál y qué NRE ahorra en el beta?
2. ¿Su AFE óptico entrega **raw waveform ≥100 Hz + IBI/RR** con acceso por SDK? (descalificante si no).
3. ¿Autonomía real proyectada por modo de captura y capacidad de celda recomendada?
4. ¿Cuánto buffer de flash y con qué compresión para PPG crudo + IMU?
5. Carga: ¿pogo (oro duro ≥20 µin/Pd-Ni) o inductiva en su plataforma? Costo/confiabilidad.
6. Postura de **propiedad y licencia** por cada elemento de IP (§11), en especial **SDK + firmware**.
7. Price breaks @500/1k/5k, NRE (existente vs custom), lead times y costo/tiempo de muestras.
8. **Sensor de profundidad opcional (§4.3):** ¿Integran un **sensor de presión/profundidad** con
   **puerto de presión sellado** manteniendo **5 ATM + IP68 Y el envelope actual sin crecer ninguna
   dimensión**? ¿Delta de costo, delta de NRE y rango/resolución (buscamos ~0–10 m, resolución cm)?
9. **ECG hardware-ready (§4.3):** ¿Pueden integrar un **AFE de ECG monocanal** (p. ej. MAX30001) con
   **electrodos** (electrodo en carcasa trasera + electrodo accesible) manteniendo **5 ATM + IP68 y el
   envelope sin crecer**? ¿Delta de costo/NRE con el AFE **poblado** vs. solo **dejar el footprint/layout
   previsto** (sin poblar)? Nota: es capacidad a futuro; en v1 no se habilita.

---

## 16. Fuentes (datos técnicos verificados 2026-08-02)

- Nordic nRF52840 (1 MB flash / 256 KB RAM, CryptoCell/TrustZone, BLE 5.x) — nordicsemi.com/Products/nRF52840
- Nordic nRF5340 (1 MB flash / 512 KB RAM, dual Cortex-M33, CryptoCell-312) — nordicsemi.com/Products/nRF5340
- Analog Devices MAX86141 (AFE óptico dual-channel, ADC 19-bit, WLP 20-pin) — analog.com/en/products/max86141.html
- TE MS5837-30BA (sensor de profundidad/presión, paquete **3.3×3.3×2.75 mm**, I²C, res. ~2 mm de agua,
  0–30 bar) — te.com / mouser.com/new/te-connectivity/te-ms5837-30ba
- Analog Devices/Maxim MAX30001 (AFE de **ECG monocanal + bioimpedancia**, ultra-bajo consumo; el
  complemento de ECG que el MAX86141 no cubre) — analog.com/en/products/max30001.html
- ISO 22810:2010 (resistencia al agua de relojes, versión vigente) — iso.org
- IP68 — IEC 60529
- UN 38.3 (UN Manual of Tests and Criteria, sec. 38.3; test summary obligatorio desde 2020) — intertek.com/batteries/un-38-3-testing
- Decisiones de producto: `.claude/agents/norte.md`, `analisis/bandas-dato-crudo.md`,
  `analisis/oportunidades-producto.md`, `PROJECT-TRACKER.md`.
