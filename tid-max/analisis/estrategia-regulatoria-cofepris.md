# Estrategia regulatoria — TID-MAX (dos carriles: deportivo ahora, médico después)

> Decisión de Carlos (2026-08-03): TID-MAX v1 se ofrece como **producto deportivo/bienestar**, NO como
> dispositivo médico → **no** requiere registro sanitario de dispositivo médico ante COFEPRIS. Lo médico
> se deja para una **etapa posterior**, PERO **la tecnología (hardware/sensores) ya se diseña integrada**
> para poder habilitarlo después sin rediseñar. Fecha: 2026-08. No es asesoría legal — confirmar con
> especialista regulatorio/sanitario en México antes de lanzar. Ver `plataforma-multideporte.md §2`,
> `agentes-ai.md` (guardrails 2.4), `especificacion-pulsera-rfq.md`.

## Principio central: lo que gatilla "dispositivo médico" es el CLAIM, no el sensor

En México (COFEPRIS) un producto entra al régimen de **dispositivo médico** por su **uso previsto** y sus
**claims** (diagnóstico, tratamiento, prevención o monitoreo de una enfermedad), **no** por qué sensores
trae. Tener un sensor capaz de una medición clínica **no** te vuelve médico; **decir** que diagnostica o
detecta una enfermedad **sí**. Por eso la estrategia es **"hardware-ready, claim-gated"**: el hardware se
construye capaz; las funciones y afirmaciones médicas se mantienen **apagadas** en v1 y se **habilitan
después** con el registro correspondiente (precedente: Apple Watch embarcó el ECG y lo activó tras la
autorización regulatoria).

## Los dos carriles

| | **Carril 1 — AHORA (deportivo/bienestar)** | **Carril 2 — DESPUÉS (médico)** |
|---|---|---|
| Propuesta | Rendimiento, carga (ACWR), recuperación, sueño, bienestar, tendencias | Diagnóstico/alerta clínica (p. ej. arritmia, SpO₂ clínico, alerta de salud) |
| Registro médico COFEPRIS | **NO requerido** (sin claims médicos) | **Requerido**: registro sanitario de dispositivo médico |
| Otros requisitos | IFT/NOM-208-SCFI (radio), NOM-024/050-SCFI (etiquetado), IMPI (marca), **LFPDPPP** (datos personales de salud) | Todo lo anterior **+** probable **ISO 13485**, evidencia clínica, expediente técnico |
| En el tracker | **Fase R0 ya está en este carril** (IFT + etiqueta + marca; sin COFEPRIS médico) | Fase futura (no en el alcance del beta) |

> **Hallazgo a favor:** la Fase R0 del `PROJECT-TRACKER.md` **ya estaba construida para el Carril 1** — no
> contempla registro médico. Esta decisión solo lo hace explícito y consciente.

## Disciplina de claims (lo que NO se dice en v1)

Prohibido en marketing, app, firmware y tarjeta mientras estemos en Carril 1:
- "grado médico", "médico", "clínico" como calificativo del producto.
- "diagnostica", "detecta [enfermedad]", "trata", "previene [enfermedad]".
- Nombrar enfermedades o dar interpretación clínica (ya está en los guardrails 2.4).

Permitido (lenguaje de rendimiento/bienestar): carga, recuperación, readiness, HRV como *tendencia*,
sueño, estrés, zonas de FC, eficiencia. Ante una señal de alarma real → *"consulta a un profesional"*,
nunca una interpretación clínica. Todo claim es **trazable** a una señal del motor.

## "Tecnología ya integrada" — qué prever en el hardware AHORA (sin activarlo)

Para que el salto al Carril 2 **no** obligue a rediseñar la banda:
1. **AFE óptico de calidad + dato crudo** (ya [DURO] en el RFQ: MAX86141, PPG ≥100 Hz + IBI/RR). Base de
   HRV/SpO₂ clínicos futuros. ✅ ya previsto.
2. **Store-and-forward del dato crudo** (ya [DURO]). Sin dato crudo guardado no hay **evidencia clínica**
   futura. ✅ ya previsto.
3. **SpO₂ y temperatura** como opcionales del AFE (§4.3). Capacidad presente, claim apagado.
4. **ECG (si se contempla a futuro):** ⚠️ el MAX86141 **no** hace ECG — requiere **AFE de ECG aparte +
   electrodos**. Decisión: o se **prevé el espacio/footprint en el layout ahora** (sin popular en v1), o
   se acepta un rediseño en el Carril 2. *Pregunta abierta para la fábrica en la fase de layout.*

## Datos personales (aplica desde v1, aunque no sea COFEPRIS)

Los datos de salud/fisiológicos están protegidos por la **LFPDPPP**: aviso de privacidad, consentimiento,
y minimización. Relevante además por el perfil de usuarios (incluye menores/atletas jóvenes). No es
COFEPRIS, pero es cumplimiento obligatorio del Carril 1.

## Recomendación

1. **Proceder en Carril 1** para el beta y el lanzamiento inicial (deportivo/bienestar). Es rápido, barato
   y no bloquea la venta con registro médico.
2. **Mantener la disciplina de claims** en todo el material (la parte más fácil de romper por accidente).
3. **Diseñar el hardware "listo para lo médico"** según la sección de arriba — decidir explícitamente si se
   prevé el footprint de ECG antes de congelar el layout.
4. **Confirmar con un especialista regulatorio/sanitario mexicano** antes de lanzar (igual que el NDA con
   abogado de PI). Esta nota es estrategia, no la firma.
