# Mapa de conectividad — de qué apps podemos bajar datos (y cómo)

> Mapa maestro para la ingesta de TID-MAX: qué plataformas tienen **API directa** (botón "Conéctate con…"),
> cuáles solo se pescan **indirectamente** (vía Strava o vía Apple Health / Health Connect), y cuáles son
> **imposibles** hoy. Complementa `agregadores-terra-vital.md` (ítem 0.1 del tracker).
> URLs verificar al entrar (el entorno bloquea egress a varios de estos dominios).

## Regla base (OAuth, no contraseñas)
El usuario da clic en el logo → va **a la página de la plataforma** → mete su usuario/contraseña **allá** →
nos devuelve un **token**. **Nunca** tecleamos ni guardamos su contraseña. Válido para todas las de "API directa".

---

## Tabla maestra

| App | Tipo | API directa (OAuth) | Vía Strava | Vía Apple Health / Health Connect | Veredicto |
|---|---|:---:|:---:|:---:|---|
| **WHOOP** | Wearable | 🟢 Sí *(ya integrado)* | — | — | ✅ Listo |
| **Strava** | Plataforma/hub | 🟢 Sí | — | — | ✅ Hub de actividades |
| **Polar** (Flow) | Wearable | 🟢 Sí (AccessLink) | ✔️ (si el user sincroniza) | ✔️ | ✅ Directo |
| **Garmin** | Wearable | 🟡 Sí (con aprobación) | ✔️ | ✔️ | ⭐ Prioridad — running/tri/ciclismo/**natación** |
| **Oura** | Anillo | 🟢 Sí (self-serve) | parcial | ✔️ | ⭐ Sueño/HRV top |
| **Fitbit** | Wearable | 🟢 Sí (OAuth2) | parcial | ✔️ | ✅ Base enorme |
| **Withings** | Salud | 🟢 Sí (OAuth2) | parcial | ✔️ | ✅ Peso/FC/sueño |
| **Ultrahuman** | Anillo | 🟢 Sí (partner) | — | ✔️ | ✅ Recovery/glucosa |
| **COROS** | Wearable | 🟡 Sí (partner) | ✔️ | ✔️ | ✅ Running/trail élite |
| **Suunto** | Wearable | 🟡 Sí (partner) | ✔️ | ✔️ | ✅ Outdoor |
| **Wahoo** | Ciclismo | 🟡 Sí (partner) | ✔️ | ✔️ | ✅ Potencia bici |
| **TrainingPeaks** | Plataforma coach | 🟡 Sí (partner) | ✔️ | — | ✅ Triatlón/resistencia |
| **Zwift** | Indoor bici/run | 🔴 API limitada | ✔️ (Zwift→Strava) | ✔️ | 🟠 Solo vía Strava/Health |
| **Apple Health** | Colector (iOS) | 🟠 Solo con app iOS | — | (es la fuente) | 🟠 Requiere app propia |
| **Samsung Health** | Colector (Android) | 🟠 Solo con app (Health Connect) | — | (es la fuente) | 🟠 Requiere app propia |
| **Google Fit** | Colector (Android) | 🟠 En retiro → Health Connect | — | ✔️ | 🟠 Migrar a Health Connect |
| **Nike Run Club** | Marca/app | 🔴 No | 🔁 Nike→Strava | ✔️ | 🔴 Solo indirecto |
| **Adidas Running** (Runtastic) | Marca/app | 🔴 No | ❌ (no sync nativo) | ✔️ | 🔴 Solo vía Apple Health/HC o puente |
| **Peloton** | Fitness | 🔴 No oficial | 🔁 (sync) | ✔️ | 🔴 Solo indirecto |
| **MyFitnessPal** | Nutrición | 🔴 Cerrada a nuevos | — | — | 🔴 No |

Leyenda: 🟢 self-serve · 🟡 requiere aprobación/partner · 🟠 necesita app en el teléfono · 🔴 sin API · 🔁 sincroniza a Strava · ✔️ posible por esa ruta

---

## Los 3 patrones

1. **Wearables y plataformas deportivas → SÍ abren API** (WHOOP, Strava, Polar, Garmin, Oura, Fitbit, Withings, Coros, Suunto, Wahoo, TrainingPeaks). Son la vía limpia.
2. **Apps de marca de ropa/tenis → CIERRAN datos** (Nike, Adidas) y **Peloton/MyFitnessPal** también. Solo indirecto.
3. **Apple Health / Health Connect = el "colector universal"**: casi todo lo que no abre API sí escribe ahí. Por eso, tener **una app propia** que lea de Apple Health/Health Connect nos da acceso a las cerradas (Nike, Adidas, Peloton…) por la puerta de atrás legítima.

## Recomendación de ingesta (orden)
1. **Agregador (Vital/Junction o Terra)** → cubre de un jalón WHOOP, Strava, Garmin, Polar, Oura, Fitbit, Withings…
2. **App propia ligera** (fase posterior) con **Apple Health + Health Connect** → suma Nike, Adidas, Samsung, etc.
3. **PPG/IBI crudo (DFA-α1)** NO sale de ninguna de estas → hardware propio / Polar H10.
