#!/bin/bash
# Corre un ciclo del bot usando el Python del venv.
# Pensado para el piloto automatico (launchd) en Mac.
cd "$(dirname "$0")" || exit 1
mkdir -p data_storage
./venv/bin/python -m app.services.bot >> data_storage/bot.log 2>&1
