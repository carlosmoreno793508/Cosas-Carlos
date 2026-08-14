#!/usr/bin/env bash
# Genera los proyectos nativos (android/ e ios/) de la app RN de TV usando la
# plantilla de react-native-tvos. Se corre UNA sola vez, en tu máquina (necesita
# Android Studio/Xcode). Copia el código JS/TS existente sobre la plantilla.
set -euo pipefail

APP_NAME="MoreTV"
HERE="$(cd "$(dirname "$0")/.." && pwd)"   # apps/tv
TMP="$(mktemp -d)"

echo "→ Generando plantilla react-native-tvos en $TMP …"
cd "$TMP"
npx @react-native-community/cli@latest init "$APP_NAME" \
    --template=react-native-tvos --skip-install

echo "→ Copiando proyectos nativos a apps/tv …"
cp -r "$TMP/$APP_NAME/android" "$HERE/android"
cp -r "$TMP/$APP_NAME/ios" "$HERE/ios"

echo "→ Listo. Ahora, desde apps/tv:"
echo "   npm install --legacy-peer-deps"
echo "   npm run android     # compila e instala en Fire TV/Android TV por ADB"
rm -rf "$TMP"
