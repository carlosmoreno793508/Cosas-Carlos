# Athyx — Reverse Engineering Comercial (Dossier de Inteligencia Competitiva)

**Autor:** NORTE (copiloto TID-MAX) para Carlos Moreno · **Fecha:** 2026-08-28
**Objetivo:** entender qué es realmente Athyx (FLUX I / OBLA I), separar hecho de marketing, y decidir
la jugada de TID-MAX. **No** copiar a Athyx.

> **Nota de método:** Investigación vía WebSearch (el proxy bloquea WebFetch a varios dominios:
> athyx.com devolvió 403, nature.com y pubmed pidieron cookies/login). Donde no pude verificar el dato
> primario, lo marco como **[NO VERIFICADO]** o **[ESTIMACIÓN]**. Los precios exactos del sitio de
> Athyx **no** se pudieron confirmar (página bloqueada al scraping) — marcados abajo.

---

## Resumen de la confusión de marca (contexto crítico)
Athyx vende **dos aparatos que la gente mezcla**, y el marketing ayuda a la confusión:

- **FLUX I** = lo que **se vende hoy**. Parche/banda de brazo **sin batería (battery-free, NFC)** que
  lee **sudor** y toma la **FC de la cámara del teléfono**; un algoritmo **estima** lactato. Optimizado
  para **caminadora (treadmill)** y "modelo noruego". **No es láser.**
- **OBLA I** = el **aspiracional/premium**. Aquí aparece la narrativa **"quantum laser technology"**
  ("world's first laser-based lactate wearable"). Lanzamiento anunciado **julio 2026** (aún no en manos
  de usuarios de forma verificable). "OBLA" = *Onset of Blood Lactate Accumulation* (umbral ~4 mmol/L).

