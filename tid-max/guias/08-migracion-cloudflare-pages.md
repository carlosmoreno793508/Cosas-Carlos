# Guía 08 — Migrar TID-MAX a Cloudflare Pages (adiós Vercel)

**Por qué:** Vercel deshabilitó el despliegue (`402 Payment Required / DEPLOYMENT_DISABLED`). Nos
mudamos a **Cloudflare Pages**: gratis, **permite uso comercial**, corre funciones y auto-despliega
desde GitHub igual que Vercel. TID-MAX queda como un **proyecto NUEVO e independiente** del Worker
`natacion` (SwimMx) — no se toca ese.

## Qué ya cambié en el repo (listo en el PR)
- `tid-max/app/functions/api/*.js` — las 9 funciones portadas a **Pages Functions** (mismo comportamiento;
  solo cambia el envoltorio `req,res → Request/Response` y `process.env → env`). Usan `node:crypto`
  (HMAC/scrypt) vía `nodejs_compat`.
- `tid-max/app/wrangler.toml` — `pages_build_output_dir="."` + `compatibility_flags=["nodejs_compat"]`.
- `tid-max/app/_headers` — reemplaza las cabeceras de `vercel.json` (no-store en data.json, nosniff).
- **Eliminados:** `tid-max/app/api/` (funciones Vercel) y `tid-max/app/vercel.json`.
- El frontend usa rutas **relativas** (`/api/...`), así que **no cambió nada** de la UI.

---

## Parte A — Crear el proyecto Pages (una vez, en tu dashboard)
1. **dash.cloudflare.com → Workers & Pages → Create → Pages → Connect to Git**.
2. Autoriza GitHub y elige el repo **`Cosas-Carlos`**.
3. **Project name:** `tid-max` (queda independiente del Worker `natacion`).
4. **Production branch:** `main`.
5. **Build settings:**
   - Framework preset: **None**.
   - Build command: **(vacío)**.
   - Build output directory: **(déjalo en la raíz / `/`)**.
   - **Root directory (Advanced): `tid-max/app`** ← importante, es donde vive la app.
6. **Save and Deploy.** (El primer deploy puede quedar incompleto hasta poner las variables; seguimos.)

## Parte B — Compatibility flag (obligatorio para las funciones)
En el proyecto → **Settings → Functions → Compatibility flags**: agrega **`nodejs_compat`** en
**Production** y en **Preview**. Compatibility date: **2026-10-01** (o más reciente).
> Sin este flag, `node:crypto`/`Buffer` fallan y el login/API no responde.

## Parte C — Variables de entorno (las MISMAS que tenías en Vercel)
En **Settings → Environment variables** → agrégalas en **Production** y **Preview**.
🔒 Cópialas desde Vercel (Project → Settings → Environment Variables) — **no las pegues en el chat.**

| Variable | Para qué | ¿Obligatoria? |
|---|---|---|
| `AUTH_SECRET` | firma los tokens de sesión (login/me/evento/…) | **Sí** |
| `GH_TOKEN` | PAT fino "Contents: Read and write" (repo como BD) | **Sí** |
| `TID_LOGINS` | cuentas semilla (Gael, Carlos) — JSON | **Sí** (para entrar hoy) |
| `ANTHROPIC_API_KEY` | visión del agente de comida | Para /api/comida |
| `UPLOAD_SECRET` | clave de la familia (alta/registro, connect legacy) | Si usas registro |
| `JUNCTION_API_KEY` + `JUNCTION_*` | conectar fuentes (si sigues con Junction) | Opcional |
| `JUNCTION_WEBHOOK_SECRET`, `GH_ACTIONS_TOKEN` | webhook push | Opcional |

Después de guardarlas: **Deployments → Retry deployment** (o empuja un commit) para que tomen efecto.

## Parte D — La URL nueva y la app nativa
- El sitio quedará en **`https://tid-max.pages.dev`** (o el nombre que pusiste). Opcional: en
  **Custom domains** puedes poner un dominio propio (ya tienes Domains en Cloudflare).
- **La app nativa (Capacitor)** apunta a la URL vieja de Vercel. Hay que cambiar
  `tid-max/native/capacitor.config.json` → `server.url` a la **URL nueva de Cloudflare**.
  Dime la URL final (pages.dev o dominio) y lo actualizo + recompilas en Xcode.

## Parte E — El pipeline diario (no cambia)
GitHub Actions sigue haciendo commit de `data.json`/reportes; con la **integración Git de Pages**, cada
push a `main` **auto-despliega** — igual que Vercel. No hay que tocar el workflow.

---

## Verificación (cuando esté desplegado)
- `https://tid-max.pages.dev/` abre la app.
- `GET /api/webhook` → `{"ok":true,"servicio":"tidmax-webhook"}` (confirma que las funciones corren).
- Login con tu cuenta semilla → entra y carga tu reporte (`/api/me`).
- Nota: la verja scrypt de usuarios dados de alta depende de `scryptSync` en `nodejs_compat`; las cuentas
  semilla (`TID_LOGINS`) funcionan siempre. Lo validamos en el primer login real.

## Cuando quede verde
- Apagamos/ignoramos Vercel (o bajamos a Hobby si quieres conservarlo de respaldo).
- El proyecto `tid-max/web` (dashboard estático) se puede migrar igual (es solo estático, trivial).
