#!/usr/bin/env bash
# tid_publicar.sh — Publica la tarjeta del día (publico/index.html) en un link
# PÚBLICO con Cloudflare Tunnel, igual que el Plan Financiero de Karla.
# Cualquiera abre el link con un clic, SIN cuenta de nada.
#
# Uso:
#   ./tid_publicar.sh          # sirve + abre el túnel; DEJA esta terminal abierta
#
# Deja este proceso corriendo (mientras viva, el link funciona). La URL queda
# guardada en publico/url.txt, y tid_notify.py la toma sola para el mensaje diario.
#
# Requisitos: cloudflared instalado (brew install cloudflared) y python3.
set -euo pipefail
# launchd corre con un PATH mínimo: agregamos las rutas de Homebrew para que
# encuentre cloudflared (y python3) igual que en tu terminal.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
DIR="$(cd "$(dirname "$0")" && pwd)"
PUB="$DIR/publico"
PORT="${TID_PORT:-8787}"
mkdir -p "$PUB"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "❌ No encuentro 'cloudflared'. Instálalo con:  brew install cloudflared"
  exit 1
fi
if [ ! -f "$PUB/index.html" ]; then
  echo "⚠️  Aún no existe $PUB/index.html — corre primero:  python3 tid_cliente.py"
fi

# Servidor local que sirve SOLO la carpeta publico/ (no expone el resto del repo).
python3 -m http.server "$PORT" --directory "$PUB" >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
echo "🌐 Sirviendo $PUB en http://localhost:$PORT"
echo "🚇 Abriendo túnel de Cloudflare… (deja esta terminal abierta)"
echo

# cloudflared imprime la URL https://...trycloudflare.com; la capturamos y guardamos.
cloudflared tunnel --url "http://localhost:$PORT" 2>&1 | while IFS= read -r line; do
  echo "$line"
  if [[ "$line" =~ (https://[a-zA-Z0-9.-]+\.trycloudflare\.com) ]]; then
    URL="${BASH_REMATCH[1]}"
    echo "$URL" > "$PUB/url.txt"
    echo
    echo "✅ LINK PÚBLICO (para Karla):  $URL"
    echo "   (guardado en publico/url.txt — tid_notify.py lo usa automáticamente)"
    echo
  fi
done
