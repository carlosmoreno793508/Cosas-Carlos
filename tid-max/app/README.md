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

## Siguiente (v0 → completar)
1. **Login real** (Apple/Google/correo) — hoy entra directo.
2. **OAuth de fuentes** — cablear los botones "Conectar" (Strava/Polar directos o vía agregador Vital/Terra).
3. **Datos por usuario** — que cada quien vea su propio `data.json` (multiusuario).
4. **v1:** grabar workout con **GPS + FC en vivo** (BLE al H10) → tu "info en vivo de carreras".
