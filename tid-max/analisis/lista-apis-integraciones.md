# Lista de integraciones por API — con quién podemos trabajar (backlog accionable)

> "¿Con quién podemos trabajar vía su API?" — lista **priorizada y accionable** para la ingesta de TID-MAX.
> A diferencia del mapa (`mapa-conectividad-apps.md`, referencia) y del doc de agregadores
> (`agregadores-terra-vital.md`), esto es el **backlog**: a quién registrarse, en qué orden, qué da y qué lo desbloquea.
>
> Estado: ⬜ pendiente · 🟡 en trámite · ✅ activo. Actualizar conforme avanzamos.

## Cómo se lee
- **Acceso** = self-serve (te registras y listo) · aprobación (solicitas y esperan OK) · vía-agregador (Terra/Vital lo trae).
- **Desbloquea** = qué se necesita de nuestro lado para prender esa integración.
- **Prioridad** = orden sugerido por valor × esfuerzo para el beta.

---

## TIER 1 — Ya / inmediato (arrancar el beta)

| # | Socio | Acceso | Qué nos da | Desbloquea | Estado |
|---|---|---|---|---|---|
| 1 | **WHOOP** | self-serve (hecho) | Recovery, HRV, sueño, strain | — | ✅ Activo |
| 2 | **Polar** (AccessLink) | self-serve | Entrenos, FC continua, sueño; **R-R** (H10) | Registrar app en AccessLink → OAuth | ⬜ *(parser de export ya listo: `polar_flow_import.py`)* |
| 3 | **Strava** | self-serve | Actividades, FC/ritmo por seg, zonas | Crear app (Client ID/Secret) + **leer términos IA 2024** | ⬜ |
| 4 | **Agregador (Vital/Junction)** | self-serve | WHOOP+Strava+Garmin+Polar+Oura+Fitbit… de un jalón | Cuenta dev + Vital Link widget | ⬜ **decisión ítem 0.1** |

## TIER 2 — Alto valor, requieren aprobación/partner

| # | Socio | Acceso | Qué nos da | Desbloquea | Estado |
|---|---|---|---|---|---|
| 5 | **Garmin** | aprobación (Connect Dev Program) | Running/tri/ciclismo/**natación** + salud | Solicitud al programa + caso de uso | ⬜ ⭐ |
| 6 | **Oura** | self-serve | Sueño/HRV/readiness (calidad alta) | Cuenta dev + OAuth | ⬜ |
| 7 | **Fitbit** | self-serve | FC, pasos, sueño (base enorme) | App dev (cuenta Google) | ⬜ |
| 8 | **Withings** | self-serve | Peso, FC, sueño, presión | Cuenta dev + OAuth | ⬜ |
| 9 | **TrainingPeaks** | partner | Planes/carga de coaches (tri/resistencia) | Solicitud partner | ⬜ |
| 10 | **COROS / Suunto / Wahoo** | partner | Running élite / outdoor / potencia bici | Solicitud partner (según demanda) | ⬜ |

## TIER 3 — Solo indirecto (sin API propia)

| Socio | Ruta única | Requiere |
|---|---|---|
| **Nike Run Club** | Nike → Strava, o Apple Health/Health Connect | Leer de Strava o app propia |
| **Adidas Running** | Apple Health/Health Connect, o app puente | App propia (no sync a Strava) |
| **Peloton** | Sync → Strava/Health | Leer de Strava o app propia |
| **Apple Health / Samsung Health** | *Colectores* on-device | **App propia** (iOS HealthKit / Android Health Connect) |

> Estas se desbloquean **todas juntas** cuando exista la **app propia** que lea de Apple Health + Health Connect. Fase posterior.

## TIER 4 — Descartadas (hoy)
- **MyFitnessPal** — API cerrada a nuevos partners.
- **Zwift** — API limitada; solo vía Strava.

---

## Orden recomendado de ataque
1. **Decidir agregador (Vital vs Terra)** — desbloquea Tier 1 y parte del Tier 2 con **una** integración → *ítem 0.1 del tracker*.
2. **En paralelo, Strava + Polar directos** (gratis) si queremos evitar $/usuario en las 2-3 fuentes clave.
3. **Solicitar Garmin** (aprobación tarda) — arrancar el trámite temprano.
4. **Oura/Fitbit/Withings** self-serve conforme lleguen usuarios que los usen.
5. **App propia (Apple Health/Health Connect)** — fase posterior; abre Nike/Adidas/Samsung/Peloton de golpe.

## Recordatorio de moat
Ninguna de estas entrega **PPG/IBI crudo continuo** para DFA-α1 en todos los deportes. El **Polar H10** sí da R-R
(por eso el parser ya lo procesa), y el **hardware TID-MAX** es la fuente propia de dato crudo. Las APIs son para
**cobertura y enganche**; el moat es el dato crudo + el motor de IA.
