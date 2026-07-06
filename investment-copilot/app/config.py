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

# Acciones / ETFs. Modelo hibrido de Carlos: la cripto la EJECUTA el sistema
# (paper/live), pero la bolsa es solo ADVISORY (el sistema avisa, tu ejecutas
# en IBKR). Ver execution_mode() abajo.
EQUITIES: list[str] = ["SPY", "QQQ"]

# ACTIVOS ACTIVOS: los que el bot realmente opera. El backtest mostro que la
# estrategia funciona en los grandes y falla en los alt chicos (ilic­uidos),
# asi que el bot se enfoca aqui. El resto del UNIVERSE queda solo en observacion.
ACTIVE_BASES: list[str] = ["BTC", "ETH", "XRP"]


def active_symbols(quote: str = "USDT") -> list[str]:
    """Pares que el bot opera de verdad, ej. ['BTC/USDT', 'ETH/USDT', 'XRP/USDT']."""
    return [f"{b}/{quote}" for b in ACTIVE_BASES]

# Multiplicador de ATR para el stop, por grupo (runbook: core holgado, utility
# estricto). Las acciones usan un stop holgado por defecto.
STOP_MULT: dict[str, float] = {
    "core": 2.0,
    "infra": 1.5,
    "utility": 1.0,
    "equity": 2.0,
    "unknown": 2.0,
}


def all_symbols(quote: str = "USDT") -> list[str]:
    """Devuelve la lista plana de pares cripto, ej. ['BTC/USDT', ...]."""
    out: list[str] = []
    for coins in UNIVERSE.values():
        out.extend(f"{c}/{quote}" for c in coins)
    return out


def group_of(symbol: str) -> str:
    """Regresa el grupo ('core'/'infra'/'utility'/'equity') de un simbolo."""
    if asset_class(symbol) == "equity":
        return "equity"
    base = symbol.split("/")[0]
    for grp, coins in UNIVERSE.items():
        if base in coins:
            return grp
    return "unknown"


def asset_class(symbol: str) -> str:
    """'crypto' si es un par (BTC/USDT); 'equity' si es un ticker suelto (SPY)."""
    return "crypto" if "/" in symbol else "equity"


def execution_mode(symbol: str) -> str:
    """Modo hibrido: cripto -> 'paper' (ejecuta simulado); bolsa -> 'advisory'."""
    return "paper" if asset_class(symbol) == "crypto" else "advisory"


def stop_mult(symbol: str) -> float:
    return STOP_MULT.get(group_of(symbol), 2.0)


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
    paper_capital: float = 10_000.0  # capital simulado inicial del bot

    # Dial de riesgo: fraccion MAXIMA del capital que puede estar invertida.
    # 1.0 = 100% invertido (mas retorno, mas drawdown).
    # 0.6 = deja 40% en efectivo siempre (menos retorno, menos drawdown).
    max_exposure: float = 1.0

    @property
    def exchange_list(self) -> list[str]:
        return [x.strip() for x in self.exchange_ids.split(",") if x.strip()]


settings = Settings()
