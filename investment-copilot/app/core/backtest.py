"""Backtest — el evaluador de la Etapa 1.

Corre la estrategia sobre toda la historia de un activo y responde la pregunta
clave: **¿esto funciona?** Y, mas importante, **¿le gana a solo comprar y
aguantar (buy & hold)?**

Estrategia v2 (trend following):
  * ENTRA cuando la tendencia es alcista (precio > MA200) y el riesgo no esta
    en zona roja.
  * NO usa objetivo fijo (eso cortaba a los ganadores). En su lugar usa un
    TRAILING STOP: el stop sube solo mientras el precio sube, dejando correr
    la ganancia, y te saca cuando el precio retrocede N*ATR desde su maximo.
  * Tambien sale si la tendencia se voltea bajista (close < MA200).

Metricas:
  * return_pct    : rendimiento de la estrategia
  * buy_hold_pct  : rendimiento de solo comprar el primer dia y aguantar
  * max_drawdown  : peor caida pico-a-valle de la cartera
  * trades / win  : numero de operaciones y % ganadoras
"""
from __future__ import annotations

import os

import pandas as pd

from app.config import stop_mult
from app.core.opportunity_engine import MAX_RISK_SCORE, RISK_PER_TRADE
from app.core.paper_engine import COMMISSION, SLIPPAGE, PaperBroker
from app.core.risk_engine import RiskEngine

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")


def backtest_symbol(symbol: str, df: pd.DataFrame, capital: float = 10_000.0) -> dict:
    """Simula la estrategia dia por dia sobre `df` (un solo activo)."""
    ind = RiskEngine.calculate_indicators(df).dropna(subset=["ma200", "atr"])
    if ind.empty:
        return {"symbol": symbol, "error": "historia insuficiente"}

    broker = PaperBroker(cash=capital)
    mult = stop_mult(symbol)
    peak_equity = capital
    max_dd = 0.0
    peak_price = 0.0  # maximo precio desde que se abrio la posicion (para el trailing)

    for when, row in ind.iterrows():
        price = float(row["close"])
        high, low, atr = float(row["high"]), float(row["low"]), float(row["atr"])
        day = when.date().isoformat()
        pos = broker.positions.get(symbol)

        if pos is not None:
            # Trailing stop: el stop solo sube, nunca baja.
            peak_price = max(peak_price, high)
            trail = peak_price - mult * atr
            pos.stop = max(pos.stop, trail)

            if low <= pos.stop:
                broker.sell(symbol, pos.stop, day, "trailing_stop")
            elif price < float(row["ma200"]):
                broker.sell(symbol, price, day, "trend_flip")
        else:
            bullish = price > float(row["ma200"])
            if bullish and float(row["total_risk"]) <= MAX_RISK_SCORE and atr > 0:
                stop = price - mult * atr
                risk_per_unit = price - stop
                if risk_per_unit > 0:
                    size = (broker.equity({symbol: price}) * RISK_PER_TRADE) / risk_per_unit
                    broker.buy(symbol, price, size, stop, stop, day)  # target no se usa (trailing)
                    peak_price = price

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
    from app.config import all_symbols, settings

    print("\n📈 BACKTEST v2 — estrategia vs comprar-y-aguantar")
    print(f"   (slippage {SLIPPAGE:.1%} + comision {COMMISSION:.1%} por lado)")
    print("=" * 70)
    print(f"   {'activo':<12} {'estrategia':>11} {'buy&hold':>11} {'maxDD':>9} {'trades':>7} {'win':>7}")
    print("-" * 70)
    for r in run_backtests(all_symbols(settings.quote_currency)):
        if r.get("error"):
            print(f"🔹 {r['symbol']:<12} {r['error']}")
            continue
        beat = "✅" if r["return_pct"] > r["buy_hold_pct"] else "  "
        print(
            f"{beat} {r['symbol']:<12} {r['return_pct']:>9.2f}%  {r['buy_hold_pct']:>9.2f}%  "
            f"{r['max_drawdown_pct']:>7.2f}%  {r['trades_closed']:>6}  {r['win_rate_pct']:>5.1f}%"
        )
    print("=" * 70)
    print("✅ = la estrategia le gano a solo comprar y aguantar")
