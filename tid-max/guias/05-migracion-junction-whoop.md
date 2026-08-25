# Guía 05 — Migrar WHOOP al agregador (Junction) · adiós a los tokens frágiles

**Por qué:** hasta hoy bajábamos WHOOP con nuestro propio OAuth y **un solo refresh
token** guardado como secreto de GitHub. El token de WHOOP rota en cada sync y de un
solo uso; cualquier tropiezo lo mata. Ya se rompió 4 veces (incluida la regeneración
del Client Secret). **No escala ni a un usuario.**

**La solución:** que WHOOP entre por **Junction** (agregador). Junction guarda el token
por-usuario en su bóveda, lo refresca del lado servidor y nos **empuja** los datos por
webhook. El atleta conecta **una vez desde el teléfono** y no volvemos a tocar un token.

El código ya está (PR de esta rama): `api/connect.js` (conectar/reconectar por-usuario
con token de sesión) y `api/webhook.js` (recibe el push de Junction y dispara el
pipeline). Falta **la configuración del dashboard**, que es lo que hace esta guía.

---

## Parte A — Configuración en el dashboard de Junction (una sola vez)

1. **WHOOP como proveedor (BYOO — "bring your own OAuth").**
   WHOOP es un proveedor que exige credenciales propias. En el dashboard de Junction
   (https://app.junction.com) → *Providers / Connections* → **WHOOP** → pega el
   **Client ID** y **Client Secret** de tu app de WHOOP (los mismos del dashboard de
   WHOOP developer). En WHOOP developer, agrega a los **redirect URIs** el callback que
   te indique Junction (algo como `https://api.prod.us.junction.com/...`). Junction te
   dice la URL exacta en esa pantalla.

2. **Pasar a PRODUCTION.** Hoy estamos en `sandbox` (datos simulados). Para datos reales
   de la banda de Gael necesitas las llaves de **production** de Junction.

3. **Registrar el webhook.** Dashboard de Junction → *Webhooks* → **Add endpoint**:
   - URL: `https://tid-max-app.vercel.app/api/webhook`
   - Eventos: los de datos (workouts, sleep, recovery, body, daily/historical) y, si
     está, `provider.connection.created`.
   - Copia el **Signing Secret** (formato `whsec_...`) — lo necesitas en la Parte B.

---

## Parte B — Variables de entorno en Vercel (proyecto `tid-max-app`)

Settings → Environment Variables. Pon/actualiza:

| Variable | Valor |
|---|---|
| `JUNCTION_API_KEY` | tu API key de **production** de Junction |
| `JUNCTION_API_BASE` | la base **exacta** de production que te da tu dashboard (ej. `https://api.prod.us.junction.com`) |
| `JUNCTION_ENV` | `production` |
| `JUNCTION_REGION` | `us` (o `eu`) |
| `JUNCTION_WEBHOOK_SECRET` | el `whsec_...` del paso A.3 (sin él, el webhook responde 200 pero **no dispara** — es a prueba de abuso) |
| `GH_ACTIONS_TOKEN` | PAT fino con permiso **"Actions: write"** en el repo, para que el webhook pueda disparar el pipeline. (Si tu `GH_PAT` actual ya tiene Actions:write, el webhook lo usa como respaldo.) |
| `AUTH_SECRET` | la MISMA con que `/api/login` firma los tokens (ya debería existir; `connect.js` la usa para el conectar por-usuario) |

> Nota: en **software/.env** (para pruebas locales con `agregador_*.py`) también va
> `JUNCTION_WEBHOOK_SECRET` si quieres verificar firmas en el receptor local.

---

## Parte C — Conectar a Gael (desde el teléfono, 1 minuto)

1. Gael abre la app **con su sesión** (login), va a **Datos → Conectar → WHOOP**.
   (El botón ya usa su token de sesión: guarda el evento/fuente en SU cuenta, no en la
   de otro.)
2. Se abre el widget de Junction; elige **WHOOP**, hace login en WHOOP y autoriza.
3. Junction empieza a jalar su histórico y a **empujar** lo nuevo por webhook.

## Parte D — Cambiar la fuente de Gael a "agregador"

Cuando Gael ya conectó (Parte C), cambiar en `tid-max/software/atletas.json` su entrada:

```json
{ "slug": "gael-moreno", "nombre": "Gael Moreno", "deporte": "natacion",
  "fuente": "agregador", "agregador_atleta": "gael-moreno",
  "perfil": "nutricion-gael.json", "planes": ["plan-macro.json","plan-semana.json"], "activo": true }
```

- `fuente`: `whoop` → **`agregador`** (deja de usar nuestro OAuth propio).
- Quitar `evento.json` de `planes` no es necesario (el evento ya es por-atleta vía la app).
- Avísame y yo hago este cambio + disparo un run para confirmar que sus datos vuelven a
  fluir vía Junction.

---

## Cómo probar que quedó

- **Webhook vivo:** abre en el navegador `https://tid-max-app.vercel.app/api/webhook`
  → debe responder `{"ok":true,"servicio":"tidmax-webhook"}`.
- **Push real:** tras conectar a Gael, en minutos debería llegar un evento y disparar un
  run del pipeline (pestaña Actions). El reporte de Gael vuelve a moverse **sin** que
  nadie toque un token.
- **Reconectar:** si algún día WHOOP pide re-permiso, el atleta solo vuelve a
  **Datos → Conectar** — cero intervención nuestra.

---

## Qué ganamos (vs. el token manual)

| | Antes (OAuth propio) | Ahora (Junction) |
|---|---|---|
| Token | 1 secreto de GitHub, re-escrito por CI | bóveda por-usuario en Junction |
| Rotación | nuestra (frágil, se rompió 4×) | de Junction (servidor, con lock) |
| Datos | cron 2×/día (polling) | **webhook** (push casi en vivo) |
| Si expira | Carlos re-autoriza en la Mac | el atleta toca **Reconectar** |
| Multi-marca | un flujo por marca | una integración: WHOOP/Oura/Garmin/Polar/… |
