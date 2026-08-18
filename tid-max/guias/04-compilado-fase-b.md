# Guía · Día del compilado (Fase B) — app nativa con FC en vivo + GPS en segundo plano

Checklist para convertir la PWA en **app nativa** (iOS/Android) con las dos
capacidades que el navegador no da: **FC del Polar por Bluetooth** y **GPS que
sigue grabando con la pantalla apagada**. Todo el código ya está cableado; esto es
la parte que se hace **una vez en tu Mac**.

> Tiempo estimado: **1–2 horas**. Necesitas una **Mac con Xcode** y (para iPhone
> real sin límite de 7 días) el **Apple Developer Program ($99 USD/año)**.

---

## 0) Antes de empezar — ten a la mano
- [ ] **Mac** con **Xcode** instalado (App Store) y abierto al menos una vez.
- [ ] **Node.js 18+** y **npm**.
- [ ] **Cuenta Apple Developer** ($99) — o un Apple ID normal para prueba de 7 días.
- [ ] Tu **iPhone** y un **Android** físicos + sus cables.
- [ ] Tu **Polar H10** (o reloj con "broadcast" de FC activado), encendido/húmedo.
- [ ] (Android) **Android Studio** instalado.

---

## 1) Traer el repo y preparar la concha
```bash
git clone https://github.com/carlosmoreno793508/Cosas-Carlos.git
cd Cosas-Carlos/tid-max/native

npm install            # instala Capacitor + plugins (BLE y background-geolocation ya están en package.json)
npm run build          # copia la PWA (app/) a www/
npx cap add ios
npx cap add android
npx cap sync
```

## 2) Terminar el único método pendiente (FC nativa)
En `../app/index.html`, busca el bloque **`RunHR`** (marcado "PUENTE NATIVO"). El
método `_nativeConnect` está como stub. Complétalo con el plugin
`@capacitor-community/bluetooth-le` siguiendo el comentario que ya está ahí:

```
initialize() → requestDevice({services:['heart_rate']}) → connect(deviceId)
→ startNotifications(deviceId, '0000180d-...', '00002a37-...', bytes => onHr(parseHr(new DataView(bytes.buffer))))
```

`parseHr()` ya existe y decodifica los bytes igual que en web. Es el **único** lugar
a tocar; el resto del grabador (splits, mapa, zonas) no cambia. Luego:
```bash
npm run build && npx cap sync
```

## 3) Permisos y "background modes"
Los textos exactos están en `../native/README.md`. Resumen:

**iOS — `ios/App/App/Info.plist`**
- `NSBluetoothAlwaysUsageDescription`, `NSLocationWhenInUseUsageDescription`,
  `NSLocationAlwaysAndWhenInUseUsageDescription`.
- `UIBackgroundModes` → `location` + `bluetooth-central`.
- En Xcode: **Signing & Capabilities** → agrega **Background Modes** (Location updates + Uses BLE accessories). Si usarás Apple Salud: agrega **HealthKit**.

**Android — `android/app/src/main/AndroidManifest.xml`**
- `ACCESS_FINE_LOCATION`, `ACCESS_BACKGROUND_LOCATION`,
  `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_LOCATION`,
  `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`.

## 4) Firmar y correr en tu iPhone
```bash
npx cap open ios          # abre Xcode
```
En Xcode:
- [ ] **Signing & Capabilities** → *Team*: tu cuenta Apple Developer.
- [ ] *Bundle Identifier*: `mx.com.tidmexico.tidmax` (o el que prefieras, único).
- [ ] Conecta el iPhone, selecciónalo como destino y **▶ Run**.
- [ ] La primera vez, en el iPhone: **Ajustes → General → VPN y gestión de dispositivos** → confía en tu perfil de desarrollador.

## 5) Prueba de aceptación (con esto damos Fase B por buena)
- [ ] Abre TID-MAX nativa → **Entrenar → Correr → Iniciar**.
- [ ] Toca **Conectar Polar** → acepta el permiso de Bluetooth → ves **FC + zona en vivo**.
- [ ] **Bloquea la pantalla** y camina 2–3 min → al volver, la **distancia y los splits siguieron** (GPS en segundo plano ✓).
- [ ] **Termina** → aparece el **mapa de la ruta**, splits por km e historial.
- [ ] Si iniciaste sesión, la corrida **sube a tu cuenta** (toast "Corrida subida ✓").

## 6) Android (opcional, mismo día)
```bash
npx cap open android      # abre Android Studio → Run en tu teléfono
```
Acepta permisos de ubicación (incluye "Permitir siempre") y Bluetooth cercano.

## 7) Repartir sin cables (recomendado)
- **iOS → TestFlight**: en Xcode, **Product → Archive → Distribute → TestFlight**.
  Invita a Gael y a ti por correo; instalan desde la app TestFlight.
- **Android → APK/AAB interno** o Play Console (interno).

---

## Notas
- **Íconos/splash**: se generan aparte (`@capacitor/assets`) cuando quieras pulir el look de tienda.
- **La PWA sigue viva**: nada de esto rompe la web; los mismos archivos de `app/`
  corren dentro de la concha. Un cambio en la web = `npm run build && npx cap sync`.
- **WHOOP/Polar por la nube** siguen en paralelo (pipeline diario). Esto suma la FC
  en vivo durante la carrera, que es lo que la nube no puede dar en tiempo real.
