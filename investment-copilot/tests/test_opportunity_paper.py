"""Pruebas de los motores de oportunidad, paper trading y backtest.

Todo con datos SINTETICOS (sin red, sin CSV).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.config import asset_class, execution_mode
from app.core.backtest import backtest_symbol
from app.core.opportunity_engine import OpportunityEngine
from app.core.paper_engine import COMMISSION, SLIPPAGE, PaperBroker


def _make_df(closes: list[float], vol_factor: float = 0.01) -> pd.DataFrame:
    n = len(closes)
    idx = pd.date_range("2020-01-01", periods=n, freq="D", tz="UTC")
    close = np.array(closes, dtype=float)
    return pd.DataFrame(
        {
            "open": close,
            "high": close * (1 + vol_factor),
            "low": close * (1 - vol_factor),
            "close": close,
            "volume": 1000.0,
        },
        index=idx,
    )


# ---------- config hibrida ----------
def test_hybrid_modes():
    assert asset_class("BTC/USDT") == "crypto"
    assert execution_mode("BTC/USDT") == "paper"
    assert asset_class("SPY") == "equity"
    assert execution_mode("SPY") == "advisory"


# ---------- motor de oportunidades ----------
def test_proposal_in_uptrend():
    closes = list(100 + np.arange(400) * 0.5)
    prop = OpportunityEngine().build_proposal("BTC/USDT", _make_df(closes, 0.005), capital=10_000)
    assert prop is not None
    assert prop["stop"] < prop["entry"] < prop["target"]
    assert prop["size"] > 0
    assert prop["execution_mode"] == "paper"


def test_no_proposal_in_downtrend():
    # Precio por debajo de una MA200 alta => sin setup de compra.
    closes = list(np.linspace(200, 100, 400))
    prop = OpportunityEngine().build_proposal("BTC/USDT", _make_df(closes), capital=10_000)
    assert prop is None


# ---------- paper broker: costos reales ----------
def test_paper_costs_applied():
    b = PaperBroker(cash=10_000)
    assert b.buy("BTC/USDT", price=100.0, size=10, stop=90, target=120, when="2020-01-01")
    # Entrada efectiva con slippage; cash baja por costo + comision.
    expected_cost = 100 * (1 + SLIPPAGE) * 10
    expected_fee = expected_cost * COMMISSION
    assert abs(b.cash - (10_000 - expected_cost - expected_fee)) < 1e-6
    # No se puede abrir dos veces el mismo simbolo.
    assert not b.buy("BTC/USDT", price=100.0, size=1, stop=90, target=120, when="2020-01-02")


def test_paper_sell_records_trade():
    b = PaperBroker(cash=10_000)
    b.buy("BTC/USDT", 100.0, 10, 90, 120, "2020-01-01")
    assert b.sell("BTC/USDT", 120.0, "2020-01-10", "target")
    assert len(b.closed) == 1
    assert b.closed[0]["pnl"] > 0  # vendio mas caro de lo que compro


# ---------- backtest ----------
def test_backtest_runs_and_reports():
    # Uptrend con un pullback para forzar al menos una entrada.
    closes = list(100 + np.arange(500) * 0.4 + 5 * np.sin(np.arange(500) / 20))
    stats = backtest_symbol("BTC/USDT", _make_df(closes, 0.01), capital=10_000)
    assert "return_pct" in stats
    assert "max_drawdown_pct" in stats
    assert "buy_hold_pct" in stats  # benchmark de comprar-y-aguantar
    assert stats["max_drawdown_pct"] <= 0  # el drawdown nunca es positivo


def test_trailing_stop_lets_winner_run():
    # En una tendencia alcista fuerte, el trailing stop debe capturar buena
    # parte del movimiento (mas que un objetivo fijo 2:1 que cortaria temprano).
    closes = list(100 * (1.004 ** np.arange(500)))  # +0.4% diario compuesto
    stats = backtest_symbol("BTC/USDT", _make_df(closes, 0.008), capital=10_000)
    assert stats["return_pct"] > 20  # captura una porcion grande del trend
