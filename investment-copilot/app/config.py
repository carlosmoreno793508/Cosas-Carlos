"""Configuracion central del sistema.

Toda la app lee sus parametros desde aqui (un solo lugar), en vez de tener
constantes regadas por cada script. Los valores se cargan desde variables de
entorno / .env con valores por defecto seguros.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


# Universo cripto definido por Carlos, clasificado por grupo de riesgo.
# El grupo determina allocation maxima y agresividad del stop (ver runbook.md).
UNIVERSE: dict[str, list[str]] = {
    "core": ["BTC", "ETH"],
    "infra": ["SOL", "XRP", "HBAR"],
    "utility": ["XLM", "ALGO", "IOTA", "XDC"],
}


def all_symbols(quote: str = "USDT") -> list[str]:
    """Devuelve la lista plana de pares, ej. ['BTC/USDT', 'ETH/USDT', ...]."""
    out: list[str] = []
    for coins in UNIVERSE.values():
        out.extend(f"{c}/{quote}" for c in coins)
    return out


def group_of(symbol: str) -> str:
    """Regresa el grupo ('core'/'infra'/'utility') de un simbolo dado."""
    base = symbol.split("/")[0]
    for grp, coins in UNIVERSE.items():
        if base in coins:
            return grp
    return "unknown"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Infra
    database_url: str = "postgresql://postgres:securepassword@db:5432/copilot"
    redis_url: str = "redis://redis:6379/0"

    # Mercado
    exchange_ids: str = "binance,kraken,coinbase,kucoin"
    quote_currency: str = "USDT"
    timeframe: str = "1d"
    history_years: int = 3

    # Alertas
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Control
    kill_switch: bool = False

    @property
    def exchange_list(self) -> list[str]:
        return [x.strip() for x in self.exchange_ids.split(",") if x.strip()]


settings = Settings()