Fuentes: [Athyx – FLUX I](https://www.athyx.com/product/flux) · [Athyx – OBLA I](https://www.athyx.com/product/obla) · [Athyx – home](https://www.athyx.com/)

---

## 1. Qué sensor/tecnología usa CADA producto

**FLUX I (real, a la venta):**
- Sensor de **composición de sudor** en la banda de brazo, alimentado por **NFC** (sin batería): la
  energía la toma del campo NFC del teléfono en el momento del escaneo. Lectura **por escaneo NFC**, no
  streaming continuo.
- **FC desde la cámara del teléfono** (fotopletismografía por cámara) o, para "mayor precisión", una
  **banda de FC Bluetooth vendida aparte**.
- Un **algoritmo** combina señal de sudor + FC + modelo (caminadora / "modelo noruego") → **estimación**
  de lactato y de tasa de sudoración. Athyx describe explícitamente "estimate lactate", no medición
  directa en sangre.

**OBLA I (aspiracional):**
- Marketing declara **"quantum laser technology"** + **LEDs de alta intensidad** para FC/oxígeno,
  y sensores de "lactato, potencia, FC, temperatura central, sudor y oxígeno". Continuo, IP68.
- La parte "láser" es la única diferencia física relevante frente a FLUX; el resto (LED PPG, temp) es
  wearable estándar.

Fuentes: [FLUX I](https://www.athyx.com/product/flux) · [OBLA I](https://www.athyx.com/product/obla)

---

## 2. Quién fabrica realmente el módulo sensor/láser

- **FLUX I (sudor + NFC):** consistente con un **parche electroquímico/microfluídico NFC** de marca
  blanca; Athyx aporta app + algoritmo. No hay evidencia pública de que Athyx fabrique silicio propio.
  El know-how "battery-free skin-interfaced microfluidic + NFC" es tecnología académica madura y
  licenciable (líneas tipo Rogers Lab / Epicore Biosystems). **[PARCIALMENTE VERIFICADO]** — Athyx no
  publica su cadena de suministro.
- **OBLA I (láser):** apunta a la alianza **"Starleet × Athyx"** ([starleet.com](https://www.starleet.com/)).
  Según PitchBook, **Starleet** es una startup de **Copenhague, Dinamarca, fundada en 2024**, de
  "wearables de IA personalizados para manejo de estrés, tecnología ultradelgada en el brazo que detecta
  lactato". Starleet aportaría la tecnología óptica/IA; Athyx la marca deportiva.
  ([PitchBook – Starleet](https://pitchbook.com/profiles/company/756628-84))
- **El módulo láser en sí** casi seguro sería un **QCL/óptica mid-IR de un OEM externo** (ver §8), no
  fabricado por Athyx ni por Starleet. **[NO VERIFICADO]** — ninguna de las dos publica proveedor.

**Lectura NORTE:** Athyx es principalmente **software + integración + marca**, montada sobre parches de
sudor de terceros (FLUX) y, para OBLA, sobre óptica de un socio/OEM que **aún no se demuestra en un
form factor de muñeca**.

---

## 3. Principio físico/químico de cada uno

**FLUX I — electroquímica de sudor (plausible y real):**
- Sensor enzimático amperométrico: **lactato oxidasa (LOx)** + mediador (ej. Azul de Prusia) sobre
  electrodos serigrafiados; microfluídica en papel/hidrogel para transportar sudor. Es tecnología
  bien documentada y funcional. ([ACS Sensors – wearable sweat lactate](https://pubs.acs.org/doi/10.1021/acssensors.3c00708) · [Frontiers – narrative review](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2024.1376801/full))
- **Pero** Athyx dice usar "sweat signals" + FC para **estimar** — puede que ni siquiera mida lactato
  enzimático directo, sino que infiera desde electrolitos/tasa de sudor + FC + modelo. Nótese que la
  literatura de "umbral por sudor" más citada mide **Na+/K+**, no lactato (ver §6). **[AMBIGÜEDAD real
  en el claim de Athyx.]**

**OBLA I — espectroscopía mid-IR con QCL (físicamente posible, pero brutal en muñeca):**
- Un **Quantum Cascade Laser** emite mid-IR (~8–11 µm); las biomoléculas (glucosa, lactato) absorben
  en esa banda y se lee el espectro (fototérmico/fotoacústico). Es la vía que persiguen DiaMonTech y
  grupos de glucosa no invasiva. ([Ophir – DiaMonTech M-IR](https://www.ophiropt.com/en/a/blood-glucose-monitor) · [Sci Reports – dual QCL photoacoustic glucose](https://www.nature.com/articles/s41598-023-34912-3))
- **Problema de física:** el mid-IR **penetra micras** en piel (mide fluido intersticial superficial,
  no "sangre"), es sensible a temperatura/presión/sudor, y **discriminar lactato de glucosa/albúmina
  es difícil** (se usan como interferentes mutuos en los papers). Raman sería la alternativa, con señal
  aún más débil.
- **Plausibilidad de "quantum laser en la muñeca 24/7": muy baja hoy.** Ver §10 (un módulo QCL OEM pesa
  ~1 in³ y cuesta ~US$100k). El claim "world's first laser-based lactate wearable" está en zona de
  **hype** hasta ver hardware y datos.

---

## 4. ¿Mide sudor, lactato intersticial, o estima?

| Producto | Qué toca | Qué reporta | Naturaleza |
|---|---|---|---|
| **FLUX I** | **Sudor** (superficie de piel) + FC de cámara | Lactato "equivalente" + tasa de sudor | **Estimación algorítmica** (no sangre) |
| **OBLA I** | **Intersticial superficial** vía óptica mid-IR (claim) | Lactato + O2 + temp + potencia | **Medición óptica indirecta** (claim, no validada) |

Ninguno mide **lactato en sangre**. FLUX es explícitamente **estimación**. OBLA sería medición
intersticial óptica, no sangre — y **[NO VERIFICADA]**.

---

## 5. Frecuencia de medición y latencia

- **FLUX I:** **por escaneo NFC** (discreto, el usuario acerca el teléfono), no continuo autónomo.
  Protocolo publicitado: sesiones tipo **4×10 min en caminadora**. **No** hay flujo 24/7 propio (no
  tiene batería).
- **OBLA I:** se anuncia **continuo**. **[NO VERIFICADO]** frecuencia real.
- **Latencia sudor↔sangre:** intrínseca del método. El lactato en sudor **va con retraso y no es 1:1**
  con el sanguíneo; depende de tasa de sudoración, zona corporal, aclimatación y contaminación de
  glándula. En arranque de ejercicio el sudor tarda en "cargar". Esto es un **límite físico**, no
  resoluble por firmware. (Contexto: [PMC – narrative review sweat lactate](https://pmc.ncbi.nlm.nih.gov/articles/PMC11025537/))

---

## 6. Precisión vs lactato sanguíneo — ¿hay validación revisada por pares?

**Para el dispositivo de Athyx específicamente: NO encontré ninguna publicación revisada por pares
que valide FLUX I ni OBLA I contra lactato sanguíneo.** Athyx cita "moderate accuracy" en su propio
sitio, sin estudio.

**Cuidado con una confusión frecuente:** el paper de *Scientific Reports* 2025 "Feasibility study of a
novel wearable sweat sensor for anaerobic threshold determination" **NO es de Athyx**. Autores **Luo Z,
Cao M, Yan L, Wang J**; usaron el analizador **AbsoluteSweat brush-chip** midiendo **Na+/K+** (no
lactato) en test de ciclismo. Hallazgo: correlación con umbral de lactato **moderada y solo en
atletas entrenados/medios; falla en poco entrenados**. Buen soporte para el *concepto* "umbral por
sudor", pero **no valida a Athyx** y ni siquiera mide lactato.
([Nature s41598-025-16559-4](https://www.nature.com/articles/s41598-025-16559-4) · [AZoSensors resumen](https://www.azosensors.com/news.aspx?newsID=16595))

**Conclusión §6:** validación científica de Athyx = **inexistente públicamente**. El género (sudor→umbral)
tiene soporte **parcial y dependiente del nivel del atleta**. **Bandera roja de rigor.**

---

## 7. Patentes de Athyx / Peter Tran

- **No encontré ninguna patente concedida ni solicitud publicada a nombre de "Athyx" ni de "Peter Tran"
  (perfil Athyx) en las búsquedas USPTO/Justia/Google Patents.** **[NO ENCONTRADAS]** — puede haber
  solicitudes no publicadas (<18 meses) o provisionales no visibles.
- El panorama de patentes de lactato continuo está dominado por otros: **Abbott Diabetes Care** (solicitud
  jul-2024, sensor de lactato con lactato oxidasa; inventor Lam Tran — persona **distinta**), y trabajo
  académico de biosensores de sudor. ([Justia – Lam N. Tran](https://patents.justia.com/inventor/lam-n-tran) · [Patsnap – continuous lactate patent landscape 2026](https://www.patsnap.com/resources/blog/articles/continuous-lactate-monitor-patent-landscape-2026/))

**Implicación para TID:** Athyx **no aparenta un foso de IP defendible propio**; su ventaja es marca +
software + narrativa. Bueno para TID: no hay barrera de patente evidente que nos bloquee si algún día
tocáramos sudor. (Confírmelo un **abogado de IP** antes de cualquier movimiento — yo solo preparo el
brief.)

---

## 8. Proveedores/OEM que TID podría integrar (en vez de inventar)

**Sudor (electroquímico):**
- **Epicore Biosystems** (spin-off Rogers Lab, Gx Sweat Patch de Gatorade): microfluídica de sudor
  battery-free NFC — el arquetipo detrás del estilo FLUX.
- Casas académicas/licenciables: plataformas LOx + Azul de Prusia serigrafiadas (ACS Sensors, ABC
  Springer). MOQ y madurez variables. ([ACS Sensors](https://pubs.acs.org/doi/10.1021/acssensors.3c00708) · [Springer ABC](https://link.springer.com/article/10.1007/s00216-025-05905-0))

**QCL / mid-IR (para la vía óptica):**
- **Boston Electronics / Block Engineering – MiniQCL / LaserTune**: módulo QCL OEM sintonizable. Tamaño
  **~1 pulgada cúbica**, **precio ~US$99,999**. Pensado para análisis de gases/lab, **no** para muñeca.
  ([Boston Electronics – MiniQCL](https://shop.boselec.com/products/miniqcl%E2%84%A2-quantum-cascade-laser-modules-for-oem-customers))
- **DiaMonTech** (Berlín): mid-IR fototérmico para glucosa no invasiva; venden módulo D-Base/D-Pocket y
  licencian IP. Referencia de que "óptica mid-IR en dedo/muñeca" existe pero **aún es voluminosa y
  cara**. ([Ophir/DiaMonTech](https://www.ophiropt.com/en/a/blood-glucose-monitor))

**Lectura NORTE:** para TID hay ruta de **integrar sudor vía OEM** si algún día lo quisiéramos; la ruta
**QCL es prohibitiva** en costo/tamaño/energía para una banda de rendimiento hoy.

---

## 9. Precio y modelo de venta

- **Modelo:** venta por **"batches"/preventa** (ej. "Batch 3 en venta, envía **septiembre 2026**";
  OBLA I lanzamiento **julio 2026**). Esto = **producto muy nuevo, sin stock maduro**, financiando
  producción con preórdenes. Envío citado 3–5 días hábiles / "free shipping" / "low on stock".
- **Precio exacto USD:** **[NO VERIFICADO]** — la tienda de Athyx bloqueó el scraping (HTTP 403) y los
  snippets no exponen la cifra. **No pongo un número inventado.** Referencia de mercado
  **[ESTIMACIÓN]**: consumibles de sudor tipo parche suelen ir US$50–200; un wearable óptico "premium"
  de nicho, US$300–600+. **Verificar directo en** [athyx.com/product](https://www.athyx.com/product)
  antes de citar cifra a dirección.

---

## 10. Costo aproximado de fabricar algo similar — **[ESTIMACIÓN, orden de magnitud]**

**Vía sudor tipo FLUX (viable):**
- BOM: parche electroquímico (LOx + microfluídica + antena NFC + IC NFC) **≈ US$8–25/unidad** a volumen;
  es en parte **consumible** (SKU aparte).
- NRE: diseño de sensor + app + algoritmo + validación ≈ **US$150k–500k** si se licencia base OEM;
  más si se desarrolla química propia.
- Orden de magnitud: **alcanzable para una startup**; el reto no es fabricar, es **validar el dato**.

**Vía láser tipo OBLA (no viable como banda hoy):**
- Solo el módulo QCL OEM **~US$100k/unidad** y **~1 in³** ([MiniQCL](https://shop.boselec.com/products/miniqcl%E2%84%A2-quantum-cascade-laser-modules-for-oem-customers)). Miniaturizar a
  muñeca con presupuesto energético de días es **I+D de años + decenas de millones**, no un BOM.
- Conclusión: si OBLA existe físicamente en 2026, o usa un QCL de laboratorio empaquetado (grande/caro/
  demo), o **el "quantum laser" es marketing** sobre óptica LED/NIR convencional. **[NO VERIFICADO —
  bandera de hype.]**

---

## 11. Dificultad de integrarlo a TID-MAX

TID-MAX ya es **PPG/HR/HRV/IBI/RR crudo ≥100 Hz + BLE + 5 ATM/IP68, pod polímero con bisel de aluminio**.
Meter "lactato" encima:

**Técnico:**
- **Sudor:** incompatible con nuestra arquitectura sellada y con natación (§12). Requiere consumible en
  contacto húmedo, se contamina, se lava. Rompe el "superficie limpia, sin puertos".
- **Óptico/QCL:** tamaño, energía (mata la meta de 7–14 días) y costo prohibitivos para v1/beta. **No.**
- Nuestra jugada de umbral **no necesita** un sensor de lactato nuevo: **DFA-α1 desde IBI/RR** (que ya
  capturamos) da LT1/VT1 no invasivo, **gratis en hardware** (§12).

**Regulatorio (analizando la jugada de Athyx):**
- Athyx se blinda con "**estimate for training, not a medical device**" (su propio disclaimer: "no
  intended to diagnose/treat"). Es **la misma jugada que ya adoptó TID-MAX**: claims de rendimiento,
  **nunca diagnóstico** → esquiva clasificación FDA/COFEPRIS. **Correcto y replicable.** El riesgo
  aparece si prometes un **número clínico** (mmol/L de lactato "real"): ahí te acercas a dispositivo
  médico. Mantener lenguaje de **zonas/umbral/estimación**.
- Para México sigue aplicando lo nuestro: **IFT/NOM-208** (BLE), **NOM-024/050** (etiquetado español),
  **COFEPRIS** (sin claim médico). Un sensor de lactato no cambia esa base si no se hace claim clínico.

**Validación:**
- El talón de Aquiles del género: correlación con lactato sanguíneo es **modesta y dependiente del
  atleta** (§6). Integrar lactato-estimado a TID **importaría el problema de credibilidad de Athyx**
  sin resolverlo. Nuestro diferencial es **IA predictiva sobre dato crudo confiable**, no un número de
  lactato dudoso.

**Veredicto de integración:** **alto costo, bajo retorno, riesgo de credibilidad.** No integrar sensor
de lactato en v1.

---

## 12. Qué cambiar para que sirva en NATACIÓN — y la alternativa DFA-α1

**El problema físico duro:** un **sensor de sudor es inservible bajo el agua** — el agua **lava el
sudor**, diluye electrolitos y arruina la microfluídica. FLUX I, por diseño (sudor + cámara del
teléfono + caminadora), **no existe para el nadador**. Punto.

**¿La vía láser/óptica transdérmica podría funcionar sumergida?**
- En teoría el mid-IR mide intersticial, no sudor, así que "no se lava". **Pero**: (a) el mid-IR se
  absorbe fuertísimo en **agua** — un contacto piel-agua arruina la ventana espectral; necesitas
  acoplamiento óptico sellado y presión constante contra piel, difícil con brazada; (b) tamaño/energía/
  costo (§10) lo descartan para una banda. **Conclusión: no es camino viable para natación en el
  horizonte de TID.**

**La alternativa correcta y barata — DFA-α1 (ya alineada con nuestra estrategia):**
- **DFA-α1** es un índice de HRV (correlación fractal de los intervalos R-R). **DFA-α1 ≈ 0.75 marca
  HRVT1 ≈ LT1/VT1** (umbral aeróbico) y **≈ 0.5 marca HRVT2 ≈ LT2/VT2**. Se calcula **solo con
  intervalos R-R** — exactamente el **dato crudo IBI/RR que TID ya exige capturar**. Cero sensor nuevo,
  cero consumible, cero contacto húmedo.
  ([the5krunner – DFA-α1](https://the5krunner.com/2021/02/25/important-training-news-dfa-alpha-1-new-threshold-discovery-method-with-hrv/) · [PMC – reliability/validity DFA-α1 thresholds](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10875128/))
- **Límites honestos:** DFA-α1 valida **mejor el umbral bajo (LT1/VT1)**; en alta intensidad el índice
  tiene **sesgo y límites de acuerdo amplios**, y depende de **calidad de R-R** (movimiento, artefacto).
  El Polar H10 correlaciona con ECG r>0.93 en reposo/ejercicio incremental, pero DFA-α1 en esfuerzo
  intenso muestra sesgo grande → **hay que limpiar R-R agresivamente.**
  ([PMC – Polar H10 HRV validity](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9459793/) · [PMC – agreement HRV vs lactate/ventilatory thresholds](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12910119/))
- **En natación** el reto no es el método, es la **calidad de señal PPG/IBI con brazada + agua fría +
  vasoconstricción**. Por eso TID ya apuesta a **PPG de bíceps** (más limpio en esfuerzo) + store-and-
  forward. **Ese** es el trabajo de ingeniería que da un diferencial real, no un sensor de sudor.

**Recomendación §12:** para "umbral en el nadador", TID va por **DFA-α1 sobre IBI/RR de bíceps**, no por
sudor ni láser. Es más barato, ya está en nuestra arquitectura, y no rompe el sellado.

---

## Veredicto para TID-MAX

**VIGILAR — no integrar, no aliar (por ahora).**

- **Ignorar, no:** Athyx valida que existe **apetito de mercado por "lactato/umbral para endurance"** y
  ocupa un espacio de marca ("real-time lactate", coach IA "Grete"). Es señal de demanda que nuestro
  agente de Rendimiento/Coach puede capturar mejor.
- **Integrar-vía-OEM, no:** el sensor de sudor rompe nuestro sellado y no sirve para natación; el láser
  es humo/prohibitivo. Importaríamos su problema de credibilidad.
- **Aliar, no (todavía):** Athyx es **inmaduro** (venta por batches, sin validación publicada, IP no
  visible, láser no demostrado). Una alianza hoy nos ataría a su riesgo científico.
- **Sí hacer:** **apropiarnos del "umbral no invasivo" por la vía sólida (DFA-α1 sobre nuestro R-R
  crudo)** y comunicarlo mejor que Athyx, con honestidad sobre límites. Ese es nuestro terreno:
  **IA predictiva sobre dato crudo confiable**, no un número de lactato dudoso.

**Porqué en una línea:** Athyx nos enseña el *mensaje* (umbral/lactato vende) pero no el *método* (su
dato es débil); TID gana comunicando umbral con DFA-α1, que ya tenemos, sin sensor nuevo.

---

## Riesgos y banderas

1. **Validación científica ausente:** cero estudios peer-reviewed del dispositivo Athyx; el paper de
   Nature que se les asocia **no es suyo** y mide **Na+/K+**, no lactato.
2. **Hype "quantum laser":** OBLA I no tiene hardware demostrado; física y costo (QCL ~US$100k, ~1 in³)
   hacen implausible una banda láser 24/7 hoy. Tratar como **marketing hasta ver datos**.
3. **Producto inmaduro:** venta por batches/preventa = financiando producción con preórdenes; riesgo de
   entrega/soporte.
4. **Credenciales del fundador sin verificar:** "BSc Nano + MD + PhD Sports Medicine" de Peter Tran
   **[NO VERIFICADO]** en fuentes independientes.
5. **Latencia y no-1:1 sudor↔sangre:** límite físico del método de sudor, no resoluble por software.
6. **Precio exacto no confirmado** (sitio bloqueó scraping): no citar cifra a dirección sin verla en vivo.
7. **Lección regulatoria útil (no riesgo):** su encuadre "estimate for training, not medical" es la
   jugada correcta y ya es la nuestra — mantenerla.

---

## Tabla resumen

| Producto | Tecnología (real vs claim) | Madurez | Precio (USD) | Aplicable a natación | Oportunidad para TID |
|---|---|---|---|---|---|
| **FLUX I** | Sudor electroquímico NFC battery-free + FC de cámara → **estimación** de lactato (real, a la venta) | Baja-media (venta por batches, sin peer-review) | **[NO VERIFICADO]**; est. ~US$50–200 | **No** (el agua lava el sudor) | Aprender el *mensaje* de umbral; **no** el sensor |
| **OBLA I** | **"Quantum laser"** mid-IR (claim) + LED PPG (aspiracional) | Muy baja (lanzamiento jul-2026, no demostrado) | **[NO VERIFICADO]** | Improbable (mid-IR se absorbe en agua; tamaño/energía) | Ninguna; vigilar por si demuestran algo |
| **DFA-α1 (nuestra vía)** | Umbral LT1/VT1 desde **IBI/RR crudo** (Polar H10-grade / PPG bíceps) | Alta (peer-reviewed, límites conocidos) | ~US$0 hardware extra (ya lo capturamos) | **Sí**, si se limpia bien el R-R subacuático | **Nuestro camino**: umbral no invasivo, barato, sellado |

---

### Fuentes principales
- [Athyx – FLUX I](https://www.athyx.com/product/flux) · [Athyx – OBLA I](https://www.athyx.com/product/obla) · [Athyx – home](https://www.athyx.com/)
- [Starleet × Athyx](https://www.starleet.com/) · [PitchBook – Starleet](https://pitchbook.com/profiles/company/756628-84)
- [Nature s41598-025-16559-4 (sudor Na+/K+, NO Athyx)](https://www.nature.com/articles/s41598-025-16559-4) · [AZoSensors](https://www.azosensors.com/news.aspx?newsID=16595)
- [Boston Electronics – MiniQCL (~US$100k, ~1 in³)](https://shop.boselec.com/products/miniqcl%E2%84%A2-quantum-cascade-laser-modules-for-oem-customers) · [Ophir/DiaMonTech mid-IR](https://www.ophiropt.com/en/a/blood-glucose-monitor) · [Sci Reports – dual QCL glucosa](https://www.nature.com/articles/s41598-023-34912-3)
- [ACS Sensors – sweat lactate](https://pubs.acs.org/doi/10.1021/acssensors.3c00708) · [Frontiers – narrative review](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2024.1376801/full) · [PMC – narrative review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11025537/)
- [Justia – patentes Lam N. Tran (Abbott, persona distinta)](https://patents.justia.com/inventor/lam-n-tran) · [Patsnap – panorama patentes lactato 2026](https://www.patsnap.com/resources/blog/articles/continuous-lactate-monitor-patent-landscape-2026/)
- DFA-α1: [the5krunner](https://the5krunner.com/2021/02/25/important-training-news-dfa-alpha-1-new-threshold-discovery-method-with-hrv/) · [PMC – reliability/validity](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10875128/) · [PMC – Polar H10 HRV](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9459793/) · [PMC – acuerdo HRV vs umbral](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12910119/)

_Marcados **[NO VERIFICADO]** / **[ESTIMACIÓN]** donde no hubo fuente primaria confiable. Precio exacto
de Athyx y credenciales del fundador pendientes de verificación directa._
