# Diseño del pod y la banda — mecanismo, materiales, desgaste y serviciabilidad

> Consolida las decisiones de diseño industrial del pod TID-MAX y su unión con la banda, discutidas con
> Carlos (2026-08). Alimenta el RFQ (`especificacion-pulsera-rfq.md`, §3/§8/§9). Marca **[decidido]** vs
> **[a confirmar por DFM]**. Render conceptual: ver el artifact de concepto visual.

## 1. Material del pod — polímero + bisel de aluminio  [decidido]
- **Cuerpo = polímero de ingeniería** (PC / PC+ABS o equivalente). Un cuerpo 100% aluminio actúa como
  **jaula de Faraday** (mata el BLE) y estorba al **sensor óptico** (reflejos/fugas), además de subir peso.
- **Aluminio solo como bisel/acento** premium (no bloquea RF ni óptico).
- Precedente: **WHOOP es todo polímero**; el metal (broche) vive en la correa, no en el pod.
- En el RFQ se escribe como **requisito funcional** (no se amarra la resina), igual que el SoC y el AFE.

## 2. Unión pod↔banda — sin pernos  [decidido]
- **Cero pernos / spring-bars.** El punto que se rompe en relojes tradicionales (Garmin: el perno de las
  asas) **no existe**. El pod **se aloja en un cradle** integrado a la banda.
- El **imán solo alinea y da el "clic"** + alinea los contactos de carga. **La retención es MECÁNICA**,
  no magnética (aunque el imán no existiera, el pod queda atrapado).

## 3. Dos conceptos de enganche

### Concepto A — Guía + traba (slide-lock)
Enganchas un lado del pod bajo una **guía/riel** y presionas el otro hasta el clic.
- La guía puede ser **metálica** (máxima durabilidad, premium) o de **plástico reforzado**.
- Casi no flexiona → **poco desgaste**. El más robusto. Más piezas/costo.

### Concepto B — Snap-fit (broche a presión)  [detallado]
Mecanismo clásico de wearables/carcasas; se basa en la flexibilidad del plástico.
1. **Alineación y empuje vertical:** el usuario alinea el pod y empuja **derecho** hacia abajo (sin
   deslizamiento previo).
2. **Flexión de las costillas:** en los bordes del cradle hay **costillas** de plástico flexible pero
   resistente (**POM / Nylon**) que se flexionan hacia afuera al bajar el pod.
3. **Clic y bloqueo:** el **hombro** del pod de aluminio tiene el perfil donde encajan las costillas; al
   bajar lo suficiente, las costillas **saltan** de vuelta y atrapan el pod bajo un reborde, con un
   **clic audible y táctil**.

**Pros ✅:** gesto intuitivo y rápido · **mucho más barato** que una guía metálica · menos piezas
(el mecanismo es parte de la misma banda).
**Contras ❌:** **mayor desgaste en la banda** (las costillas rozan el aluminio en cada inserción; con el
tiempo pierden fuerza de sujeción y el pod queda "suelto") · **riesgo de rotura** si el plástico es de
mala calidad o se vuelve quebradizo (una costilla rota inutiliza la banda).

## 4. Por qué el pod NO se desgasta (principio de diseño clave)
Aunque hay fricción, el **aluminio anodizado (metal duro)** del pod es mucho más resistente que las
**costillas de POM/Nylon (plástico blando)**. Es el principio del **cuchillo de acero sobre la tabla de
picar**: la tabla se raya y se gasta, el cuchillo queda intacto.
→ **La pieza de desgaste vive en la banda** (consumible barato); el **pod** (la pieza cara con
electrónica) tiene **vida útil larga**, libre de desgaste mecánico en su punto de sujeción.

## 5. Desgaste y serviciabilidad — la banda es consumible  [decidido]
- **Features de retención (costillas / guía) en la BANDA reemplazable**, nunca en el pod. El pod solo
  presenta su **hombro de aluminio** (pasivo, sellado, sin partes que flexionen).
- **Banda vendible por separado** como refacción barata (**modelo WHOOP / Apple**). El usuario **nunca
  vuelve a comprar el pod** por un desgaste — cambia una banda de pocos dólares.
- Beneficios: **ingreso recurrente** (colores/materiales/tallas) + historia de **sustentabilidad** (no se
  tira la electrónica).
- **Vida de inserción [a confirmar]:** especificar y **validar por prueba** (sugerencia: **≥ 5,000–10,000
  ciclos**), para que la fábrica lo garantice con número.

