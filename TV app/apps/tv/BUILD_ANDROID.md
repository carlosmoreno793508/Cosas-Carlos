# Generar el APK para Fire TV / Android TV / Google TV

La app RN (`apps/tv`) trae el código JS/TS listo. Para producir un **APK** hay
que generar una vez los proyectos nativos (`android/`) —que dependen de tu
máquina y no se versionan— y luego compilar.

## Requisitos

- Node 22+, JDK 17.
- **Android Studio** + Android SDK (API 34), con `ANDROID_HOME` configurado.
- Un **Fire TV** o **Android TV** en modo desarrollador (o un emulador de TV).

## 1) Generar los proyectos nativos (una sola vez)

```bash
cd "TV app/apps/tv"
bash scripts/init-native.sh      # crea android/ e ios/ desde la plantilla tvOS
npm install --legacy-peer-deps
```

> El nombre del módulo registrado debe ser **MoreTV** (coincide con `app.json`).

## 2) Compilar e instalar por ADB (uso personal)

Fire TV y Android TV aceptan sideload directo por ADB — ideal para uso personal:

```bash
# Empareja el dispositivo (una vez): en el TV activa "Depuración por ADB"
adb connect <IP-DEL-TV>:5555

cd "TV app/apps/tv"
npm run android                  # compila el APK debug y lo instala en el TV
```

## 3) APK/AAB de release (para distribuir)

```bash
cd "TV app/apps/tv/android"
# Genera una clave de firma (una vez)
keytool -genkeypair -v -keystore moretv.keystore -alias moretv \
        -keyalg RSA -keysize 2048 -validity 10000

# Compila
./gradlew assembleRelease      # -> app/build/outputs/apk/release/app-release.apk
./gradlew bundleRelease        # -> .aab para Google Play
```

Configura la firma en `android/app/build.gradle` (`signingConfigs`) apuntando a
`moretv.keystore`.

## 4) Publicar

- **Fire TV** → Amazon Appstore (sube el APK) o sideload por ADB para ti.
- **Android TV / Google TV** → Google Play Console (sube el `.aab`).

Marca el APK como app de TV en el `AndroidManifest.xml`:

```xml
<uses-feature android:name="android.software.leanback" android:required="true" />
<uses-feature android:name="android.hardware.touchscreen" android:required="false" />
<!-- En el <activity> principal: -->
<category android:name="android.intent.category.LEANBACK_LAUNCHER" />
```

(La plantilla de react-native-tvos ya incluye la configuración Leanback.)

## CI (opcional)

`.github/workflows/build-android.yml` compila el APK automáticamente **cuando el
directorio `apps/tv/android/` existe** (es decir, después del paso 1 y de
commitearlo, si decides versionar los proyectos nativos).
