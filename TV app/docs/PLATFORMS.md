# Guía por plataforma

Cada plataforma de TV tiene su propio SDK y forma de instalar apps. La estrategia
es maximizar la reutilización del núcleo (`@tvapp/core`) y compartir la mayor
cantidad de UI posible.

## Resumen de decisión

| Plataforma           | SDK / Lenguaje              | Reutiliza núcleo | Tienda / distribución                        |
| -------------------- | --------------------------- | ---------------- | -------------------------------------------- |
| Navegador / Web      | React + hls.js              | Directo          | URL / PWA                                    |
| Samsung Smart TV     | **Tizen** (web app, WGT)    | Directo          | Samsung Apps / sideload con Tizen Studio     |
| LG Smart TV          | **webOS** (web app, IPK)    | Directo          | LG Content Store / sideload con webOS CLI    |
| Amazon **Fire TV**   | Android TV (Kotlin) o RN-TV | Vía núcleo (JS)  | Amazon Appstore (APK)                        |
| Android TV / Google TV | Android TV (Kotlin) o RN-TV | Vía núcleo (JS) | Google Play                                  |
| **Apple TV**         | tvOS (Swift) o RN-tvOS      | Vía núcleo (JS)  | App Store                                    |
| **Roku**             | BrightScript + SceneGraph   | Reimplementa     | Roku Channel Store / sideload developer mode |

## 1. Web / Samsung Tizen / LG webOS (ya implementado)

`apps/web` es una app React que corre en navegador y, empaquetada, en Samsung y
LG. Ambos sistemas operativos de TV son básicamente un WebView: la misma app web
se empaqueta en un contenedor.

- **Samsung Tizen**: instalar [Tizen Studio](https://developer.tizen.org/), crear
  un proyecto "TV Web app", copiar el `dist/` de `apps/web` y generar el `.wgt`.
  Para pruebas, activar *Developer Mode* en el TV y hacer sideload con
  `tizen install`.
- **LG webOS**: instalar
  [webOS CLI (ares)](https://webostv.developer.lge.com/), envolver el `dist/` con
  un `appinfo.json`, empaquetar con `ares-package` y desplegar con `ares-install`.

El control remoto ya está soportado en `apps/web/src/remote.ts` (mapea flechas,
OK y las teclas "Atrás" de Tizen `10009`/`461` y webOS `461`/`427`).

## 2. Fire TV / Android TV / Google TV

Fire TV es Android TV con la tienda de Amazon. Dos caminos:

- **React Native for TV** (`react-native-tvos`): reutiliza `@tvapp/core` tal cual
  (es TS puro) y comparte gran parte de la UI con Apple TV. Recomendado si
  queremos un solo código para Android TV + Apple TV.
- **Nativo Kotlin + Leanback/Compose for TV**: máximo rendimiento y mejor
  integración; el núcleo se consume vía un puente JS o se reimplementa el parser
  (es pequeño). Reproductor: **ExoPlayer/Media3** (HLS/DASH nativo).

Distribución: generar APK y subir a **Amazon Appstore** (Fire TV) y **Google
Play** (Android TV/Google TV). Fire TV también permite sideload por ADB.

## 3. Apple TV (tvOS)

- **React Native tvOS**: comparte código con Fire TV/Android TV y reutiliza
  `@tvapp/core`. Reproductor vía `AVPlayer` (HLS nativo, ideal para Apple).
- **Nativo SwiftUI + AVKit**: mejor experiencia, pero sin reutilización de UI.

Distribución: solo App Store (Apple no permite sideload en tvOS para usuarios
finales). Requiere cuenta de desarrollador de Apple.

## 4. Roku

Roku es el caso especial: **no** ejecuta JavaScript de apps. Usa **BrightScript**
con el framework **SceneGraph** (XML + BrightScript). Aquí no se reutiliza el
núcleo JS; se reimplementa la lógica (el parser M3U y el cliente Xtream son
pequeños y directos de portar). Reproductor: nodo `Video` de SceneGraph, que
soporta HLS/DASH.

Distribución: *Roku Developer Mode* para sideload durante desarrollo; publicación
en el **Roku Channel Store**.

## Recomendación de fases

1. **Fase 1 (hecha):** núcleo + app web → cubre navegador, Samsung y LG con un
   solo código.
2. **Fase 2:** React Native TV → cubre Fire TV, Android TV/Google TV y Apple TV
   reutilizando `@tvapp/core`.
3. **Fase 3:** Roku en BrightScript (puerto de la lógica del núcleo).
