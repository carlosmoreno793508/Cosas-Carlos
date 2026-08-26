"""Servicio de alertas por Telegram (Dia 5).

Reemplaza a WhatsApp/Twilio para el MVP: gratis, inmediato y con Markdown.
El bot solo habla con TELEGRAM_CHAT_ID (tu). Cualquier otro chat se ignora.
"""
from __future__ import annotations

import requests

from app.config import settings


class TelegramBot:
    def __init__(self):
        self.token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, message: str) -> bool:
        if not self.token or not self.chat_id:
            print("❌ Faltan TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID en .env")
            return False
        try:
            resp = requests.post(
                f"{self.base_url}/sendMessage",
                json={"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"},
                timeout=15,
            )
            if resp.status_code == 200:
                print("✅ Alerta enviada a Telegram.")
                return True
            print(f"❌ Error Telegram: {resp.text}")
            return False
        except Exception as e:
            print(f"❌ Fallo de conexion: {e}")
            return False

    @staticmethod
    def format_report(reports: list[dict]) -> str:
        line = "⎯" * 15
        msg = f"📊 *REPORTE DE MERCADO (MVP)*\n{line}\n\n"
        for item in reports:
            stale = "  ⏳_datos rancios_" if item.get("is_stale") else ""
            msg += f"*{item['symbol']}* | ${item['price']:,.2f}\n"
            msg += f"{item['level']}  Score: *{item['risk_score']}/100*{stale}\n"
            d = item["details"]
            msg += f"📉 DD: {d['drawdown_pct']}%  |  🌊 Vol: {d['atr_pct']}%\n\n"
        msg += f"{line}\n💡 Detalle en el dashboard."
        return msg


if __name__ == "__main__":
    TelegramBot().send_message("👋 *Investment Copilot* conectado. El riesgo manda.")
