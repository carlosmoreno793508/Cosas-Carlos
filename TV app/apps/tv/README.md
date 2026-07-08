# @tvapp/tv — App React Native para TV (Fire TV · Android TV · Apple TV)

Fase 2 del proyecto. Reutiliza el núcleo `@tvapp/core` (parser M3U + cliente
Xtream) y añade UI nativa de TV con navegación por control remoto y reproductor
de video nativo (ExoPlayer/Media3 en Android/Fire TV, AVPlayer en Apple TV) vía
`react-native-video`.

Está basada en [`react-native-tvos`](https://github.com/react-native-tvos/react-native-tvos),
el fork oficial de React Native con soporte de TV, que cubre **Apple TV** y
**Android TV / Fire TV** desde un mismo código.

## Pantallas

- **Home** — tus listas de reproducción guardadas (AsyncStorage, solo local).
- **Form** — "Nueva lista de reproducción" (M3U o Xtream), igual que en la web.
- **Browse** — categorías + rejilla de canales navegable con el D-pad.
- **Player** — reproducción a pantalla completa.

## Requisitos

- Node 22+, watchman.
- **Fire TV / Android TV:** Android Studio + SDK, un Fire TV/emulador con ADB.
- **Apple TV:** macOS + Xcode con la plataforma tvOS.

> Este scaffold trae el código JS/TS y la config de Metro/Babel. Los proyectos
> nativos (`android/` e `ios/`) se generan una vez con la plantilla de TV (abajo),
> porque son específicos de cada máquina y no se versionan aquí.

## Puesta en marcha

```bash
# 1) Desde la raíz del monorepo, instala dependencias
cd "TV app"
npm install

# 2) Genera los proyectos nativos con la plantilla de react-native-tvos
#    (solo la primera vez), dentro de apps/tv:
cd apps/tv
npx react-native@npm:react-native-tvos init TvApp --template=react-native-tvos --skip-install
#    …y mueve las carpetas android/ e ios/ generadas junto a este package.json.
```

### Fire TV / Android TV

```bash
# Con un Fire TV en modo desarrollador conectado por ADB:
adb connect <IP-del-firetv>:5555
npm run android          # compila e instala el APK
```

Para publicar: genera un APK/AAB de release y súbelo a la **Amazon Appstore**
(Fire TV) o **Google Play** (Android TV/Google TV). Fire TV también acepta
sideload directo del APK por ADB para uso personal.

### Apple TV

```bash
cd ios && pod install && cd ..
npm run tvos             # abre el simulador de Apple TV, o usa Xcode para un equipo real
```

Para uso personal en un Apple TV físico basta con firmar con tu cuenta de
desarrollador de Apple desde Xcode.

## Notas de TV

- El foco se ve con un borde blanco (`focused` en cada pantalla). Fire TV/Android
  y Apple TV mueven el foco automáticamente con el D-pad entre componentes
  `Pressable`.
- El botón **Atrás** (Android/Fire) y **Menu** (Apple TV) se manejan en
  `App.tsx` con `useTVEventHandler`.
- `hasTVPreferredFocus` marca el primer elemento enfocado al entrar a cada pantalla.
