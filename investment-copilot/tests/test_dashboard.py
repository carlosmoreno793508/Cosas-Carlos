"""Pruebas del modulo de datos del dashboard (sin Streamlit)."""
from __future__ import annotations

from app.services import dashboard_data as dd


def test_global_risk_averages():
    rows = [{"risk_score": 20}, {"risk_score": 40}, {"risk_score": 60}]
    g = dd.global_risk(rows)
    assert g["score"] == 40
    assert "level" in g


def test_global_risk_empty():
    assert dd.global_risk([]) is None


def test_observation_universe_excludes_active():
    obs = dd.observation_universe()
    assert "BTC/USDT" not in obs   # BTC es activo, no observacion
    assert "SOL/USDT" in obs       # SOL esta en observacion


def test_snapshot_without_state(monkeypatch):
    # Sin archivo de estado, el snapshot arranca con el capital inicial y sin posiciones.
    monkeypatch.setattr(dd, "STATE_FILE", "/nonexistent/bot_state.json")
    snap = dd.portfolio_snapshot()
    assert snap["positions"] == []
    assert snap["stats"]["open_positions"] == 0
