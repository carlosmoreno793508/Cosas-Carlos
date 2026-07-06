"""El Bot — corre la estrategia hacia adelante y opera (en paper).

Un ciclo del bot:
  1. Respeta el Kill Switch (si esta activo, no hace nada).
  2. Actualiza datos de los activos activos (BTC/ETH/XRP).
  3. Para cada activo: calcula indicadores, revisa datos rancios, y decide con
     app/core/strategy.py (la MISMA logica que el backtest valido).
  4. Ejecuta la orden en PAPER (dinero simulado), recordando el estado en disco.
  5. Registra cada decision y te manda un resumen por Telegram.

Mismo codigo servira para real: solo se cambia el PaperBroker por un broker real
cuando el forward-test en paper te convenza. Hasta entonces: dinero simulado.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from app.config import active_symbols, settings
from app.core import strategy
from app.core.paper_engine import PaperBroker
from app.core.risk_engine import STALE_DAYS, RiskEngine
from app.services.alert_service import TelegramBot

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")
STATE_FILE = os.path.join(DATA_DIR, "bot_state.json")


def _load_broker() -> PaperBroker:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return PaperBroker.from_dict(json.load(f))
    return PaperBroker(cash=settings.paper_capital)


def _save_broker(broker: PaperBroker) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(broker.to_dict(), f, indent=2)


def run_bot_cycle(update_data: bool = True, notify: bool = True) -> dict:
    """Ejecuta un ciclo. Devuelve un resumen con las acciones tomadas."""
    if settings.kill_switch:
        print("🛑 Kill Switch ACTIVO: el bot no opera.")
        return {"kill_switch": True, "actions": []}

    if update_data:
        from app.services.market_data import run_ingestion
        run_ingestion(active_symbols(settings.quote_currency))

    engine = RiskEngine()
    broker = _load_broker()
    symbols = active_symbols(settings.quote_currency)
    actions: list[str] = []
    prices: dict[str, float] = {}
    rows: dict[str, object] = {}

    # 1er paso: reunir el ultimo dato de cada activo.
    for symbol in symbols:
        df = engine.load_data(symbol)
        if df is None:
            continue
        ind = engine.calculate_indicators(df).dropna(subset=["ma200"])
        if ind.empty:
            continue
        row = ind.iloc[-1]
        rows[symbol] = row
        prices[symbol] = float(row["close"])

    # Reparto equitativo con dial de exposicion: cada activo apunta a
    # max_exposure/N del capital total (el resto queda en efectivo).
    total_equity = broker.equity(prices)
    target_per_asset = total_equity * settings.max_exposure / max(len(symbols), 1)
    day = None

    # 2do paso: decidir y ejecutar.
    for symbol in symbols:
        row = rows.get(symbol)
        if row is None:
            continue
        price, ma200 = float(row["close"]), float(row["ma200"])
        pos = broker.positions.get(symbol)
        day = row.name.date().isoformat()

        age_days = (datetime.now(timezone.utc) - row.name.to_pydatetime()).days
        if age_days > STALE_DAYS and pos is None:
            actions.append(f"⏳ {symbol}: datos rancios ({age_days}d), no se abre.")
            continue

        if pos is not None:
            pos.peak = max(pos.peak, price)

        action = strategy.decide(
            price=price, ma200=ma200, total_risk=float(row["total_risk"]),
            holding=pos is not None, peak_price=pos.peak if pos else 0.0,
        )

        if action in (strategy.EXIT_TREND, strategy.EXIT_PROTECT):
            broker.sell(symbol, price, day, action.lower())
            actions.append(f"🔴 VENTA {symbol} @ ${price:,.4f} ({action})")
        elif action == strategy.ENTER:
            notional = min(target_per_asset, broker.cash * 0.99)  # 1/N del capital, sin sobregiro
            size = notional / price
            if size > 0 and broker.buy(symbol, price, size, ma200, price, day):
                actions.append(f"🟢 COMPRA {symbol} @ ${price:,.4f} (~${notional:,.0f})")
        # HOLD / FLAT: sin accion

    _save_broker(broker)
    stats = broker.stats(prices)
    summary = {"date": day if prices else None, "actions": actions, "stats": stats}

    if notify:
        _notify(actions, stats)
    print(f"🤖 Ciclo bot: {len(actions)} accion(es). Equity ${stats['equity']:,.2f} "
          f"({stats['return_pct']:+.2f}%)")
    return summary


def _notify(actions: list[str], stats: dict) -> None:
    line = "⎯" * 15
    msg = f"🤖 *BOT (paper)*\n{line}\n"
    msg += "\n".join(actions) if actions else "Sin operaciones nuevas."
    msg += f"\n{line}\n💼 Equity: *${stats['equity']:,.2f}* ({stats['return_pct']:+.2f}%)\n"
    msg += f"Posiciones abiertas: {stats['open_positions']}  |  Operaciones: {stats['trades_closed']}"
    TelegramBot().send_message(msg)


if __name__ == "__main__":
    run_bot_cycle()
