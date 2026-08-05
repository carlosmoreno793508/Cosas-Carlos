# TID-MAX — Technical Specification for Quotation (RFQ) · Performance Band

**Document:** RFQ v2.3 — Hardware specification for ODM/EMS
**Date:** 2026-08-04 · **Owner:** Carlos Moreno (TID México) · carlos.moreno@tidmexico.com.mx
**Target recipients:** JointCorp, Vositone, Bingo, Star King (China Tier-1) · India alternative: Dixon/Dixtel, Optiemus
**Project stage:** Phase H0 (Spec + RFQ). The EVK (Phase H1) precedes tooling; see §12.

> **How to read this document.** Each requirement is tagged **[HARD]** (frozen decision, non-negotiable
> unless evidence is provided) or **[EST]** (estimate / target, to be confirmed by the manufacturer's DFM).
> **Optional** items are quoted separately with a cost delta and must NOT block the beta. All **open
> questions for the manufacturer** are consolidated in §13 and §15.

---

## 1. Product summary

TID-MAX is a **high-performance sports band**, **screenless and buttonless**. An **aluminum pod** with an
optical sensor sits in an **interchangeable magnetic woven loop** (quick-swap) and is worn on the **wrist
or upper arm (biceps)**. All interaction is via **app + double-tap + haptic feedback**; a **hidden
"breathing" color light** is the only visual element. The product's value is the **quality of the raw
signal** (raw PPG waveform + IBI/RR) that feeds the predictive AI in the cloud — therefore the
non-negotiable requirement is **access to raw data, not cooked metrics**. **This is not a wellness band**:
it is a measurement instrument for athletes.

**What is being quoted is "dumb but precise" hardware:** it captures, stores and transmits high-fidelity
physiological signal. **All intelligence (HRV, DFA-α1, load, prediction) lives in the cloud/app, NOT in
the firmware.** The firmware only acquires, compresses, stores and forwards.

---

## 2. Wear modes · [HARD]

| Mode | Location | Primary use |
|---|---|---|
| Wrist | Ventral/dorsal wrist | 24/7 wear, sleep, resting HRV |
| Biceps (upper arm) | Over the biceps | Effort/training: cleaner PPG for HRV/DFA-α1 under motion |

The **same pod** must work in both positions by swapping only the loop. The optical design must
prioritize a clean signal on the **biceps under motion and sweat** (the training use case), not only at
rest.

---

## 3. Form factor, dimensions, materials and finish

| Item | Requirement | Tag |
|---|---|---|
| Concept | Sensor pod + interchangeable woven band | [HARD] |
| Target pod dimensions | ~**32 × 28 × 11 mm** (target envelope, to be optimized by DFM) | [EST] |
| **Pod housing material** | **High-strength engineering polymer** (PC, PC+ABS or equivalent) suitable for skin contact, sweat, chlorine, sunscreen and UV. Must maintain IP68 + 5 ATM while **minimizing RF (BLE) attenuation** and **not degrading the optical sensor**. **Anodized aluminum allowed only as a bezel/accent** (localized metal) as long as it does NOT degrade RF or optics. *(Specified by performance; exact material to be proposed by DFM.)* | [HARD by performance] |
| Surface | **Clean, no openings or buttons** (better sealing, fewer failure points) | [HARD] |
| Skin contact | Biocompatible material (ISO 10993 / hypoallergenic) | [HARD] |
| Loop / strap | **Woven, magnetic clasp, interchangeable.** Variants: **woven textile = sport band** (light, quick-dry, for swimming); **metal mesh (Milanese) = optional lifestyle band** | [HARD] |
| **Pod↔band attachment** | **NO spring bars / pins.** The pod seats into a **cradle** on the band with **mechanical retention** (tabs capturing the pod's shoulder); the **magnet only aligns and provides the "click"**. See §9.4 | [HARD] |
| Loop sizes | Wrist range + biceps range (at least 2 lengths) | [EST] |
| Target weight | As low as possible; pod target ≤ ~25 g without loop | [EST] |
| Color/finish | Neutral pod (TBD); "Living Monolith" aesthetic. **Pod face has NO center LED** (only light = the perimeter ring, see §9.3) | [EST] |

**Key question for the manufacturer:** do you have an **existing tooling/platform** close to this form
factor that we could use for the beta to minimize NRE? (see §11–12).

---

## 4. Required sensors

### 4.1 Optical PPG — **the heart of the product** · [HARD]
- **Access to the raw PPG waveform, sampling ≥ 100 Hz**, plus **beat-to-beat IBI/RR** intervals. HR or
  cooked metrics only are **NOT** accepted. Without raw data the AI (DFA-α1, HRV) does not work — **this
  is a supplier disqualification criterion.**
- Reference optical AFE: **Analog Devices MAX86141 or equivalent-or-better** (dual-channel AFE, 19-bit
  ADC, ambient-light cancellation). Part number is not locked: any AFE that delivers **raw waveform
  ≥100 Hz + IBI/RR** with programmable MCU access is acceptable.
- Optical configuration (green/red/IR LEDs and photodiodes) to be proposed by the manufacturer for a
  **clean signal on wrist and biceps under motion**.

### 4.2 IMU — motion · [HARD]
- **Accelerometer + gyroscope (6-axis)**; **9-axis** (with magnetometer) preferred if it does not
  penalize battery/cost. Used for effort detection, sport classification and **swim lap counting via IMU**
  (no GPS — a documented differentiator).

### 4.3 Optional sensors (quote separately, state cost delta)
- **SpO2** (pulse oximetry) — supported by the MAX86141; confirm feasibility. *[Optional]*
- **Skin temperature sensor.** *[Optional]*
- **Depth / pressure sensor** (e.g. TE **MS5837-30BA**, ~3.3×3.3×2.75 mm, I²C, ~2 mm water resolution —
  *or equivalent*). For **underwater swim analysis** (streamline/breakout depth and turn trajectory) — a
  documented differentiator. *[Optional]* with **TWO [HARD] conditions:**
  1. **NO change to pod dimensions:** it must fit **within the current envelope (~32×28×11 mm, §3)
     without increasing any dimension.** If the manufacturer's platform cannot do it without growing the
     case, **it is dropped for the beta.**
  2. **NO compromise to sealing:** the pressure port must maintain **5 ATM (ISO 22810) + IP68** (§9.1).
     If it compromises sealing, it is dropped.
- **Single-lead ECG — HARDWARE-READY capability (not activated/claimed in v1).** Requires a **dedicated
  ECG AFE** (the MAX86141 does **NOT** do ECG) + skin-contact **electrodes**. Reference AFE: Analog
  Devices/Maxim **MAX30001** (ECG + bioimpedance) *or equivalent-or-better*. Electrodes: e.g. a **rear
  housing electrode** (wrist/biceps contact) + accessible electrode(s) for a spot-check reading.
  **Purpose:** to leave the device **ready for a future medical track** without a later redesign — in v1
  the product is **sports/wellness** and ECG is **NOT** advertised or enabled. Same **[HARD]** conditions
  as the depth sensor: **do not grow the envelope** and **do not compromise 5 ATM + IP68**. Preference:
  **lay out the footprint and electrodes now**, populated or not in the first run. *[Optional ·
  hardware-ready]*
- Optional items **must NOT** block the beta or trigger NRE. Quote them as add-ons.

> **No GPS in the band** [HARD]: it kills battery, raises cost/size and adds regulatory weight. Swim
> distance is solved by IMU (lap counting), not GPS.

### 4.4 Live on-device feedback · [HARD]
The band gives **real-time HR-zone feedback** without a screen, using the actuators it already carries:
- **Light by zone:** the **RGB perimeter ring** changes color by HR zone (e.g. Z1 blue, Z2 green,
  Z3 amber, Z4 red). **The face has NO center LED** (only light = the ring, §9.3).
- **Vibration by zone (accessible):** the **haptic motor (LRA)** vibrates **N times by zone** (Z1=1 …
  Z4=4, or a long alert buzz) **on zone change**. Serves **visually impaired users, no-look use and
  underwater**.
- **Independent on/off:** the user enables/disables light and vibration separately (light only / vibration
  only / both / none) **via double-tap + app — NOT a physical button** (keeps the "no buttons" rule, §9.2).
- **HR broadcast:** expose HR over a **standard BLE HR profile (and/or ANT+)** for external displays
  (coach tablet, pool wall clock).
- **Firmware requirement:** compute a **basic live HR** on-device **only to drive this feedback**. It does
  NOT replace the cloud AI; the **raw data (§4.1) is still stored intact**.

---

## 5. SoC / MCU · [HARD by capability, not by part number]

Specify **by minimum capability ("equivalent-or-better"), do not lock a part number.**

| Requirement | Minimum | Reference |
|---|---|---|
| RAM | **≥ 256 KB** | — |
| Flash | **≥ 512 KB** | — |
| Radio | **Bluetooth LE 5.x** (BLE) | — |
| Update | **OTA (over-the-air firmware update)** | — |
| Security | **Secure boot + encrypted/signed firmware** | ARM TrustZone / CryptoCell or equiv. |
| Reference SoC | **Nordic nRF52840** (1 MB flash / 256 KB RAM) or **nRF5340** (1 MB flash / 512 KB RAM, dual Cortex-M33) — **or better** | Available in production 2026 |

**Ruled out:** nRF52832 (insufficient memory for raw-data buffering). Any BLE SoC that meets the
RAM/flash floor + OTA + secure boot is acceptable.

---

## 6. On-board storage and capture modes (store-and-forward) · [HARD]

- **On-board flash (NAND/NOR)** for **store-and-forward**: the band **records to memory and syncs over
  BLE later**. Essential because **2.4 GHz BLE does not travel through water** (swimming) and to avoid
  depending on a continuous connection.
- **Continuous 100 Hz streaming over BLE 24/7 is NOT requested** — it breaks the battery. Continuous
  streaming applies only to a training/validation mode on demand.
- **Two capture modes:**
  1. **24/7 burst (duty-cycled):** periodic raw-PPG windows across the day/sleep for resting HRV, at low
     power consumption.
  2. **Continuous workout:** raw PPG ≥100 Hz + IBI + IMU sustained during the session, stored to flash
     and synced when finished.
- **Flash capacity [EST]:** size for **≥ several hours of raw PPG ≥100 Hz + IBI + IMU** without syncing
  (use case: long swim session). *Question for the manufacturer: how much buffer does your platform
  support and with what compression scheme?*

---

## 7. Battery and autonomy · target by AUTONOMY, not mAh

- **Autonomy target: 7–14 days** in mixed use (24/7 burst + ~1 training session/day). **[HARD on the
  autonomy target; mAh is a consequence, not a requirement.]**
- **Estimated capacity [EST]:** ~**80–110 mAh** LiPo within the §3 envelope — to be confirmed by the
  manufacturer per its platform and real consumption.
- Chemistry: **rechargeable Li-Po / Li-ion**, must comply with **UN 38.3** (see §10).
- *Question for the manufacturer: what real autonomy do you project on your platform for our two capture
  modes, and what cell capacity do you recommend?*

---

## 8. Charging · [HARD]

- **Sealed magnetic charging.** **No open port** on the device — the clean surface is a sealing
  requirement.
- Two acceptable options:
  1. **Magnetic pogo pins** with **hard gold ≥ 20 µin (0.5 µm) over a Pd/Ni barrier** for corrosion/sweat
     resistance.
  2. **Sealed inductive charging** (Qi-like).
- **Included accessory:** only a **USB-C magnetic charging cable/dock**. **No wall adapter / no AC plug**
  — this avoids NOM-003-SCFI in Mexico.
- **The charger couples magnetically to the POD** (where the battery is), **without removing it from the
  band** — it can charge in place, even on the wrist (WHOOP pattern). The band carries no electronics or
  contacts.
- *Question for the manufacturer: pogo or inductive on your existing platform? Cost and reliability of
  each.*

---

## 9. Water, sealing, interaction and aesthetics

### 9.1 Sealing / water · [HARD]
- **5 ATM (50 m) per ISO 22810:2010** (current version) — resistance for swimming/surface use.
- **IP68 (IEC 60529)** — dust + immersion.
- No open port (see §8). The manufacturer must **validate and certify** the sealing (see §10, §12).

### 9.2 Interaction · [HARD]
- **App (BLE)** as the primary interface.
- **Double-tap** on the pod as physical input (via IMU/tap-detect). **It is the "button" with no hole:**
  double-tap **cycles the feedback modes** (light / vibration / both / none, §4.4).
- **Haptic feedback** — **LRA vibration motor** (per-zone pattern, §4.4).
- **No screen, no mechanical buttons.** (A physical push-button is ruled out: a hole = leak and failure point.)

### 9.3 "Living Monolith" aesthetic · [HARD as a hook, detail [EST]]
- **Hidden breathing light** — a **perimeter ring** of RGB LED(s) under the surface that light up in a
  pattern/color (HR zone, §4.4). Hidden when off (clean surface). **The pod face has NO center LED** — the
  only light is the perimeter ring. Diffuser/optics to be defined with the manufacturer.

### 9.4 Pod↔band retention and serviceability · [HARD]
- **No spring bars / pins.** The pod seats into a **cradle** on the band with **mechanical retention**:
  tabs (or a guide + latch) that **capture the pod's shoulder**. The **magnet only aligns and provides the
  "click"** — retention does NOT depend on the magnet.
- **The wear feature lives on the REPLACEABLE band** (the tabs/guide, in POM/nylon or a metal guide). The
  **pod** only presents a **passive aluminum shoulder** (does not flex, does not wear).
- **Band sold as a spare part** (separate SKU) — the user replaces a cheap band, never the pod.
- **Must withstand** the forces of **swimming (push-off), running and contact (team sports)** without
  detaching; removal requires a **deliberate action** (release tab / double-tap).
- *Questions for the manufacturer: (a) measurable **retention force** + test method; (b) **insertion cycle
  life** (target ≥ 5,000–10,000 cycles) validated by test; (c) **drop/impact** test; (d) your recommended
  mechanism (metal guide vs POM snap-fit) with cost delta.*

---

## 10. Certifications the manufacturer must deliver (compliance deliverables)

The manufacturer **delivers the reports/certificates; the Mexican homologation (IFT/NOM) is handled by
TID** (not the manufacturer's responsibility). We request from the manufacturer:

| Deliverable | Detail |
|---|---|
| **RF reports** | RF measurements of the module/BLE (to support **IFT / NOM-208-SCFI** homologation in Mexico) |
| **CE** (radio/EMC/health) | Applicable CE marking (RED) |
| **FCC** | FCC ID / BLE module report |
| **RoHS** | Substance compliance |
| **UN 38.3** | Li battery test summary (transport requirement, mandatory since 2020) |
| **Biocompatibility** | ISO 10993 for the skin-contact material |
| **Sealing report** | Evidence of 5 ATM (ISO 22810) + IP68 testing |
| Labeling support | Product data for the NOM label (see §14): brand/model, country of origin, specs |

---

## 11. Intellectual property (IP ownership) · [HARD — granular]

**Ownership of each element must be negotiated and put in writing separately.** The IP contract is
reviewed/signed by an IP attorney (TID prepares requirements). For the quotation, ask the manufacturer for
its **position on ownership and license** for:

| Element | Note |
|---|---|
| **PCB (schematic + layout)** | TID ownership or license? |
| **Gerbers** (PCB fabrication files) | |
| **Firmware** (acquisition/BLE/OTA code) | Critical: raw-data access depends on this |
| **Mold / tooling** (mechanical) | Distinguish existing (shared) mold vs. custom (owned by whom?) |
| **Mechanical CAD** (3D of pod/loop) | |
| **Bootloader** | Tied to secure boot / OTA |
| **SDK** (so the app can read the raw data) | Essential for TID |
| **Test & calibration software** | |
| **Production/test fixtures** | |

> **Risk if undefined:** these are white-label manufacturers; by default mechanical/firmware IP tends to
> stay with them. Without the SDK + firmware/raw-data access, TID becomes captive to a single supplier.
> **Negotiate before cutting any custom mold.**

---

## 12. EVK-first path (do not cut a mold blindly)

**Before** the mold and the pilot, TID validates raw-data quality with dev boards. This shapes the
quotation:

1. **EVK first (Phase H1):** **3–5 dev boards** (nRF52840/nRF5340 + MAX86141, e.g. MAXREFDES103 or
   equivalent) to validate **RR-interval + DFA-α1** capture against an ECG reference (Polar H10) **before**
   committing tooling.
2. **Mold go/no-go (H1.5):** no custom mold is cut until the EVK validates "better raw data".
3. **Beta on existing mold/platform:** for the pilot we use the ODM's **existing mold/platform** to
   minimize NRE. The beta's goal is to **validate function and data quality, not custom tooling.**

That is why this RFQ asks for a **two-stage** quotation: (a) EVK/dev boards now, and (b) pilot on an
existing platform.

---

## 13. Quantities to quote and price breaks

Please provide a tiered quotation:

| Item | Quantity | Purpose |
|---|---|---|
| **EVK / dev boards** | **3–5 units** (nRF + MAX86141) | Raw-data validation (Phase H1), before the mold |
| **Beta pilot (DVT)** | **~20–50 units** | Beta with real athletes (Phase H3) |
| **Production MOQ** | **~500 units** | Commercial start (Star King MOQ 500) |
| **Price breaks** | Quote **@500 / @1,000 / @5,000** | Cost curve by volume |

**Request for each tier:**
- **Unit cost (FOB)** by volume (500/1k/5k).
- **NRE / tooling**: break out **existing mold vs. custom**.
- **Lead time**: samples, tooling, production.
- **Samples**: cost and time for golden samples / pre-production.
- **DFM feedback**: design-for-manufacturing recommendations on this spec (form factor, battery,
  charging, sealing).
- **Explicit confirmation**: can you use an **existing mold/platform** for the beta to minimize NRE? Which
  platform, and how close is it to §3?
- **Compliance Matrix**: for each requirement in this spec, please respond **Compliant / Partially
  compliant / Not compliant / Alternative proposal** (with a note). This lets us compare multiple ODM
  proposals objectively.

---

## 14. Labeling and packaging — TID's responsibility, NOT blocking

*Informational for the manufacturer; TID provides artwork and text. It does not condition the technical
quotation.*

- Label in **Spanish** per **NOM-024-SCFI + NOM-050-SCFI**: denomination, brand/model, country of origin,
  **importer (Mexican tax domicile)**, instructions and **warranty policy**.
- Origin: label **"Assembled in Mexico with imported components"** if local assembly applies; **"Designed
  in Mexico"** as narrative. "Made in Mexico" is a separate process (not automatic).
- The manufacturer must **support** labeling with product data and leave space/area for the NOM label on
  the packaging.
- Packaging: TBD; no wall adapter included (see §8).

---

## 15. Summary: HARD vs ESTIMATE

**[HARD] (frozen; disqualification criterion if not met):**
- Access to **raw PPG ≥100 Hz + IBI/RR** (not cooked metrics only).
- **Store-and-forward** with on-board flash + 2 capture modes.
- SoC **≥256 KB RAM / ≥512 KB flash + BLE 5.x + OTA + secure boot**.
- **5 ATM (ISO 22810) + IP68**, **no open port**, **sealed magnetic charging** (to the pod, without
  removing it), **no wall adapter**.
- No screen / no buttons; **polymer housing + aluminum bezel** (§3); interchangeable magnetic woven loop;
  wrist and biceps.
- **Pod↔band attachment with no pins, mechanical retention**; wear feature on the **replaceable band**
  (separate SKU); resistance to swim/run/contact/drop + insertion cycle life (§9.4).
- **Live feedback (§4.4):** HR zone by **light color** (perimeter ring, no center LED) + **vibration
  N×zone** (accessible); on/off via **double-tap** (no button); BLE HR / ANT+ broadcast.
- **7–14 day autonomy** target.
- Granular IP negotiated (§11).

**[EST] (target / to be confirmed by DFM):**
- Dimensions ~32×28×11 mm and weight ≤~25 g.
- Battery capacity ~80–110 mAh.
- Flash capacity / hours of buffer.
- SpO2, skin temperature, **depth/pressure sensor** and **hardware-ready single-lead ECG** (optional,
  §4.3). The depth sensor and ECG only if they fit the current envelope **without growing the case** and
  **without compromising sealing**. ECG is a future capability (medical track); it is not enabled or
  advertised in v1.

**Open questions for the manufacturer (consolidated):**
1. Existing mold/platform close to the form factor? Which one, and how much NRE does it save in the beta?
2. Does your optical AFE deliver **raw waveform ≥100 Hz + IBI/RR** with SDK access? (disqualifying if not).
3. Projected real autonomy per capture mode and recommended cell capacity?
4. How much flash buffer and with what compression for raw PPG + IMU?
5. Charging: pogo (hard gold ≥20 µin / Pd-Ni) or inductive on your platform? Cost/reliability.
6. Position on **ownership and license** for each IP element (§11), especially **SDK + firmware**.
7. Price breaks @500/1k/5k, NRE (existing vs custom), lead times and sample cost/time.
8. **Optional depth sensor (§4.3):** can you integrate a **pressure/depth sensor** with a **sealed
   pressure port** while maintaining **5 ATM + IP68 AND the current envelope without growing any
   dimension**? Cost delta, NRE delta and range/resolution (we target ~0–10 m, cm resolution)?
9. **Hardware-ready ECG (§4.3):** can you integrate a **single-lead ECG AFE** (e.g. MAX30001) with
   **electrodes** (rear-housing electrode + accessible electrode) while maintaining **5 ATM + IP68 and the
   envelope without growing**? Cost/NRE delta with the AFE **populated** vs. only **laying out the
   footprint** (unpopulated)? Note: this is a future capability; it is not enabled in v1.
10. **Pod↔band attachment (§9.4):** recommended **pin-less** mechanism (metal guide vs POM snap-fit)?
    Measurable **retention force** + test method, **insertion cycle life** (≥5,000–10,000 cycles) and a
    **drop** test? Can the **band** be sold as a spare part (separate SKU)?
11. **Live feedback (§4.4):** does your platform support an **RGB perimeter ring** (no center LED), an
    **LRA haptic** with patterns, **double-tap** to cycle modes, and **BLE HR / ANT+ broadcast**? Cost
    delta if any?

---

## 16. Sources (technical data verified 2026-08-02)

- Nordic nRF52840 (1 MB flash / 256 KB RAM, CryptoCell/TrustZone, BLE 5.x) — nordicsemi.com/Products/nRF52840
- Nordic nRF5340 (1 MB flash / 512 KB RAM, dual Cortex-M33, CryptoCell-312) — nordicsemi.com/Products/nRF5340
- Analog Devices MAX86141 (dual-channel optical AFE, 19-bit ADC, WLP 20-pin) — analog.com/en/products/max86141.html
- TE MS5837-30BA (depth/pressure sensor, **3.3×3.3×2.75 mm** package, I²C, ~2 mm water res., 0–30 bar) —
  te.com / mouser.com/new/te-connectivity/te-ms5837-30ba
- Analog Devices/Maxim MAX30001 (**single-lead ECG + bioimpedance** AFE, ultra-low power; the ECG
  complement the MAX86141 does not cover) — analog.com/en/products/max30001.html
- ISO 22810:2010 (water resistance of watches, current version) — iso.org
- IP68 — IEC 60529
- UN 38.3 (UN Manual of Tests and Criteria, sec. 38.3; test summary mandatory since 2020) —
  intertek.com/batteries/un-38-3-testing
