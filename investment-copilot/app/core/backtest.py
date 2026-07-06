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


def backtest_portfolio(
    symbols: list[str],
    capital: float = 10_000.0,
    data_dir: str = DATA_DIR,
    max_exposure: float = 1.0,
) -> dict:
    """Backtest de CARTERA: las N monedas juntas, reparto 1/N (como opera el bot).

    Es la foto honesta de lo que vivirias: al no caer todas a la vez, el
    drawdown de la cartera suele ser menor que el de la peor moneda sola.

    `max_exposure` es el dial de riesgo: fraccion maxima del capital invertida
    (1.0 = todo; 0.6 = deja 40% en efectivo -> menos drawdown y menos retorno).
    """
    engine = RiskEngine(data_dir)
    inds: dict[str, pd.DataFrame] = {}
    for s in symbols:
        df = engine.load_data(s)
        if df is None:
            continue
        ind = RiskEngine.calculate_indicators(df).dropna(subset=["ma200"])
        if not ind.empty:
            inds[s] = ind
    if not inds:
        return {"symbol": "PORTAFOLIO", "error": "sin datos"}

    n = len(inds)
    broker = PaperBroker(cash=capital)
    peak_equity = capital
    max_dd = 0.0
    last_prices: dict[str, float] = {}
    all_dates = sorted(set().union(*[set(ind.index) for ind in inds.values()]))

    for d in all_dates:
        for s, ind in inds.items():
            if d in ind.index:
                last_prices[s] = float(ind.loc[d, "close"])
        target_per_asset = broker.equity(last_prices) * max_exposure / n
        day = d.date().isoformat()

        for s, ind in inds.items():
            if d not in ind.index:
                continue
            row = ind.loc[d]
            price, ma200 = float(row["close"]), float(row["ma200"])
            pos = broker.positions.get(s)
            if pos is not None:
                pos.peak = max(pos.peak, price)
            action = strategy.decide(
                price=price, ma200=ma200, total_risk=float(row["total_risk"]),
                holding=pos is not None, peak_price=pos.peak if pos else 0.0,
            )
            if action in (strategy.EXIT_TREND, strategy.EXIT_PROTECT):
                broker.sell(s, price, day, action.lower())
            elif action == strategy.ENTER:
                notional = min(target_per_asset, broker.cash * 0.99)
                size = notional / price
                if size > 0:
                    broker.buy(s, price, size, ma200, price, day)

        eq = broker.equity(last_prices)
        peak_equity = max(peak_equity, eq)
        max_dd = min(max_dd, eq / peak_equity - 1)

    # Buy & hold de cartera: 1/N en cada moneda el primer dia, aguantar.
    bh_value = sum((capital / n) * (float(ind.iloc[-1]["close"]) / float(ind.iloc[0]["close"]))
                   for ind in inds.values())
    stats = broker.stats(last_prices)
    stats.update(
        {
            "symbol": "PORTAFOLIO",
            "max_drawdown_pct": round(max_dd * 100, 2),
            "buy_hold_pct": round((bh_value / capital - 1) * 100, 2),
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
    syms = active_symbols(settings.quote_currency)
    for r in run_backtests(syms):
        if r.get("error"):
            print(f"🔹 {r['symbol']:<12} {r['error']}")
            continue
        beat = "✅" if r["return_pct"] > r["buy_hold_pct"] else "  "
        print(
            f"{beat} {r['symbol']:<12} {r['return_pct']:>9.2f}%  {r['buy_hold_pct']:>9.2f}%  "
            f"{r['max_drawdown_pct']:>7.2f}%  {r['trades_closed']:>6}  {r['win_rate_pct']:>5.1f}%"
        )

    p = backtest_portfolio(syms, max_exposure=settings.max_exposure)
    if not p.get("error"):
        print("-" * 70)
        beat = "✅" if p["return_pct"] > p["buy_hold_pct"] else "  "
        print(
            f"{beat} {'CARTERA 1/N':<12} {p['return_pct']:>9.2f}%  {p['buy_hold_pct']:>9.2f}%  "
            f"{p['max_drawdown_pct']:>7.2f}%  {p['trades_closed']:>6}  {p['win_rate_pct']:>5.1f}%"
        )
    print("=" * 70)
    print("✅ = le gano al buy & hold  |  CARTERA = las 3 juntas (lo que vives de verdad)")

    # Frontera riesgo/retorno: como cambia todo segun cuanto capital inviertes.
    print("\n🎚️  DIAL DE EXPOSICION — elige tu punto de comodidad")
    print("-" * 70)
    print(f"   {'invertido':<12} {'retorno':>10} {'maxDD':>10} {'efectivo':>10}")
    for e in (1.0, 0.75, 0.60, 0.50, 0.30):
        fp = backtest_portfolio(syms, max_exposure=e)
        if not fp.get("error"):
            print(f"   {int(e*100):>3}%{'':<9} {fp['return_pct']:>8.2f}%  {fp['max_drawdown_pct']:>8.2f}%"
                  f"  {int((1-e)*100):>7}%")
    print("-" * 70)
    print("   Menos exposicion = menos drawdown Y menos retorno. Ajusta max_exposure en .env")
