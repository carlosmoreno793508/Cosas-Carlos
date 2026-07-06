"""Backtest — el evaluador de la Etapa 1.

Corre la MISMA estrategia que el bot (app/core/strategy.py) sobre toda la
historia y la compara contra comprar-y-aguantar (buy & hold).

Estrategia: filtro de regimen MA200 + Agente de Proteccion (stop de emergencia
si la posicion cae PROTECTION_DD desde su pico). Ver strategy.py.
"""
from __future__ import annotations

import os

import pandas as pd

from app.core import strategy
from app.core.paper_engine import COMMISSION, SLIPPAGE, PaperBroker
from app.core.risk_engine import RiskEngine

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")

INVEST_FRACTION = 0.98  # fraccion del capital que se pone al activo mientras esta dentro


def backtest_symbol(symbol: str, df: pd.DataFrame, capital: float = 10_000.0) -> dict:
    ind = RiskEngine.calculate_indicators(df).dropna(subset=["ma200"])
    if ind.empty:
        return {"symbol": symbol, "error": "historia insuficiente"}

    broker = PaperBroker(cash=capital)
    peak_equity = capital
    max_dd = 0.0

    for when, row in ind.iterrows():
        price, ma200, high = float(row["close"]), float(row["ma200"]), float(row["high"])
        day = when.date().isoformat()
        pos = broker.positions.get(symbol)

        if pos is not None:
            pos.peak = max(pos.peak, high)  # actualiza el pico para el stop de proteccion

        action = strategy.decide(
            price=price,
            ma200=ma200,
            total_risk=float(row["total_risk"]),
            holding=pos is not None,
            peak_price=pos.peak if pos else 0.0,
        )

        if action in (strategy.EXIT_TREND, strategy.EXIT_PROTECT):
            broker.sell(symbol, price, day, action.lower())
        elif action == strategy.ENTER:
            size = (broker.cash * INVEST_FRACTION) / price
            broker.buy(symbol, price, size, ma200, price, day)

        eq = broker.equity({symbol: price})
        peak_equity = max(peak_equity, eq)
        max_dd = min(max_dd, eq / peak_equity - 1)

    first_close = float(ind.iloc[0]["close"])
    last_close = float(ind.iloc[-1]["close"])
    stats = broker.stats({symbol: last_close})
    stats.update(
        {
            "symbol": symbol,
            "max_drawdown_pct": round(max_dd * 100, 2),
            "buy_hold_pct": round((last_close / first_close - 1) * 100, 2),
        }
    )
    return stats


def run_backtests(symbols: list[str], capital: float = 10_000.0, data_dir: str = DATA_DIR) -> list[dict]:
    engine = RiskEngine(data_dir)
    results = []
    for symbol in symbols:
        df = engine.load_data(symbol)
        if df is None:
            continue
        results.append(backtest_symbol(symbol, df, capital))
    return results


if __name__ == "__main__":
    from app.config import active_symbols, settings

    print("\n📈 BACKTEST — regimen MA200 + stop de proteccion")
    print(f"   activos: {', '.join(active_symbols(settings.quote_currency))}")
    print(f"   (slippage {SLIPPAGE:.1%} + comision {COMMISSION:.1%} por lado)")
    print("=" * 70)
    print(f"   {'activo':<12} {'estrategia':>11} {'buy&hold':>11} {'maxDD':>9} {'trades':>7} {'win':>7}")
    print("-" * 70)
    for r in run_backtests(active_symbols(settings.quote_currency)):
        if r.get("error"):
            print(f"🔹 {r['symbol']:<12} {r['error']}")
            continue
        beat = "✅" if r["return_pct"] > r["buy_hold_pct"] else "  "
        print(
            f"{beat} {r['symbol']:<12} {r['return_pct']:>9.2f}%  {r['buy_hold_pct']:>9.2f}%  "
            f"{r['max_drawdown_pct']:>7.2f}%  {r['trades_closed']:>6}  {r['win_rate_pct']:>5.1f}%"
        )
    print("=" * 70)
    print("✅ = le gano al buy & hold  |  el stop de proteccion recorta el maxDD")
