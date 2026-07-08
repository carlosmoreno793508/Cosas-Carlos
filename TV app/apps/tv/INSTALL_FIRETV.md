# Instalar MoreTV en Fire TV / Android TV (APK compilado en la nube)

No necesitas Android Studio. GitHub compila el APK por ti; tú lo descargas e
instalas en el TV.

## 1. Descargar el APK

1. Entra a tu repo en GitHub → pestaña **Actions**.
2. Abre el último run de **build-android** que tenga ✓ verde.
3. Abajo, en **Artifacts**, descarga **MoreTV-FireTV-AndroidTV-apk** (es un .zip).
4. Descomprímelo → obtienes `app-release.apk`.

## 2. Activar el modo desarrollador en el Fire TV

1. **Ajustes → Mi Fire TV → Acerca de** → pulsa 7 veces sobre el nombre del
   dispositivo (activa opciones de desarrollador).
2. **Ajustes → Mi Fire TV → Opciones de desarrollador** → activa
   **Depuración por ADB** y **Apps de fuentes desconocidas**.
3. Anota la **IP** del Fire TV (Ajustes → Mi Fire TV → Acerca de → Red).

## 3. Instalar por ADB desde tu Mac

Necesitas ADB una vez (`brew install android-platform-tools`, o viene con Android
Studio). Luego, en la Terminal:

```bash
adb connect <IP-DEL-FIRETV>:5555      # acepta el aviso que sale en el TV
adb install -r ~/Downloads/app-release.apk
```

Aparecerá **MoreTV** en tus apps del Fire TV.

> Alternativa sin Mac: sube el `app-release.apk` a tu Google Drive/Dropbox y en el
> Fire TV usa la app **Downloader** (con el enlace directo) para instalarlo.

## 4. Usarla

Abre MoreTV en el Fire TV, **➕ Añadir lista** y pon tu M3U/Xtream. En el TV **no
hay límite de CORS**, así que reproduce tu lista directamente (sin proxy).

> Usa fuentes para las que tengas derechos (proveedor con licencia, TV abierta,
> FAST). Ver `../../docs/LEGAL.md`.
