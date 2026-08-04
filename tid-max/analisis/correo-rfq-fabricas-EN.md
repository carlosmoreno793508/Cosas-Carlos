# Correos a fábricas (RFQ) — EN · secuencia de 2 pasos (NDA-first)

> Estrategia (decisión Carlos, 2026-08): el **primer correo NO adjunta la spec**. Manda un **scope breve**
> + propone **firmar un NDA mutuo ANTES** de compartir el RFQ técnico (protege la PI y filtra en serio).
> Solo tras el NDA se manda el `RFQ_TID-MAX_v2.3_EN.pdf`. Personaliza `[Contact]` / `[Manufacturer]`.
> Enviar desde carlos.moreno@tidmexico.com.mx.

---

## Correo 1 — Presentación + scope + NDA-first (SIN spec adjunta)

> Versión Rev. B (incorpora revisión externa): NO menciona aluminio (deja libre el material para no
> descartar plataformas existentes); encuadra como **"health & performance platform"** para ampliar el
> mercado percibido ante el ODM; pide la relación de largo plazo. *Nota: para usuario final / COFEPRIS
> mantener "rendimiento/bienestar, no médico" — esto es un correo B2B a fábrica.*

**Subject:** NDA Request & ODM Partnership Inquiry – TID-MAX Wearable Platform

Dear Sales & Engineering Team,

My name is Carlos Moreno, and I represent **TID**, a technology company based in Mexico.

We are currently developing **TID-MAX**, a next-generation wearable health and performance platform, and
we are looking for an experienced **ODM/EMS partner** to support our development from engineering
evaluation through pilot production and mass manufacturing.

**Project Overview**
TID-MAX is a screenless, waterproof wearable sensor platform designed for continuous physiological
monitoring across multiple sports and performance applications. Our current concept includes:
- Screenless wearable with an **interchangeable textile band** (wrist and upper-arm configurations)
- **Sealed engineering-polymer enclosure** with premium exterior finishes
- **5 ATM + IP68** water resistance
- **Sealed magnetic charging** (no exposed connectors)
- **BLE 5.x** with **OTA** firmware updates
- Target battery life of **7–14 days**
- Preference for leveraging an **existing hardware platform and tooling** to minimize NRE, development
  risk, and time-to-market

The core value of our product is **not the hardware itself, but the quality of the physiological data.**
A critical requirement for us is **access to raw biometric signals**, including:
- Raw PPG waveform (≥100 Hz)
- Beat-to-beat IBI/RR intervals
- IMU raw data
- Additional raw sensor data whenever available

**Access to raw sensor data through an SDK or documented API is mandatory.** We are not looking for a
platform that only provides processed fitness metrics. Our software, cloud platform, AI algorithms, and
mobile applications are being developed internally.

**Development Scope** — we are planning the project in the following phases:
- Engineering evaluation using development kits or existing platforms
- Prototype customization
- Beta pilot (approximately 20–50 units)
- Low-volume production
- Volume production (500 / 1,000 / 5,000+ units)

Before sharing our detailed RFQ and technical specifications, we would like to execute a **Mutual
Non-Disclosure Agreement**. We are happy to sign your standard NDA, or provide our own if that is more
convenient.

If the project appears to fit your capabilities, we would appreciate your feedback on the following:
1. Does your current platform support access to **raw PPG waveform, IBI/RR intervals, and other raw sensor
   streams**?
2. Are you willing to enter into a **Mutual NDA**?
3. Which member of your engineering or business-development team should we coordinate with?

If there is a good technical fit, I would be pleased to arrange a brief introductory meeting to discuss the
project in greater detail. We look forward to exploring the possibility of building a **long-term
partnership**.

Kind regards,

**Carlos Moreno**
Founder | TID · Mexico
carlos.moreno@tidmexico.com.mx

---

## Correo 2 — Tras firmar el NDA (adjunta la spec)

**Subject:** TID-MAX technical RFQ (under NDA) — quotation request

Dear [Contact],

Thank you for signing the NDA. Attached is our **technical RFQ (v2.3, `RFQ_TID-MAX_v2.3_EN.pdf`)**.

We'd appreciate a **tiered quotation** and your **DFM feedback**. The specific questions are consolidated
in **§13 and §15** (unit cost FOB, NRE existing vs. custom, lead times, samples, IP/SDK position, and the
optional add-ons). Two-stage quotation requested: **(a)** 3–5 EVK/dev boards now for data validation, and
**(b)** a ~20–50 unit pilot on an existing platform.

Happy to jump on a call to walk through it. Looking forward to your feedback.

**Carlos Moreno** · TID México · carlos.moreno@tidmexico.com.mx

---

## Flujo recomendado (5 pasos)
1. **Correo 1** (presentación + scope + NDA — sin adjunto).
2. **Firma del NDA mutuo.**
3. **Envío del RFQ** (Correo 2, adjunta `RFQ_TID-MAX_v2.3_EN.pdf`).
4. **Reunión técnica** con su ingeniería.
5. **Compliance Matrix:** pedir que respondan **requisito por requisito** — *Compliant / Partially
   compliant / Not compliant / Alternative proposal*. Proyecta empresa organizada y permite comparar ODMs
   objetivamente. (Ya está pedida en el RFQ §13.)

## Notas de uso (no enviar)
- **Correo 1 NO lleva adjunto** — es el gancho + NDA. Adjunta la spec **solo** en el Correo 2 (post-NDA).
- El **descalificador (raw PPG + SDK)** va desde el Correo 1 para que se autoseleccionen.
- **NO** menciones a Gael, WHOOP, ni el detalle de la IA/algoritmos — vendes "captura de dato crudo +
  manufactura". El moat vive en la nube, no en la cotización.
- **De cara a fábrica** puedes usar "health & performance platform"; **de cara a usuario/COFEPRIS**
  mantén "rendimiento/bienestar, no médico".
- Confirmar el **título de la firma** ("Founder" u otro). Ten el **NDA** listo (PDF/Word) para mandarlo
  en cuanto acepten. Prioriza a quien confirme **raw data**.
- Registrar en el tracker (H0.2 → H0.4): enviado, ¿acepta NDA?, ¿cumple dato crudo?, costo EVK, NRE, lead.
