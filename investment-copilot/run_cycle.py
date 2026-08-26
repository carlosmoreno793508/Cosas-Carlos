"""Ciclo de ejecucion manual (simula el job diario de las 8:00 AM).

    1. Actualiza datos (opcional con --skip-ingest si ya tienes CSVs frescos)
    2. Calcula riesgo de la cartera
    3. Envia el reporte a Telegram

Uso:
    python run_cycle.py                # ingesta + reporte
    python run_cycle.py --skip-ingest  # solo reporte con datos existentes
"""
from __future__ import annotations

import sys

from app.config import all_symbols, settings
from app.core.risk_engine import RiskEngine
from app.services.alert_service import TelegramBot


def main() -> None:
    skip_ingest = "--skip-ingest" in sys.argv
    print("\n🏁 CICLO DE EJECUCION")

    if not skip_ingest:
        from app.services.market_data import run_ingestion

        run_ingestion()

    engine = RiskEngine()
    reports = [engine.compute_risk_profile(s) for s in all_symbols(settings.quote_currency)]
    reports = [r for r in reports if r]

    if not reports:
        print("⚠️  Sin datos de riesgo. Revisa la ingesta.")
        return

    print("\n🧠 Perfiles calculados:")
    for r in reports:
        print(f"   {r['symbol']}: {r['risk_score']}/100 {r['level']}")

    bot = TelegramBot()
    bot.send_message(bot.format_report(reports))


if __name__ == "__main__":
    main()
