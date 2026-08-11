# Agregadores de datos wearable — Terra vs Vital (Junction)

> Decisión del ítem **0.1** del tracker: elegir el agregador que nos da, con **una sola integración**, el botón
> "Conéctate con…" de decenas de apps (Strava, Garmin, Polar, Oura, Fitbit, Withings, WHOOP…). Alternativa a
> construir el OAuth de cada plataforma por separado. Precios y coberturas **a confirmar en vivo** (los sitios
> cambian seguido; este doc se hizo con búsqueda web en ago-2026, sin poder abrir los portales por egress).

## Qué es un agregador (y por qué nos sirve)

En vez de programar y mantener el "Conéctate con Strava", "…con Garmin", "…con Polar" uno por uno —cada uno con
su registro de desarrollador, sus términos y su mantenimiento— el agregador ya tiene **todos** esos OAuth hechos.
Nosotros integramos **una API** y el usuario ve un menú con los logos; al conectar, sus entrenamientos llegan
**normalizados** a un webhook nuestro. Es exactamente el modelo "clic en su logo → su página → login allá → token".

- **Ventaja:** velocidad brutal (semanas, no meses) y cobertura enorme sin mantener N integraciones.
- **Costo:** se paga **por usuario activo/mes** (no es gratis a escala).
- **Límite:** siguen entregando dato **"cocinado"** (FC, HRV, sueño, ritmo). El **PPG/IBI crudo** para DFA-α1
  **no** viene de aquí → ese es el hardware propio / Polar H10 (moat intacto).

---

## Terra  ·  tryterra.co

| | |
|---|---|
| **Qué es** | API de datos de salud/fitness; **500+** integraciones (wearables, apps, labs de sangre) |
| **Cobertura** | Garmin, Oura, Apple, WHOOP, Polar, Fitbit, Withings, Peloton, Eight Sleep, Freestyle Libre, Suunto, COROS… |
| **Extras** | Health scores (recovery, strain, stress, immunity), integraciones de laboratorio, gamificación (rewards/streaks) |
| **Precio** | **Por usuario activo**, escala on-demand. Cifra pública no detallada → **cotizar con ventas**. Hay **30 días money-back** y se puede **pausar la suscripción durante desarrollo**. |
| **Cumplimiento** | HIPAA, GDPR, CCPA, **SOC 2 Type II** |
| **Entrar / registrarse** | Dashboard dev: **https://dashboard.tryterra.co** · Docs: **https://docs.tryterra.co** · Precios: **https://tryterra.co/pricing** |

**Pro:** cobertura y features (scores, labs) más amplias; bueno si algún día quieres el lado de laboratorio.
**Contra:** precio no transparente (hay que hablar con ventas para saber el número real).

---

## Vital — ahora "Junction"  ·  tryvital.com

> ⚠️ **Vital se renombró a "Junction".** El producto y los docs siguen bajo `tryvital`, pero la marca comercial
> es Junction. Es la misma empresa (YC W20).

| | |
|---|---|
| **Qué es** | API única para **500+** dispositivos wearable + laboratorios (EE.UU.). YC W20. |
| **Cobertura** | Garmin, Oura, Apple, WHOOP, Polar, Fitbit, Withings… (similar a Terra en wearables) |
| **Precio** | **Publicado:** de 0–1,000 usuarios = **$0.50 USD/usuario/mes**, con **mínimo $300/mes**. Incluye el **Vital Link Widget** (el menú de logos listo), integraciones básicas, Slack de comunidad y analytics. **Se empieza gratis, sin tarjeta.** |
| **Onboarding** | Llamada inicial; para el lado de labs/pacientes citan 3–6 semanas a producción (wearables suele ser más rápido). |
| **Entrar / registrarse** | Dashboard dev: **https://app.tryvital.io** · Docs: **https://docs.tryvital.io** · Precios: **https://www.tryvital.com/pricing** |

**Pro:** **precio transparente** ($0.50/usuario) y **widget listo** para poner los logos sin diseñar la UI.
**Contra:** mínimo $300/mes desde temprano; marca en transición (Vital→Junction) puede confundir en la doc.

---

## Comparativa rápida

| Criterio | Terra | Vital / Junction |
|---|---|---|
| Integraciones | 500+ | 500+ |
| Precio transparente | ❌ (cotizar) | ✅ $0.50/usuario/mes ($300 mín) |
| Empezar gratis | ✅ (30d money-back, pausar en dev) | ✅ (sin tarjeta) |
| Widget de conexión listo | Sí | ✅ **Vital Link Widget** |
| Labs de sangre | ✅ fuerte | ✅ (EE.UU.) |
| Cumplimiento | HIPAA/GDPR/CCPA/SOC2 | HIPAA/GDPR (health-grade) |

---

## ⚠️ Consideración de términos (Strava / Garmin)

Ojo con la capa legal **debajo** del agregador: aunque conectes por Terra/Vital, los datos siguen sujetos a los
términos de **cada fuente**. Relevante para TID-MAX porque somos muy de IA:
- **Strava** endureció términos a fines de 2024: restringe **entrenar modelos de IA/ML** con sus datos y mostrar
  datos de un atleta a terceros. Mostrar al usuario **su propio** dato/coaching suele estar bien; entrenar
  modelos, no. **Confirmar con el agregador** cómo pasan esos términos.
- **Garmin** requiere aprobación de su programa; el agregador ya suele tenerla, pero valida el alcance.

---

## Recomendación para arrancar

1. **Empezar con Vital/Junction** para el PoC: precio claro ($0.50/usuario), widget listo y arranque gratis →
   conectamos Strava + Polar + Garmin + Oura en días, sin programar cada OAuth.
2. **Tener Terra como plan B / comparación**: si necesitamos su cobertura extra de scores o el lado de labs,
   o si su cotización por volumen sale mejor a escala.
3. **En paralelo**, para las fuentes clave y sin costo por usuario, evaluar **Strava API** y **Polar AccessLink
   directos** (gratis) si solo necesitamos 2-3 fuentes y queremos evitar el $/usuario.
4. **El dato crudo (DFA-α1)** NO depende de esto → sigue siendo hardware propio / Polar H10.

---

## Apéndice — portales de desarrollador directos (sin agregador)

Por si construimos alguna integración nosotros mismos (Opción A):

| Plataforma | Portal dev |
|---|---|
| **Strava** | https://www.strava.com/settings/api · docs: https://developers.strava.com |
| **Polar** (AccessLink) | https://www.polar.com/accesslink-api/ · admin: https://admin.polaraccesslink.com |
| **Garmin** | https://developer.garmin.com/gc-developer-program/ |
| **Oura** | https://cloud.ouraring.com (developer) · docs: https://cloud.ouraring.com/docs |
| **Fitbit** | https://dev.fitbit.com |
| **Withings** | https://developer.withings.com |
| **WHOOP** | https://developer.whoop.com *(ya integrado)* |

> Nota: no pude abrir estos sitios desde el entorno (egress bloqueado); las URLs vienen de conocimiento + búsqueda.
> Verifícalas al entrar. Nike Run Club y Peloton **no** tienen API pública → solo vía sincronización a Strava.
