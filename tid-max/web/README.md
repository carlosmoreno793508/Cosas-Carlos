# TID-MAX · Web (dashboard en la nube)

Dashboard de readiness de TID-MAX como **sitio estático** en Vercel. Es la **Fase 1** del ecosistema
independiente: un tablero con **dirección fija 24/7** que la familia (Karla, Gael) abre sin Claude,
sin túnel y sin depender de que la Mac esté prendida.

## Cómo funciona (separación diseño / datos)

- **`index.html`** — el dashboard (diseño + render). NO tiene datos hardcodeados: al abrir, hace
  `fetch("./data.json")` y pinta el reporte. Sirve para cualquier día y cualquier atleta.
- **`data.json`** — los datos del día (semáforo, recovery, HRV, sueño, forma, nutrición, alertas).
  Es lo ÚNICO que cambia día a día.
- **`vercel.json`** — sirve estático y evita cachear `data.json` (para que actualice al instante).

El motor (WHOOP + determinista + agentes Claude) vive en `../software`. El puente es
**`../software/tid_web.py`**, que convierte `coach-hoy.json` → `data.json`.

## Flujo para actualizar el tablero

```bash
cd ../software
python3 whoop_sync.py && python3 tid_data.py && python3 tid_agent.py   # datos + reporte
python3 tid_web.py                                                      # escribe web/data.json
cd ..
git add web/data.json && git commit -m "reporte del día" && git push    # Vercel redepliega solo
```

## Deploy en Vercel (una sola vez)

1. En Vercel → **Add New… → Project** → importa el repo `Cosas-Carlos`.
2. En **Root Directory** elige **`tid-max/web`**.
3. Framework Preset: **Other** (es estático, sin build). Build Command: vacío. Output: `.`
4. **Deploy**. Te da una URL fija (p. ej. `tid-max.vercel.app`) — esa es la que compartes con Karla.
5. (Opcional) Protégela con **Vercel Password Protection** o un dominio propio para que no sea pública.

Cada `git push` que toque `web/` redepliega solo.

## Roadmap del ecosistema (siguientes fases)

- **Fase 2 — automatizar los datos sin la Mac:** un job programado (Vercel Cron o GitHub Actions)
  corre el pipeline en la nube cada mañana, regenera `data.json` y lo publica. WHOOP se baja solo.
- **Fase 3 — subir foto/texto sin Python:** ✅ CONSTRUIDA. Página `subir.html` + función serverless
  `api/comida.js` (Vercel): recibe la foto, la estima con Claude (visión) y escribe la comida en
  `data.json` (commit al repo → el tablero la muestra). Ver deploy ↓.
- **Fase 4 — notificación diaria** a Carlos y Karla con el link o la imagen del reporte.

## Fase 3 — activar la subida de comidas (deploy)

El código ya está (`subir.html` + `api/comida.js`). Para encenderlo, en Vercel → tu proyecto →
**Settings → Environment Variables**, agrega 3 variables (Production):

| Variable | Valor |
|---|---|
| `ANTHROPIC_API_KEY` | tu clave de Claude (Anthropic) |
| `GH_TOKEN` | un PAT fino de GitHub con permiso **Contents: Read and write** en el repo (para que la función escriba `data.json`) |
| `UPLOAD_SECRET` | una contraseña simple que teclearán en `subir.html` (solo la familia) |

Luego **Redeploy**. La función queda en `https://<tu-dominio>/api/comida` y la página en
`https://<tu-dominio>/subir`. Abres `subir.html` en el teléfono, tomas la foto, escribes la
contraseña → la comida aparece en el tablero en ~1 min.

Notas: la foto se comprime en el navegador (≤1024 px) para ir rápido y barato. Cada mañana el Cron
regenera `data.json` (borra el consumo del día → empieza limpio). El commit lo hace el `GH_TOKEN`,
no el `GH_PAT` de Actions (ese solo tiene permiso de Secrets).
