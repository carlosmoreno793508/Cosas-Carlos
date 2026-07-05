"""Backtest — el evaluador de la Etapa 1.

Corre la estrategia (motor de oportunidades + paper trading) sobre toda la
historia de un activo y responde la pregunta clave: **¿esto funciona?**

Metricas que devuelve:
  * return_pct   : rendimiento total sobre el capital inicial
  * max_drawdown : peor caida pico-a-valle de la cartera (cuanto te dolio)
  * trades       : cuantas operaciones cerro
  * win_rate_pct : % de operaciones ganadoras

Reglas de salida de una posicion abierta:
  1. Toca el stop      -> vende (perdida controlada)
  2. Toca el objetivo  -> vende (toma ganancia)
  3. Tendencia se voltea bajista (close < MA200) -> vende (cambio de regimen)
"""
from __future__ import annotations

import os

import pandas as pd

from app.config import stop_mult
from app.core.opportunity_engine import MAX_RISK_SCORE, RISK_PER_TRADE, RR_TARGET
from app.core.paper_engine import COMMISSION, SLIPPAGE, PaperBroker
from app.core.risk_engine import RiskEngine

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")


def backtest_symbol(symbol: str, df: pd.DataFrame, capital: float = 10_000.0) -> dict:
    """Simula la estrategia dia por dia sobre `df` (un solo activo)."""
    ind = RiskEngine.calculate_indicators(df).dropna(subset=["ma200", "atr"])
    if ind.empty:
        return {"symbol": symbol, "error": "historia insuficiente"}

    broker = PaperBroker(cash=capital)
    peak = capital
    max_dd = 0.0

    for when, row in ind.iterrows():
        price = float(row["close"])
        day = when.date().isoformat()
        pos = broker.positions.get(symbol)

        if pos is not None:
            low, high = float(row["low"]), float(row["high"])
            if low <= pos.stop:
                broker.sell(symbol, pos.stop, day, "stop")
            elif high >= pos.target:
                broker.sell(symbol, pos.target, day, "target")
            elif price < float(row["ma200"]):
                broker.sell(symbol, price, day, "trend_flip")
        else:
            # Mismo filtro que el motor de oportunidades.
            atr = float(row["atr"])
            bullish = price > float(row["ma200"])
            if bullish and float(row["total_risk"]) <= MAX_RISK_SCORE and atr > 0:
                stop = price - stop_mult(symbol) * atr
                risk_per_unit = price - stop
                if risk_per_unit > 0:
                    size = (broker.equity({symbol: price}) * RISK_PER_TRADE) / risk_per_unit
                    target = price + RR_TARGET * risk_per_unit
                    broker.buy(symbol, price, size, stop, target, day)

        eq = broker.equity({symbol: price})
        peak = max(peak, eq)
        max_dd = min(max_dd, eq / peak - 1)

    last_price = float(ind.iloc[-1]["close"])
    stats = broker.stats({symbol: last_price})
    stats.update({"symbol": symbol, "max_drawdown_pct": round(max_dd * 100, 2)})
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

    print("\n📈 BACKTEST — ¿la estrategia funciona?")
    print(f"   (slippage {SLIPPAGE:.1%} + comision {COMMISSION:.1%} por lado)")
    print("=" * 55)
    for r in run_backtests(all_symbols(settings.quote_currency)):
        if r.get("error"):
            print(f"🔹 {r['symbol']}: {r['error']}")
            continue
        print(
            f"🔹 {r['symbol']:<12} ret {r['return_pct']:>7.2f}%  "
            f"maxDD {r['max_drawdown_pct']:>7.2f}%  "
            f"trades {r['trades_closed']:>3}  win {r['win_rate_pct']:>5.1f}%"
        )
    print("=" * 55)
