# @tvapp/roku — Canal Roku de MoreTV (fase 3)

Roku **no ejecuta JavaScript**: usa **BrightScript + SceneGraph** (XML). Por eso
este cliente **reimplementa** la lógica del núcleo (`@tvapp/core`) en BrightScript
—es pequeña y directa de portar— en lugar de reutilizarla.

## Qué incluye este scaffold

```
apps/roku/
├── manifest                     # metadatos del canal (título, iconos, splash)
├── source/
│   ├── main.brs                 # entrada: crea la escena y el bucle de eventos
│   ├── Xtream.brs               # cliente Xtream (URLs + normalización JSON)
│   └── M3U.brs                  # parser de listas M3U
├── components/
│   ├── MainScene.xml/.brs       # escena: rejilla de canales + reproductor
│   ├── ContentLoader.xml/.brs   # Task de red (descarga get_live_streams)
│   └── ChannelItem.xml/.brs     # tarjeta de canal (póster + título + foco)
└── images/                      # iconos y splash (añade los de la marca)
```

Equivalencias con el núcleo TypeScript:

| Núcleo (`@tvapp/core`)      | Roku (BrightScript)                    |
| --------------------------- | -------------------------------------- |
| `xtream.ts` buildStreamUrl  | `Xtream.brs` `Xtream_StreamUrl`        |
| `xtream.ts` player_api      | `Xtream.brs` `Xtream_ApiUrl`           |
| `getLiveStreams()`          | `Xtream_LiveToContent` + `ContentLoader` |
| `m3u.ts` parseM3U           | `M3U.brs` `ParseM3U`                   |

## Configurar la fuente

Edita las credenciales en `source/main.brs` (o implementa una pantalla de alta
con `roRegistry` para persistirlas):

```brightscript
scene.serverUrl = "http://TU-SERVIDOR:8080"
scene.username = "carlos"
scene.password = "cambia-esto"
```

Apunta a **tu servidor** `@tvapp/server` o a un proveedor Xtream con licencia.

## Probar en un Roku (modo desarrollador)

1. En el Roku: **Home ×3, Arriba ×2, Derecha, Izquierda, Derecha, Izquierda,
   Derecha** para abrir *Developer Settings*; activa el modo desarrollador y
   anota la IP.
2. Empaqueta y sube el canal:
   ```bash
   cd "TV app/apps/roku"
   zip -r moretv.zip manifest source components images
   # Sube moretv.zip en http://<IP-DEL-ROKU> (Development Application Installer)
   curl -s -F "mysubmit=Install" -F "archive=@moretv.zip" \
        --user rokudev:<tu-clave> http://<IP-DEL-ROKU>/plugin_install
   ```
3. El canal aparece en la pantalla de inicio del Roku.

## Estado

Scaffold funcional de **TV en vivo** (rejilla + reproducción HLS). Pendientes de
ampliar en siguientes iteraciones: VOD/series, EPG, favoritos y búsqueda —
portando el resto de `Xtream.brs`/`M3U.brs` (la base ya está).

> Nota: este scaffold no se compila en este entorno (requiere un Roku o el
> simulador de Roku). El código sigue las convenciones de SceneGraph para que un
> `zip` + sideload en un Roku real lo ejecute.
