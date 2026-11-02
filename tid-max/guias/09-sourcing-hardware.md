# Guía 09 — Sourcing de hardware (checklist para fábricas/OEM)

> **Para qué:** vetear a cada fábrica/proveedor de la banda TID-MAX con las mismas preguntas y
> comparar manzana con manzana. Nace del contacto con un proveedor del TK35Pro ("ECG + AI Medical
> Diagnosis / hospital-grade") que **esquivó** la pregunta de precisión y respondió solo con venta.
>
> **Regla de oro:** TID-MAX corre **nuestro motor sobre el dato CRUDO** (R-R latido a latido), no
> sobre los scores de caja negra del fabricante. Si un equipo no entrega el crudo, **no nos sirve**,
> por bonito que sea.

---

## Qué necesita cada versión (split v1 / v2)

| Capacidad | v1 (lanzamiento) | v2 (siguiente) |
|---|---|---|
| **Acceso a R-R / PPG crudo** (BLE/SDK) | ✅ **imprescindible** | — |
| PPG (FC/HVC/SpO₂), temp de piel, acelerómetro | ✅ | — |
| BLE + protocolo/SDK documentado | ✅ | — |
| Banda **sin pantalla** + buena batería | ✅ | — |
| Resistencia al agua (natación) | ✅ deseable | — |
| **Carga solar (2ª fuente, trickle)** | ❌ | ⚙️ **opcional** — *extiende* batería, no la reemplaza |
| ECG de 1 derivación | ❌ (claim médico) | ⚙️ opcional, solo con cert real |

> El solar y el ECG van a v2 porque **suben BOM/MOQ/NRE** y no deben arriesgar el lanzamiento.
> v1 se juega todo en **acceso al dato crudo** + calidad de señal.

---

## La pregunta que decide todo (crudo)

> Does the device expose **raw sensor data** — raw PPG waveform and **beat-to-beat RR / IBI intervals
> (ms)** — not just processed scores? How do we access it: a **BLE characteristic**, an **SDK**, or an
> API? Is there documentation? Can a third-party app read the raw stream on-device?

---

## Preguntas al proveedor (copiar/pegar, en inglés)

**1 · Sensores y muestreo**
> PPG **sampling rate (Hz)**? Which sensors: PPG, single-lead ECG, SpO₂, **skin temperature**,
> accel/gyro? Sensor/chipset brand (Maxim, Goodix, ADI…)?

**2 · Precisión real (apretar)**
> Share **validation data**: HR/HRV accuracy **vs a reference** (Polar H10 / medical ECG), mean
> error. Is the "AI medical diagnosis" a **certified medical function** or a wellness estimate?
> **Which regulator cleared it (FDA 510(k) / CE-MDR)? Certificate number?**

**3 · Certificaciones**
> Certificates: **FCC, CE, RoHS, Bluetooth SIG**, battery **UN38.3**, any medical clearance.

**4 · Hardware**
> **Form factor** (watch vs arm/wrist **band**), battery life (continuous HR + nightly), charging,
> **water resistance (ATM/IP)**, strap, weight.

**5 · OEM/ODM y comercial**
> **OEM/white-label** (our branding, custom housing)? Can we **customize firmware** or at least
> **unlock raw-data access**? **MOQ**, **unit price at 100 / 500 / 1,000**, NRE/tooling, lead time,
> warranty, after-sales.

**6 · Solar (solo para v2)**
> Can you integrate a **solar cell on the top face** with an **energy-harvesting PMIC (MPPT)** as a
> **secondary trickle** charger, OEM/ODM? Added BOM cost, MOQ, NRE? Any solar-assisted model already?

**7 · Muestra (el filtro definitivo)**
> Can you send **1–2 paid samples** for engineering evaluation before any order?

> **Validación de la muestra:** se graba en paralelo con un **Polar H10** y se compara el R-R con
> `software/valida_motor.py`. Si el R-R no cuadra, su "hospital-grade" es marketing — con números.

---

## Carga solar como 2ª fuente — presupuesto de energía (v2)

- **Consumo de la banda** (PPG continuo + HVC + accel + BLE), optimizado: ~**5–10 mW** promedio →
  ~**120–240 mWh/día**. Batería 80–120 mAh (~300–440 mWh) → ~2–4 días.
- **Cosecha solar en muñeca** (~4–6 cm² útiles): a pleno sol ~60–90 mW *teóricos*, pero tapada por
  la manga, en ángulos random y mayormente en interior (donde rinde casi nada) → **~20–60 mWh/día
  realistas** = **10–30 %** del consumo. Estira 2 días a ~2.5–3, o 7 a ~9–10.
- **Veredicto:** **extiende, no reemplaza.** Referencia: Garmin Solar (~10 cm², worn-exposed) también
  lo vende como extensión, nunca "nunca la cargues". Mejor encaje: banda **sin pantalla** (cara libre)
  + público **outdoor**. Requiere celda flexible + **PMIC con MPPT** (p. ej. TI BQ25570/BQ25505).
- **Antes de comprometer:** medir el consumo real del sensor elegido + **field test** de cosecha en
  el uso objetivo (no el número de folleto).

---

## Banderas rojas

- **"Medical diagnosis / hospital-grade"** = **claims médicos** con responsabilidad legal (COFEPRIS en
  México). TID-MAX se posiciona **APROXIMADO, no diagnóstico** — no heredar esa promesa. Pedir cert,
  no usarla en marketing.
- **Esquivar la precisión** + respuesta 100 % de ventas = típico revendedor sin datos de validación.
  La **muestra** + el **acceso al crudo** separan al fabricante serio del intermediario.

---

## Tabla comparativa de proveedores (llenar por fábrica)

| Proveedor | Modelo | ¿R-R crudo? (BLE/SDK) | PPG Hz | Sensores | Certs | Form factor | Batería | OEM? | MOQ | Precio @500 | NRE | Muestra | R-R vs H10 | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| linshen (TK35Pro) | TK35Pro | ? (preguntar) | ? | PPG+ECG+? | ? | reloj | ? | ? | ? | ? | ? | pedir | — | esquivó precisión |
| … | | | | | | | | | | | | | | |
