# Correos a fábricas (RFQ) — EN · secuencia de 2 pasos (NDA-first)

> Estrategia (decisión Carlos, 2026-08): el **primer correo NO adjunta la spec**. Manda un **scope breve**
> + propone **firmar un NDA mutuo ANTES** de compartir el RFQ técnico (protege la PI y filtra en serio).
> Solo tras el NDA se manda el `RFQ_TID-MAX_v2.3_EN.pdf`. Personaliza `[Contact]` / `[Manufacturer]`.
> Enviar desde carlos.moreno@tidmexico.com.mx.

---

## Correo 1 — Presentación + scope + NDA-first (SIN spec adjunta)

**Subject:** Wearable ODM/EMS partner — raw-PPG performance band (NDA before RFQ)

Dear [Contact / Sales team],

My name is Carlos Moreno, from **TID (Mexico)**. We are developing **TID-MAX**, a **high-performance
sports wearable**, and we are looking for an **ODM/EMS partner** for an evaluation build, a beta pilot and
a path to production.

**Brief scope:**
- A **screenless, sealed aluminum-and-polymer sensor pod** worn on the wrist or biceps, on an
  interchangeable woven band.
- Its value is the **quality of the raw signal** — **raw PPG waveform (≥100 Hz) + beat-to-beat IBI/RR** —
  which feeds our cloud AI. **Access to raw data (not cooked metrics only) is a hard requirement.**
- Sealed to **5 ATM + IP68**, **sealed magnetic charging** (no open port), **BLE 5.x + OTA**, target
  **7–14 day** autonomy. We prefer to start on an **existing platform/mold** to minimize NRE.
- Scope covers **EVK/dev boards → a ~20–50 unit beta → production** (price breaks @500/1k/5k).

Before sharing our **detailed technical RFQ**, we'd like to put a **mutual NDA** in place. We're happy to
**sign yours, or provide ours** — whichever is faster.

Could you let us know: **(1)** is this a fit for your capabilities (in particular, can your optical AFE
expose **raw waveform + IBI/RR** via SDK)? **(2)** are you willing to sign a mutual NDA? and **(3)** who
should we coordinate with? I'd be glad to set up a short call.

Thank you for your time,

**Carlos Moreno** · TID México · carlos.moreno@tidmexico.com.mx

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

## Notas de uso (no enviar)
- **Correo 1 NO lleva adjunto** — es el gancho + NDA. Adjunta la spec **solo** en el Correo 2 (post-NDA).
- El **descalificador (raw PPG + SDK)** va desde el Correo 1 para que se autoseleccionen.
- **NO** menciones a Gael, WHOOP, ni el detalle de la IA/algoritmos — vendes "captura de dato crudo +
  manufactura". El moat vive en la nube, no en la cotización.
- Ten el **NDA** listo (PDF/Word) para mandarlo en cuanto acepten. Prioriza a quien confirme **raw data**.
- Registrar en el tracker (H0.2 → H0.4): enviado, ¿acepta NDA?, ¿cumple dato crudo?, costo EVK, NRE, lead.
