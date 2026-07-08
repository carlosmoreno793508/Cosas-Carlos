# @tvapp/server — Tu servidor M3U / Xtream para MoreTV

Servidor propio, **sin dependencias** (solo Node 22+), compatible con la API
**Xtream Codes** y con exportación **M3U**. MoreTV (o cualquier reproductor
compatible) se conecta con URL + usuario + contraseña y ve **tu** catálogo.

> El servidor **no aloja video**: guarda las URLs de tus streams en un JSON y
> redirige a ellas. Pon solo contenido para el que tengas derechos: contenido
> propio, **TV abierta / FAST gratuita** o material licenciado. Ver
> `../../docs/LEGAL.md`.

## Arrancar en 1 minuto

```bash
cd "TV app/apps/server"

# 1) Copia los ejemplos y edítalos con tu contenido y tus usuarios
cp data/catalog.example.json data/catalog.json
cp data/users.example.json   data/users.json

# 2) Arranca
npm start          # http://localhost:8080

# 3) Pruébalo
curl "http://localhost:8080/health"
```

En MoreTV, crea una lista **Xtream** con:
- **URL:** `http://<ip-de-tu-servidor>:8080`
- **Usuario / Contraseña:** los de `data/users.json`

O una lista **M3U** con:
`http://<ip-de-tu-servidor>:8080/get.php?username=U&password=P&type=m3u_plus`

## Cómo se administra el catálogo (`data/catalog.json`)

Tres secciones: `live` (canales), `movies` (películas) y `series`.

```jsonc
{
  "live": [
    { "id": "101", "name": "Canal 1", "logo": "https://…/logo.png",
      "category": "TV Abierta", "epgId": "canal1.mx",
      "url": "https://…/canal1.m3u8" }
  ],
  "movies": [
    { "id": "201", "name": "Mi Película", "logo": "https://…/poster.jpg",
      "category": "Acción", "rating": 8.2, "year": "2024",
      "url": "https://…/pelicula.mp4" }
  ],
  "series": [
    { "id": "301", "name": "Mi Serie", "cover": "https://…/cover.jpg",
      "category": "Drama", "rating": 7.5, "year": "2024",
      "seasons": [
        { "season": 1, "episodes": [
          { "id": "3011", "title": "Episodio 1", "url": "https://…/s01e01.mp4" }
        ]}
      ]}
  ]
}
```

## Cómo actualizar con contenido nuevo

1. Edita `data/catalog.json` (añade canales/pelis/series).
2. Recarga **sin reiniciar**: `curl http://localhost:8080/reload`
3. MoreTV lo verá al reabrir la sección (o con su auto-refresco).

> Para automatizarlo (p. ej. un script que agregue estrenos cada noche), basta
> con que tu proceso reescriba `catalog.json` y llame a `/reload`. Se puede
> conectar a cualquier fuente tuya: una carpeta de videos, tu CDN, una API, etc.

### Importar automáticamente desde una M3U (`ingest.mjs`)

Incluye una herramienta que importa una lista M3U (archivo o URL) a tu catálogo,
**deduplica por URL** y marca la fecha de alta (para "Recién agregado"):

```bash
# Importar canales y recargar el servidor en caliente
node src/ingest.mjs --m3u ./mis-canales.m3u --section live --reload

# Importar películas forzando una categoría
node src/ingest.mjs --m3u https://ejemplo/pelis.m3u --section movies --category "Estrenos" --reload
```

### Programarlo con cron (actualización automática)

Para traer contenido nuevo cada noche a las 3:00 am:

```cron
0 3 * * *  cd /ruta/TV\ app/apps/server && node src/ingest.mjs --m3u https://tu-fuente/lista.m3u --section movies --reload >> ingest.log 2>&1
```

La app MoreTV también **se auto-refresca cada 10 minutos** y trae lo nuevo sola;
además tiene un botón ⟳ para refrescar al instante y una categoría
**🆕 Recién agregado**.

## Endpoints

| Ruta | Qué hace |
| --- | --- |
| `/health` | Estado y conteo del catálogo |
| `/player_api.php?username=&password=&action=…` | API Xtream (categorías, streams, series) |
| `/get.php?username=&password=&type=m3u_plus` | Exporta el catálogo como M3U |
| `/{live\|movie\|series}/{u}/{p}/{id}.{ext}` | Redirige (302) al stream real |
| `/reload` | Relee `catalog.json` y `users.json` en caliente |

## Variables de entorno

- `PORT` — puerto (por defecto `8080`).
- `DATA_DIR` — carpeta de `catalog.json` / `users.json` (por defecto `./data`).
- `PUBLIC_URL` — URL pública para las URLs de stream (p. ej. `http://mi-dominio:8080`).

## Desplegar para verlo fuera de casa

Cualquier VPS o PC con Node sirve. Detrás de un proxy con HTTPS (Caddy/Nginx)
podrás usar `https://…`. Recuerda cambiar las contraseñas de `users.json` antes
de exponerlo a internet.

## Pruebas

```bash
npm test           # 7 casos: auth, API Xtream, M3U y resolución de streams
```
