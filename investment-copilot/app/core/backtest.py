"""Backtest — el evaluador de la Etapa 1.

Corre la estrategia sobre toda la historia y responde: **¿le gana a solo
comprar y aguantar (buy & hold)?**

Estrategia v3 (filtro de regimen — "time in the market"):
  Las versiones con micro-stops (objetivo fijo 2:1, trailing) picaban la
  posicion a muerte en cada bajada normal: muchas operaciones, muchos costos,
  y se perdian la tendencia grande. v3 hace lo contrario, simple y aburrido:

    * DENTRO mientras el precio > MA200 (regimen alcista).
    * FUERA cuando el precio cierra por debajo de la MA200 (rompe tendencia).
    * Sin objetivo, sin trailing. Pocas operaciones, deja correr la tendencia
      y esquiva los grandes desplomes.

  El Risk Score se sigue calculando (alimenta alertas y niveles de autonomia),
  pero solo bloquea ENTRAR si esta en zona roja; no fuerza salidas (eso churneaba).

Metricas: return_pct vs buy_hold_pct, max_drawdown, trades, win_rate.
"""
from __future__ import annotations

import os

import pandas as pd

from app.core.opportunity_engine import MAX_RISK_SCORE
from app.core.paper_engine import COMMISSION, SLIPPAGE, PaperBroker
from app.core.risk_engine import RiskEngine

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")

INVEST_FRACTION = 0.98  # fraccion del capital que se pone al activo mientras esta dentro


def backtest_symbol(symbol: str, df: pd.DataFrame, capital: float = 10_000.0) -> dict:
    """Simula la estrategia de regimen dia por dia sobre `df`."""
    ind = RiskEngine.calculate_indicators(df).dropna(subset=["ma200"])
    if ind.empty:
        return {"symbol": symbol, "error": "historia insuficiente"}

    broker = PaperBroker(cash=capital)
    peak_equity = capital
    max_dd = 0.0

    for when, row in ind.iterrows():
        price = float(row["close"])
        ma200 = float(row["ma200"])
        day = when.date().isoformat()
        pos = broker.positions.get(symbol)

        if pos is not None:
            if price < ma200:                       # rompe tendencia -> fuera
                broker.sell(symbol, price, day, "trend_break")
        else:
            entrable = price > ma200 and float(row["total_risk"]) <= MAX_RISK_SCORE
            if entrable:
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
    from app.config import all_symbols, settings

    print("\n📈 BACKTEST v3 — filtro de regimen (MA200) vs comprar-y-aguantar")
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
    print("✅ = la estrategia le gano al buy & hold  |  clave: menos maxDD con parte del upside")
