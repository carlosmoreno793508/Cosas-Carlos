"""Ayudante: descubre tu CHAT_ID de Telegram automaticamente.

Corre esto DESPUES de escribirle /start + un mensaje a tu bot en Telegram:

    python -m app.services.telegram_setup

Hace una peticion FRESCA a Telegram (sin cache del navegador) y te imprime el
CHAT_ID exacto que debes poner en .env como TELEGRAM_CHAT_ID.
"""
from __future__ import annotations

import requests

from app.config import settings


def main() -> None:
    token = settings.telegram_bot_token
    if not token:
        print("❌ Falta TELEGRAM_BOT_TOKEN en .env")
        return

    try:
        resp = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=15)
        data = resp.json()
    except Exception as e:
        print(f"❌ No pude contactar a Telegram: {e}")
        return

    if not data.get("ok"):
        print(f"❌ Telegram respondio error: {data}")
        print("   Revisa que el TELEGRAM_BOT_TOKEN sea correcto (sin espacios).")
        return

    chats: dict[int, str] = {}
    for upd in data.get("result", []):
        msg = upd.get("message") or upd.get("edited_message") or {}
        chat = msg.get("chat")
        if chat:
            chats[chat["id"]] = chat.get("first_name") or chat.get("title") or "?"

    if not chats:
        print("⚠️  No encontre ningun mensaje reciente.")
        print("   1) Abre TU bot en Telegram (Kai Copilot).")
        print("   2) Mandale un mensaje nuevo, ej. 'hola'.")
        print("   3) Vuelve a correr:  python3 -m app.services.telegram_setup")
        return

    print("✅ Encontrado(s):\n")
    for cid, name in chats.items():
        print(f"   TELEGRAM_CHAT_ID={cid}     (chat: {name})")
    print("\n👉 Copia esa linea COMPLETA en tu archivo .env (reemplaza la que ya tienes).")
    print("   Luego corre:  python3 -m app.services.bot")


if __name__ == "__main__":
    main()
