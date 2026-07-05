"""Pruebas del RiskEngine con datos SINTETICOS (sin red, sin CSV).

Validan que la matematica del cerebro sea coherente: un mercado alcista y
tranquilo debe dar riesgo bajo; un mercado en caida y volatil, riesgo alto.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.core.risk_engine import RiskEngine


def _make_df(closes: list[float], vol_factor: float = 0.01) -> pd.DataFrame:
    """Construye un OHLCV diario sintetico a partir de una serie de cierres."""
    n = len(closes)
    idx = pd.date_range("2020-01-01", periods=n, freq="D", tz="UTC")
    close = np.array(closes, dtype=float)
    high = close * (1 + vol_factor)
    low = close * (1 - vol_factor)
    return pd.DataFrame(
        {"open": close, "high": high, "low": low, "close": close, "volume": 1000.0},
        index=idx,
    )


def test_bull_market_low_risk():
    # Tendencia alcista suave y tranquila durante ~400 dias.
    closes = list(100 + np.arange(400) * 0.5)
    report = RiskEngine().compute_from_df("BULL/USDT", _make_df(closes, vol_factor=0.005))
    assert report is not None
    assert report["details"]["trend"] == "ALCISTA"
    assert report["risk_score"] < 30, f"esperaba riesgo bajo, dio {report['risk_score']}"


def test_bear_crash_high_risk():
    # Sube 300 dias y luego se desploma 40% con alta volatilidad.
    up = list(100 + np.arange(300) * 0.5)
    peak = up[-1]
    crash = list(np.linspace(peak, peak * 0.6, 100))
    df = _make_df(up + crash, vol_factor=0.06)
    report = RiskEngine().compute_from_df("BEAR/USDT", df)
    assert report is not None
    assert report["details"]["trend"] == "BAJISTA"
    assert report["details"]["drawdown_pct"] < -15
    assert report["risk_score"] >= 60, f"esperaba riesgo alto, dio {report['risk_score']}"


def test_autonomy_levels():
    assert "AUTONOMO" in RiskEngine.autonomy_level(10)
    assert "CONFIRMAR" in RiskEngine.autonomy_level(45)
    assert "PROTECCION" in RiskEngine.autonomy_level(80)


def test_insufficient_history_returns_none():
    # Menos de 200 velas => no se puede calcular MA200.
    report = RiskEngine().compute_from_df("SHORT/USDT", _make_df(list(range(100, 150))))
    assert report is None
