"""Pruebas de la estrategia compartida, el stop de proteccion y el bot (paper)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from app.core import strategy
from app.core.backtest import backtest_symbol
from app.core.paper_engine import PaperBroker


def _make_df(closes: list[float], vf: float = 0.01) -> pd.DataFrame:
    n = len(closes)
    idx = pd.date_range("2020-01-01", periods=n, freq="D", tz="UTC")
    c = np.array(closes, dtype=float)
    return pd.DataFrame(
        {"open": c, "high": c * (1 + vf), "low": c * (1 - vf), "close": c, "volume": 1000.0},
        index=idx,
    )


# ---------- decisiones de la estrategia ----------
def test_decide_enter_and_exits():
    # Sin posicion, alcista, riesgo ok -> ENTER
    assert strategy.decide(110, 100, 20, holding=False, peak_price=0) == strategy.ENTER
    # Con posicion, precio bajo MA200 -> EXIT_TREND
    assert strategy.decide(90, 100, 20, holding=True, peak_price=120) == strategy.EXIT_TREND
    # Con posicion, cayo >25% del pico (200 -> 140) pero sigue > MA200 -> EXIT_PROTECT
    assert strategy.decide(140, 100, 20, holding=True, peak_price=200) == strategy.EXIT_PROTECT
    # Riesgo en zona roja -> no entra
    assert strategy.decide(110, 100, 80, holding=False, peak_price=0) == strategy.FLAT


def test_protection_stop_reduces_drawdown():
    # Sube fuerte y luego cae en picada. El stop de proteccion debe cortar la
    # perdida antes que la lenta MA200 -> drawdown menos brutal que sin el.
    up = list(100 * (1.01 ** np.arange(300)))
    peak = up[-1]
    crash = list(np.linspace(peak, peak * 0.4, 60))  # -60% rapido
    stats = backtest_symbol("BTC/USDT", _make_df(up + crash, 0.01), capital=10_000)
    # Con proteccion al -25%, el drawdown de la cartera no debe acercarse al -60%.
    assert stats["max_drawdown_pct"] > -45


# ---------- persistencia del broker (memoria del bot) ----------
def test_broker_roundtrip():
    b = PaperBroker(cash=10_000)
    b.buy("BTC/USDT", 100.0, 5, 90, 100, "2020-01-01")
    b.positions["BTC/USDT"].peak = 150.0
    restored = PaperBroker.from_dict(json.loads(json.dumps(b.to_dict())))
    assert restored.cash == b.cash
    assert "BTC/USDT" in restored.positions
    assert restored.positions["BTC/USDT"].peak == 150.0


def test_portfolio_diversifies_drawdown(tmp_path):
    # 3 activos con caidas en momentos DISTINTOS -> el drawdown de la cartera
    # debe ser menor (menos negativo) que el de la peor moneda sola.
    from app.core.backtest import backtest_portfolio, backtest_symbol

    def series(shift):
        base = list(100 * (1.004 ** np.arange(500)))
        # inserta un desplome de -40% en una ventana distinta por activo
        for i in range(200 + shift, 240 + shift):
            base[i] = base[200 + shift] * 0.6
        return base

    syms = ["BTC/USDT", "ETH/USDT", "XRP/USDT"]
    for i, s in enumerate(syms):
        df = _make_df(series(i * 60), 0.01)
        df.index.name = "date"
        df.to_csv(tmp_path / f"{s.replace('/', '_')}_1d.csv")

    singles = [backtest_symbol(s, _make_df(series(i * 60), 0.01))["max_drawdown_pct"]
               for i, s in enumerate(syms)]
    port = backtest_portfolio(syms, data_dir=str(tmp_path))
    # la cartera no cae tan hondo como la peor moneda individual
    assert port["max_drawdown_pct"] > min(singles)


def test_exposure_dial_reduces_drawdown(tmp_path):
    # Menos exposicion debe dar un drawdown menos profundo (y menos retorno).
    from app.core.backtest import backtest_portfolio

    up = list(100 * (1.006 ** np.arange(300)))
    peak = up[-1]
    crash = list(np.linspace(peak, peak * 0.5, 100))
    for s in ["BTC/USDT", "ETH/USDT"]:
        df = _make_df(up + crash, 0.01)
        df.index.name = "date"
        df.to_csv(tmp_path / f"{s.replace('/', '_')}_1d.csv")

    full = backtest_portfolio(["BTC/USDT", "ETH/USDT"], data_dir=str(tmp_path), max_exposure=1.0)
    half = backtest_portfolio(["BTC/USDT", "ETH/USDT"], data_dir=str(tmp_path), max_exposure=0.5)
    assert half["max_drawdown_pct"] > full["max_drawdown_pct"]  # menos hondo
    assert half["return_pct"] < full["return_pct"]              # y menos retorno


def test_cetes_yield_grows_idle_cash():
    # El efectivo ocioso debe crecer con la tasa CETES; 8% anual por 365 dias ~ +8%.
    b = PaperBroker(cash=10_000)
    total = 0.0
    for _ in range(365):
        total += b.accrue_cash_yield(0.08, days=1)
    assert abs(b.cash - 10_800) < 5           # ~+8% en un anio
    assert abs(b.interest_earned - total) < 1e-6
    # Sin tasa o sin efectivo, no pasa nada.
    b2 = PaperBroker(cash=10_000)
    assert b2.accrue_cash_yield(0.0, days=1) == 0.0


def test_cetes_lifts_backtest_return(tmp_path):
    # Con CETES, una cartera que pasa tiempo en efectivo rinde mas que sin CETES.
    from app.core.backtest import backtest_portfolio
    # Serie que sube y luego cae bajo MA200 (el bot sale y se queda en cash).
    up = list(100 * (1.005 ** np.arange(300)))
    peak = up[-1]
    crash = list(np.linspace(peak, peak * 0.5, 250))
    for s in ["BTC/USDT", "ETH/USDT"]:
        df = _make_df(up + crash, 0.01)
        df.index.name = "date"
        df.to_csv(tmp_path / f"{s.replace('/', '_')}_1d.csv")
    sin = backtest_portfolio(["BTC/USDT", "ETH/USDT"], data_dir=str(tmp_path), cetes_rate=0.0)
    con = backtest_portfolio(["BTC/USDT", "ETH/USDT"], data_dir=str(tmp_path), cetes_rate=0.10)
    assert con["return_pct"] > sin["return_pct"]
    assert con["interest_earned"] > 0
