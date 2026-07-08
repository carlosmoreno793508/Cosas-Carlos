# Instalar en LG Smart TV (webOS)

Los televisores **LG** con webOS corren la misma app web (`apps/web`), empaquetada
como un paquete **.ipk**. Para uso personal basta con el *modo desarrollador*.

## Requisitos

- [webOS TV CLI (ares)](https://webostv.developer.lge.com/develop/tools/cli-installation)
  (`npm i -g @webosose/ares-cli`).
- La app **LG Developer Mode** instalada en el TV (desde la LG Content Store) y una
  cuenta de desarrollador LG.
- Un `icon.png` (80×80) y `largeIcon.png` (130×130) en `apps/web/webos/`.

## Empaquetar e instalar

```bash
cd "TV app"
npm install
npm run build:web            # genera apps/web/dist

# Copia el manifiesto webOS al dist
cp apps/web/webos/appinfo.json apps/web/dist/
cp apps/web/webos/icon.png apps/web/webos/largeIcon.png apps/web/dist/ 2>/dev/null || true

# Empaqueta el .ipk
ares-package apps/web/dist -o out/

# Conecta con el TV (modo desarrollador activo) e instala
ares-setup-device            # registra tu TV una vez
ares-install --device <tu-tv> out/com.moretv.app_0.1.0_all.ipk
ares-launch --device <tu-tv> com.moretv.app
```

## Notas

- webOS usa un WebView con MSE, así que `hls.js` reproduce HLS sin problema.
- El control remoto ya está soportado en `src/remote.ts` (tecla "Atrás" de webOS
  incluida).
- **Sin límite de CORS** como en un navegador de escritorio: la app reproduce
  directamente las listas M3U/Xtream que configures (usa fuentes con derechos).
- Publicación en la **LG Content Store**: requiere cuenta de desarrollador y pasar
  su revisión (solo si quieres distribuirla; para ti basta el sideload).
