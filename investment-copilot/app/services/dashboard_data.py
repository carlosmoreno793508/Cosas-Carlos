"""Datos para el dashboard (logica pura, sin Streamlit -> testeable).

Lee el estado del bot (posiciones/efectivo simulados), calcula el riesgo del
universo y arma las tablas que la pantalla muestra. No dispara ingesta ni red.
"""
from __future__ import annotations

import json
import os

from app.config import active_symbols, all_symbols, settings
from app.core.paper_engine import PaperBroker
from app.core.risk_engine import RiskEngine
from app.services.bot import STATE_FILE

engine = RiskEngine()


def load_broker() -> PaperBroker:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return PaperBroker.from_dict(json.load(f))
    return PaperBroker(cash=settings.paper_capital)


def latest_prices(symbols: list[str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for s in symbols:
        df = engine.load_data(s)
        if df is not None and not df.empty:
            out[s] = float(df.iloc[-1]["close"])
    return out


def portfolio_snapshot() -> dict:
    broker = load_broker()
    syms = active_symbols(settings.quote_currency)
    prices = latest_prices(syms)
    positions = []
    for s, p in broker.positions.items():
        price = prices.get(s, p.entry_price)
        positions.append(
            {
                "symbol": s,
                "size": p.size,
                "entry": p.entry_price,
                "price": price,
                "pnl": p.unrealized_pnl(price),
                "pnl_pct": (price / p.entry_price - 1) * 100 if p.entry_price else 0.0,
                "opened_at": p.opened_at,
            }
        )
    return {
        "kill_switch": settings.kill_switch,
        "stats": broker.stats(prices),
        "positions": positions,
        "closed": broker.closed,
    }


def risk_table(symbols: list[str]) -> list[dict]:
    rows = []
    for s in symbols:
        r = engine.compute_risk_profile(s)
        if r:
            rows.append(r)
    return rows


def global_risk(rows: list[dict]) -> dict | None:
    if not rows:
        return None
    score = round(sum(r["risk_score"] for r in rows) / len(rows))
    return {"score": score, "level": RiskEngine.autonomy_level(score)}


def price_history(symbol: str, days: int = 365):
    df = engine.load_data(symbol)
    if df is None:
        return None
    ind = RiskEngine.calculate_indicators(df)
    return ind[["close", "ma200"]].tail(days)


def observation_universe() -> list[str]:
    """Monedas del universo que el bot NO opera (solo observacion)."""
    active = set(active_symbols(settings.quote_currency))
    return [s for s in all_symbols(settings.quote_currency) if s not in active]