## 6. Retención bajo esfuerzo — no se suelta  [requisito de prueba]
Debe resistir **push-off de nado, carrera y contacto (básquet/soccer)** + una **prueba de caída**. Para
quitarlo se requiere una **acción deliberada** (presionar la lengüeta) que la fuerza del deporte no
reproduce. Se pide a la fábrica un **valor de fuerza de retención medible + método de prueba**.

## 7. Carga — imán al pod, sin quitarlo  [decidido]
- **Cargador magnético + cable USB-C** que se pega **solo al pod** (la banda no tiene electrónica).
- **No se saca el pod:** se carga **puesto en la banda**, incluso en la muñeca (como WHOOP) → nunca deja
  de medir (recovery 24/7).
- **Sin puerto abierto** → sigue **5 ATM + IP68**. Opciones: **pogo magnético** (oro duro) o **inductivo
  sellado** (a cotizar). **Sin adaptador de pared** (evita NOM-003-SCFI en México).

## 8. FC en vivo — la luz por zona  [feature nueva, ver agentes-ai / RFQ firmware]
- La **luz que respira cambia de color según la zona de FC en vivo** (idea de Gael): azul Z1 · verde Z2 ·
  ámbar Z3 · rojo Z4, anclado a sus umbrales (VT1 143 · VT2 167 · FATmax 173 · FCmáx 181). Sin pantalla,
  hasta bajo el agua.
- **[decidido] La luz vive SOLO en el anillo perimetral (breathing light). La cara del pod NO lleva LED
  central** — se mantiene limpia (look "Monolito Vivo"). Nota para fábrica y para renders/marketing: no
  agregar ningún punto/LED en el centro de la cara.
- **[decidido] Zona por VIBRACIÓN (háptico) — accesible.** El pod vibra **N veces según la zona** al
  **cambiar de zona**: Z1 = 1 vibración · Z2 = 2 · Z3 = 3 · Z4 = 4 (o buzz largo de alerta). Usa el
  **motor háptico (LRA)** que ya está en la spec → solo firmware. Sirve para **3 casos a la vez**: usuarios
  **ciegos / baja visión**, cualquiera que no quiere voltear a ver, y **bajo el agua** (donde luz y sonido
  fallan). El patrón exacto es afinable en pruebas.
- **Nota de accesibilidad:** un **altavoz/bip en el pod se descarta** (comprometería el sellado 5 ATM y no
  sirve bajo el agua). El canal accesible on-body es el **háptico**; opcional, **audio/voz a audífonos
  Bluetooth** vía app ("Zona 3") para uso en seco. Nicho real: **para-atletas con discapacidad visual**.
- Hardware casi sin costo (ya hay LED RGB + BLE); requiere **firmware**: FC básica en vivo → color, más
  **broadcast estándar de FC (BLE/ANT+)** y **aviso háptico por zona**. El dato crudo se sigue guardando.

## 9. Bandas — intercambiables  [decidido]
- **Tejida (textil, tipo SuperKnit): la deportiva principal** — ligera, seca, para nado/deporte.
- **Malla metálica (Milanese): banda lifestyle opcional.**
- Como el pod es intercambiable, se ofrecen **varias bandas** (WHOOP/Apple).

## 10. Requisitos que van al RFQ (checklist)
1. Carcasa del pod = **requisito funcional** (polímero de ing. + bisel de aluminio; RF baja + óptico limpio).
2. Unión **sin pernos**; **retención mecánica**; imán solo para alineación/clic.
3. **Features de desgaste en la banda reemplazable**, no en el pod (hombro de aluminio pasivo).
4. **Vida de inserción ≥ N ciclos** (def. 5,000–10,000) validada por prueba.
5. **Fuerza de retención medible** + prueba (nado/carrera/contacto/caída).
6. **Banda como refacción** (SKU vendible por separado); catálogo de bandas.
7. Carga **magnética sellada** (pogo/inductivo), sin puerto, sin adaptador de pared.
8. Firmware: **FC en vivo → luz por zona + broadcast BLE/ANT+ + háptico por zona**.
9. **Decisión de enganche:** A (guía) vs B (snap POM) — o **cotizar ambos** y decidir por costo/durabilidad.

## Relacionados
- `especificacion-pulsera-rfq.md` (RFQ — donde se formalizan estos requisitos)
- `estrategia-regulatoria-cofepris.md` · `agentes-ai.md` (FC en vivo / firmware) · `plataforma-multideporte.md`
