# Arquitectura

## Principio central: un núcleo, muchas carcasas

```
                    ┌───────────────────────────┐
                    │      @tvapp/core (TS)      │
                    │  parser M3U · Xtream · EPG │
                    │  modelos de dominio        │
                    └────────────┬──────────────┘
                                 │  (lógica pura, sin plataforma)
        ┌────────────────┬───────┴───────┬─────────────────┐
        │                │               │                 │
   apps/web         React Native      (Roku:            futuros
 (Web/Tizen/webOS)  (Fire/Android/     BrightScript,     clientes
   ya implementado   Apple TV)         reimplementa)
```

- **`@tvapp/core`** no importa nada de un navegador ni de un framework de UI. Solo
  transforma datos: texto M3U → `PlaylistContent`, respuestas Xtream → `MediaItem[]`.
  Por eso es testeable con `node:test` y reutilizable en cualquier runtime JS.
- **Las apps** (carcasas) aportan la UI, la navegación por control remoto y el
  reproductor de video propio de cada plataforma.

## Flujo de datos

1. El usuario da de alta una **Playlist** (M3U o Xtream) — pantalla "Nueva lista
   de reproducción". Se guarda **solo en el dispositivo** (`localStorage` en web).
2. Al abrirla:
   - **M3U**: se descarga el texto y `parseM3U()` lo normaliza.
   - **Xtream**: `XtreamClient` llama a `player_api.php` y normaliza categorías y
     streams.
3. Ambos caminos producen el mismo `PlaylistContent` (`categories` + `items`), que
   la UI pinta igual sin saber de dónde vino.
4. Al elegir un item, se reproduce `item.streamUrl` (HLS vía hls.js/nativo).

## Contratos clave

- `parseM3U(text: string): PlaylistContent` — pura, sin red.
- `XtreamClient(config, fetchFn?)` — `fetchFn` inyectable para tests y para
  plataformas sin `fetch` global.
- Todo lo reproducible es un `MediaItem` con `type` (`live` | `movie` | `series`)
  y `streamUrl`.

## Por qué separar así

- **Portabilidad:** el mismo parser corre en web, React Native y Node.
- **Testeo:** la lógica frágil (parsing, construcción de URLs) se prueba sin UI ni
  red — ver `packages/core/test`.
- **Cumplimiento:** el núcleo no conoce ninguna fuente concreta de contenido; el
  usuario aporta la suya con derechos.
