# TID-MAX · App (Etapa 0 "Ventana") — PWA

Primera etapa de la app, como **PWA instalable** que **reutiliza el dashboard**. Objetivo del v0:
entrar → conectar tus datos → ver tu **readiness** y el **coach del día** en el teléfono, como app.

## Por qué PWA (y no nativo aún)
- **Reutiliza** el motor y el `data.json` que ya existen — cero rework.
- **Instalable** en iPhone/Android ("Agregar a inicio") — se abre a pantalla completa, como app, sin App Store.
- **Se despliega en Vercel** igual que `web/` (root = `tid-max/app`).
- **No amarra:** más adelante se puede envolver en nativo (Flutter/React Native) sin tirar esto.
- La v1 (GPS + FC en vivo por BLE) puede empezar aquí con Web APIs, o pasar a nativo si el BLE crudo lo exige.

## Qué incluye este v0
- `index.html` — app de una sola página con 4 pestañas: **Hoy · Entrenar · Datos · Perfil**.
  - **Hoy:** semáforo, recovery/HRV/sueño y coach del día (lee `data.json`, el mismo del dashboard).
  - **Entrenar:** plan del día + botón "Iniciar entrenamiento" (teaser de la v1).
  - **Datos:** pantalla "Conecta tus fuentes" (WHOOP/Strava/Polar/Garmin/Apple Salud) — botones OAuth (stub).
  - **Perfil:** atleta, deporte, fase.
- `manifest.webmanifest` + `sw.js` + `icon-*.png` — lo que la hace **instalable**.
- `data.json` — copia del reporte (por ahora); el pipeline (`software/tid_web.py`) puede escribir aquí también.

## Probar local
```bash
cd tid-max/app
python3 -m http.server 8080
# abre http://localhost:8080  (en el teléfono: misma red → http://<ip-de-tu-mac>:8080)
```

## Desplegar (Vercel)
Nuevo proyecto en Vercel con **Root Directory = `tid-max/app`**, framework **Other** (estático).
Cada push que toque `app/` redepliega. Luego en el teléfono: **Compartir → Agregar a inicio**.

## Conectar fuentes desde la app (sin la Mac) — `api/connect.js`
Los botones "Conectar" del tab **Datos** ya no son stub: piden a `api/connect` (serverless)
un link **"Conéctate"** del agregador **Junction** y lo abren, para que el atleta haga login
en SU marca (WHOOP/Strava/Garmin/Oura/Fitbit) desde el teléfono. El mapeo atleta→usuario se
commitea al repo (`software/agregador_users.json`) para que el sync en la nube sepa a quién bajarle.

**Config (una sola vez, desde el dashboard de Vercel → Settings → Environment Variables — no la Mac):**
```
JUNCTION_API_KEY    = (de app.junction.com > API Keys)
JUNCTION_API_BASE   = https://api.sandbox.us.tryvital.io   (la base EXACTA de tu dashboard)
JUNCTION_ENV        = sandbox        # luego: production
JUNCTION_REGION     = us
GH_TOKEN            = (ya existe, el de api/evento)
UPLOAD_SECRET       = (ya existe, la clave de sincronización de la familia)
```
La clave de sincronización se teclea en la app (Perfil → "Clave de sincronización").

## Login + alta de usuario (Fase 2) — `api/registro.js` · `api/login.js` · `api/me.js`
Cada atleta se **da de alta desde la app** (Perfil → **Crear cuenta**: nombre, correo, PIN,
deporte + la **clave de la familia**) y entra con **correo + PIN** a ver **solo su** tablero
(su `reportes/<slug>.json`, del pipeline `software/tid_multi.py`). El login usa un **token
firmado** (HMAC); `api/me` lee el reporte por la API de GitHub.

- **`api/registro`** crea la cuenta ("repo como BD"): PIN con **hash scrypt+salt** en
  `software/usuarios.json` y agrega al atleta en `software/atletas.json`. Queda logueado.
- Si no hay sesión, la app cae al **dashboard público** (no rompe nada). Perfil → Cerrar sesión.

**Config (una vez, en Vercel → tid-max-app → Settings → Environment Variables):**
```
AUTH_SECRET = (una cadena larga y aleatoria, mín. 16 caracteres — firma los tokens)
GH_TOKEN    = (ya existe — necesita "Contents: Read and write" para guardar el alta)
UPLOAD_SECRET = (ya existe — es la "clave de la familia" que pide el alta)
```
Con eso, **cualquiera de la familia** se registra desde la app. (Opcional: `TID_LOGINS`
en env sigue sirviendo para cuentas "semilla" sin darse de alta — formato
`[{"user":"correo","pin":"____","slug":"...","nombre":"..."}]`.)

> **Privacidad:** el repo es **público**, así que `usuarios.json` (con hashes) y los
> `reportes/*.json` se pueden leer en GitHub. Para privacidad de verdad, poner el repo en
> **privado** (`api/me`/`api/login` ya leen con `GH_TOKEN`). Endurecer (rate-limit) con clientes externos.
> **Privacidad real:** hoy el repo es **público**, así que los `reportes/*.json` se pueden
> leer en GitHub. Para privacidad de verdad, poner el repo en **privado** (`api/me` ya lee
> con `GH_TOKEN`, así que sigue funcionando). Los PINs viven **solo** en `TID_LOGINS` (Vercel),
> nunca en el repo ni en el chat. Endurecer (hash de PIN, rate-limit) al meter clientes externos.

## Siguiente (v0 → completar)
1. **Login real** (Apple/Google/correo) — hoy entra directo.
2. ~~**OAuth de fuentes**~~ ✅ cableado vía agregador Junction (`api/connect.js`). Falta el **paso 2**:
   sync automático en la nube (extender el cron de GitHub Actions con `agregador_sync.py`).
3. **Datos por usuario** — que cada quien vea su propio `data.json` (multiusuario).
4. **v1:** grabar workout con **GPS + FC en vivo** (BLE al H10) → tu "info en vivo de carreras".
