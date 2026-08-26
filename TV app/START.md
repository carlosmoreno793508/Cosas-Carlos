# Ver MoreTV en tu computadora — paso a paso

Esto levanta **MoreTV en el navegador** con contenido de ejemplo real
(reproducible), usando tu propio servidor local. Funciona en **Windows, macOS y
Linux**.

## Requisitos (una sola vez)

1. Instala **Node.js 22 o superior**: https://nodejs.org (elige la versión "LTS").
2. Descarga el proyecto (si no lo tienes):
   ```bash
   git clone https://github.com/carlosmoreno793508/Cosas-Carlos.git
   ```

## Opción A — Un solo comando (macOS / Linux / Git Bash en Windows)

```bash
cd "Cosas-Carlos/TV app"
npm install
npm run demo
```

Se abre en: **http://localhost:5173**
(el servidor de contenido queda en http://localhost:8080)

Para detener: `Ctrl + C`.

## Opción B — Manual (dos terminales, sirve en cualquier sistema)

```bash
# 1) Entra a la carpeta e instala (una vez)
cd "Cosas-Carlos/TV app"
npm install
npm run build:core

# 2) Terminal 1 — arranca el servidor de contenido
npm run start:server

# 3) Terminal 2 — arranca la app web
npm run dev:web
```

Abre **http://localhost:5173** en tu navegador (Chrome o Edge recomendados).

## Cómo usarla

1. En "Elige tu lista", pulsa **➕ Añadir lista**.
2. Deja el modo **Xtream** y escribe:
   - **URL:** `http://localhost:8080`
   - **Usuario:** `carlos`
   - **Contraseña:** `cambia-esto`
3. **Crear lista de reproducción** → entra al dashboard **LIVE / MOVIES / SERIES**.
4. En **MOVIES** verás *Big Buck Bunny* (se reproduce de verdad). En **LIVE** un
   canal de prueba, y en **SERIES** una serie con su episodio.

### Navegar como en un TV

Aunque sea en el navegador, está pensada para control remoto:
- **Flechas** = mover el foco (D-pad)
- **Enter** = seleccionar (OK)
- **Retroceso/Backspace** = volver (Atrás)

## Poner TU propio contenido

Edita `apps/server/data/catalog.example.json` (o copia a `catalog.json`) y agrega
tus canales/películas con sus URLs. Guía completa en `apps/server/README.md`.

## Usar TU propia lista IPTV (reproductor tipo TiviMate / Smarters)

MoreTV es un **reproductor**: puedes conectar la lista **M3U** o las credenciales
**Xtream** de tu proveedor y reproducir tu contenido.

1. En "Añadir lista", elige **M3U** o **Xtream** y pon tus datos.
2. **Importante para el navegador:** Chrome bloquea (por CORS) las listas de otros
   servidores. Para reproducirlas en la compu, activa el **proxy**:
   - En el dashboard, pulsa el **engrane ⚙ → "Usar proxy local" → Guardar → ‹ Volver**.
   - Esto hace que tu lista pase por el servidor incluido (`http://localhost:8080/proxy`)
     y se reproduzca sin el bloqueo de Chrome.
3. En **Fire TV, Android TV, Apple TV o Samsung** (apps nativas) **no** necesitas el
   proxy: reproducen tu lista directamente.

> El proxy solo reenvía la fuente que TÚ configuras (tu propia suscripción/lista).
> Usa contenido para el que tengas derechos (ver `docs/LEGAL.md`).
