# TID-MAX · Concha nativa (Capacitor)

Envuelve la **PWA de `tid-max/app`** en una app nativa para iOS y Android, con un
solo objetivo nuevo: **leer el "tanque de salud" del teléfono**.

- **iPhone** → **Apple Salud** (HealthKit)
- **Android** → **Health Connect** (donde **Samsung Health**, Fitbit, Garmin, etc. depositan sus datos)

Tu código web **no se reescribe**: se reutiliza tal cual dentro de la concha nativa.

---

## Cómo está estructurado

```
tid-max/
├─ app/                     ← LA PWA (fuente web, no cambia de casa)
│  ├─ index.html            ← app de 1 archivo · tab "Datos" trae "Salud del teléfono"
│  ├─ health.js             ← PUENTE de salud (Apple Salud / Health Connect / fallback web)
│  ├─ sw.js, manifest…      ← lo que ya la hace PWA
│
└─ native/                  ← ESTA carpeta: la concha nativa (Capacitor)
   ├─ package.json          ← dependencias de Capacitor + scripts
   ├─ capacitor.config.json ← appId, appName, webDir
   ├─ scripts/sync-web.mjs  ← "build": copia app/ → www/ (no hay bundler)
   ├─ www/                  ← (generado) copia de app/ que se empaqueta
   ├─ ios/                  ← (generado con `cap add ios`) proyecto Xcode
   └─ android/              ← (generado con `cap add android`) proyecto Android Studio
```

**La idea clave (dirección de la flecha):** los relojes ya **escriben** en el
tanque del teléfono. TID-MAX solo **lee** ese tanque ya lleno → así con un enchufe
por sistema cubrimos casi cualquier marca, sin integrar una por una.

```
Reloj (Polar/Garmin/Whoop/Samsung/Apple Watch) → escribe → Tanque de Salud → lee → Motor TID-MAX
```

---

## Qué se dejó listo aquí (en el repo)

- ✅ Wrapper de Capacitor configurado (`package.json`, `capacitor.config.json`).
- ✅ "Build" sin bundler (`scripts/sync-web.mjs`) que copia la PWA a `www/`.
- ✅ **Puente de salud** (`../app/health.js`): una sola interfaz para leer salud,
  con **fallback web** (la PWA sigue funcionando en el navegador) y el **adaptador
  del plugin aislado en un solo lugar** para conectarlo fácil.
- ✅ Pantalla **"Salud del teléfono"** en el tab **Datos** (toggle + "Sincronizar
  ahora" + "última sincronización"), igual que Polar Flow.

## Fase B — Grabador de carrera nativo (FC en vivo + GPS en segundo plano)

El grabador de `app/index.html` ya está **cableado a un puente nativo** (bloque
`RunGeo` / `RunHR`, marcado como "PUENTE NATIVO"). En el navegador cae a Web
Bluetooth + `watchPosition` (la PWA no cambia); en la app nativa usará:

- **FC en vivo** → `@capacitor-community/bluetooth-le` (lee el Polar H10 por BLE;
  en iPhone es la ÚNICA vía, porque Safari no da Web Bluetooth).
- **GPS en segundo plano** → `@capacitor-community/background-geolocation`
  (sigue grabando con la pantalla apagada / app en fondo).

Ambos ya están en `package.json`. Falta, en la sesión de compilado:

1. **Terminar el método `RunHR._nativeConnect`** en `app/index.html` con las llamadas
   reales del plugin BLE (el comentario de arriba trae el flujo: `requestDevice` →
   `connect` → `startNotifications('180D','2A37')` → `parseHr`). Es el ÚNICO lugar a tocar.
2. **Declarar los background modes** (abajo).

### iOS — `ios/App/App/Info.plist`
```xml
<key>NSBluetoothAlwaysUsageDescription</key>
<string>TID-MAX se conecta a tu banda Polar para leer tu ritmo cardiaco durante la carrera.</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>TID-MAX usa el GPS para trazar tu ruta y medir distancia y ritmo.</string>
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>TID-MAX sigue registrando tu carrera aunque la pantalla esté apagada.</string>
<key>UIBackgroundModes</key>
<array><string>location</string><string>bluetooth-central</string></array>
```

### Android — `android/app/src/main/AndroidManifest.xml`
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION"/>
<uses-permission android:name="android.permission.BLUETOOTH_SCAN"/>
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT"/>
```

---

## Qué falta hacer en tu Mac (necesita Xcode / Android Studio)

Estos pasos **no** se pueden correr en el entorno del repo (piden los SDK nativos);
se corren en tu Mac una sola vez:

```bash
cd tid-max/native

# 1) Instalar dependencias
npm install

# 2) Instalar el plugin de salud (cubre iOS y Android)
#    Opción recomendada (unificada): capacitor-health
npm install capacitor-health
#    (Alternativa robusta si prefieres: cordova-plugin-health)

# 3) Copiar la web a www/
npm run build

# 4) Agregar las plataformas nativas
npx cap add ios
npx cap add android

# 5) Sincronizar y abrir
npx cap sync
npx cap open ios       # abre Xcode
npx cap open android   # abre Android Studio
```

> ℹ️ En `../app/health.js`, arriba del todo, está el bloque **`ADAPTER`** con los
> nombres de los métodos del plugin. Si eliges un plugin distinto a `capacitor-health`,
> ajústalos ahí (un solo lugar) y el resto de la app no cambia.

---

## Permisos que hay que declarar (una vez)

### iOS — `ios/App/App/Info.plist`
```xml
<key>NSHealthShareUsageDescription</key>
<string>TID-MAX lee tus entrenamientos, frecuencia cardiaca y sueño para calcular tu readiness y tu coach del día.</string>
<key>NSHealthUpdateUsageDescription</key>
<string>TID-MAX puede guardar tus sesiones en Apple Salud.</string>
```
Además, en Xcode: **Signing & Capabilities → + Capability → HealthKit**.

### Android — `android/app/src/main/AndroidManifest.xml`
Permisos de Health Connect (lectura) para los tipos que usamos, p. ej.:
```xml
<uses-permission android:name="android.permission.health.READ_HEART_RATE"/>
<uses-permission android:name="android.permission.health.READ_EXERCISE"/>
<uses-permission android:name="android.permission.health.READ_HEART_RATE_VARIABILITY"/>
<uses-permission android:name="android.permission.health.READ_RESTING_HEART_RATE"/>
<uses-permission android:name="android.permission.health.READ_SLEEP"/>
<uses-permission android:name="android.permission.health.READ_VO2_MAX"/>
```
(La lista exacta la define el plugin; Health Connect viene preinstalado en Android
14+ y como app en Play Store para versiones anteriores.)

---

## Flujo de datos completo

1. Usuario abre **Datos → Salud del teléfono** y toca **Conectar**.
2. iOS/Android muestran la hoja de permisos **por tipo de dato** (FC, entrenos, sueño…).
3. `health.js` lee una **ventana reciente** (14 días por defecto, como Polar Flow).
4. Se normaliza y se pasa al **motor TID-MAX** (zonas, VT1/VT2, FATmax) — intacto.
5. Se guarda la marca de **"última sincronización"** y se puede repetir con
   **"Sincronizar ahora"** o en segundo plano.

Lo de la nube (WHOOP/Strava/Polar por OAuth) **sigue funcionando en paralelo**:
esto solo suma el tanque del teléfono.
