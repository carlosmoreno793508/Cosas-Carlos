# Guía 05 · Migrar WHOOP al agregador (Junction) — self-serve, sin re-autorizar a mano

**Problema que resuelve:** hoy el token de WHOOP es un refresh token rotativo guardado
como secreto de GitHub. Sobrevive una sincronización y a la mínima falla (503, dos
corridas cercanas, cambio de Client Secret) **se muere** y hay que re-autorizar desde la
Mac. No escala ni a un usuario. La solución es que WHOOP entre **por Junction**: el token
vive en Junction (no en nuestros secretos), el usuario conecta/reconecta desde la app, y
Junction nos **empuja** los datos por webhook.

Este código ya quedó listo (`api/connect.js`, `api/webhook.js`, y el driver que ya lee
atletas `fuente: agregador`). Faltan **pasos de configuración que solo tú puedes hacer** en
los dashboards de Junction, Vercel y GitHub.

---

## Parte A · Junction dashboard (una vez)

1. Entra a https://app.junction.com → tu proyecto.
2. **WHOOP como proveedor (BYOO — Bring Your Own OAuth):** WHOOP exige credenciales
   propias. En Junction: *Providers → WHOOP → Enable* y pega el **Client ID** y **Client
   Secret** de tu app de WHOOP (los mismos del dashboard de WHOOP). Configura el
   **redirect URI** que Junction te indique dentro del dashboard de WHOOP.
3. **Producción vs sandbox:** para datos reales de la banda de Gael necesitas llaves de
   **producción** (`API base` tipo `https://api.us.junction.com`). Sandbox solo da datos
   simulados.
4. **Webhook:** *Webhooks → Add endpoint* →
   URL: `https://tid-max-app.vercel.app/api/webhook`
   Suscríbete a los eventos de datos (workouts / sleep / recovery / body / daily) y, si lo
   ofrece, `provider.connection.created`. Copia el **Signing Secret** (formato `whsec_...`).

## Parte B · Variables de entorno en Vercel (proyecto tid-max-app)

Settings → Environment Variables (no las pegues en el chat):

| Variable | Valor |
|---|---|
| `JUNCTION_API_KEY` | API key de Junction |
| `JUNCTION_API_BASE` | la base EXACTA del dashboard (producción para datos reales) |
| `JUNCTION_ENV` | `production` (o `sandbox` para probar) |
| `JUNCTION_REGION` | `us` |
| `JUNCTION_WEBHOOK_SECRET` | el Signing Secret `whsec_...` del webhook |
| `AUTH_SECRET` | la MISMA con que `/api/login` firma los tokens (ya debería existir) |
| `GH_ACTIONS_TOKEN` | PAT con permiso **Actions: write** (para que el webhook dispare el pipeline). Si no lo pones, cae a `GH_PAT`/`GH_TOKEN`. |

> Seguridad del webhook: si `JUNCTION_WEBHOOK_SECRET` NO está puesto, `/api/webhook`
> responde 200 pero **no dispara nada** — así nadie más puede provocar corridas. En cuanto
> pongas el secreto, solo los eventos con firma Svix válida disparan el pipeline.

## Parte C · Conectar / reconectar desde la app

- El usuario entra a **Datos → Conectar** (o el botón de reconectar) → se abre el widget de
  Junction → elige WHOOP → hace login en WHOOP → listo. El token queda en Junction.
- `api/connect.js` ahora autentica con el **token de sesión** del usuario (cada quien
  conecta SU fuente; el slug sale del token, no se puede suplantar).

## Parte D · Cambiar a Gael de WHOOP-directo → Junction

En `tid-max/software/atletas.json`, la entrada de Gael cambia de:

```json
{ "slug": "gael-moreno", "fuente": "whoop", ... }
```

a:

```json
{ "slug": "gael-moreno", "fuente": "agregador", "agregador_atleta": "gael-moreno", ... }
```

**Hazlo solo DESPUÉS** de que Gael haya conectado su WHOOP por el widget (Parte C) y de
que exista su mapeo en `agregador_users.json`. Si lo cambias antes, su fuente queda vacía
hasta que conecte. (Se puede tener a Gael en `agregador` y a otros en `whoop`/`polar` sin
problema — el driver es por-atleta.)

## Cómo verificar que quedó

1. Gael conecta WHOOP por el widget → aparece su entrada en `agregador_users.json`.
2. Haces una actividad (o esperas datos) → Junction manda webhook → `/api/webhook` dispara
   el workflow → en minutos el reporte de Gael se actualiza **sin tocar nada**.
3. Ya no necesitas `whoop_auth.py` ni re-guardar tokens: si algo se desconecta, el usuario
   solo toca **Reconectar** en la app.

---

**Resumen:** después de esta migración, dar de alta un cliente nuevo = "conecta tu WHOOP"
desde su teléfono. Cero mantenimiento de tokens de tu lado.
