#!/usr/bin/env bash
# tid_diario.sh — Corrida diaria de TID-MAX: sincroniza WHOOP, arma el reporte
# del coach + la tarjeta, y ENVÍA el mensaje con el link (iMessage/Telegram/correo).
# Pensado para lanzarse por launchd a las horas que quieras (mañana, tarde, 10pm).
#
# Config de variables: crea ~/.tid_env con tus exports (ver .tid_env.example).
# Log de cada corrida: publico/tid_diario.log
set -uo pipefail
# launchd usa un PATH mínimo: agregamos Homebrew para hallar cloudflared/python3.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# 1) Variables de entorno (TID_IMESSAGE_TO, correo, etc.).
[ -f "$HOME/.tid_env" ] && source "$HOME/.tid_env"

# 2) Python: usa el venv si existe; si no, python3 del sistema.
if [ -n "${TID_PYTHON:-}" ] && [ -x "${TID_PYTHON}" ]; then
  PY="$TID_PYTHON"
elif [ -f "$DIR/.venv/bin/python3" ]; then
  PY="$DIR/.venv/bin/python3"
elif [ -f "$HOME/Cosas-Carlos/.venv/bin/python3" ]; then
  PY="$HOME/Cosas-Carlos/.venv/bin/python3"
else
  PY="$(command -v python3)"
fi

mkdir -p "$DIR/publico"
LOG="$DIR/publico/tid_diario.log"
{
  echo "===================== $(date '+%Y-%m-%d %H:%M:%S') ====================="
  echo "Python: $PY"
  "$PY" whoop_sync.py   || echo "(whoop_sync falló u omitido — sigo con datos existentes)"
  "$PY" tid_data.py     || { echo "tid_data.py falló"; exit 1; }
  "$PY" tid_agent.py    || { echo "tid_agent.py falló"; exit 1; }
  "$PY" tid_cliente.py --solo-html || echo "(tid_cliente.py falló — reviso)"
  "$PY" tid_notify.py
  echo "----- fin de corrida -----"
} >> "$LOG" 2>&1
