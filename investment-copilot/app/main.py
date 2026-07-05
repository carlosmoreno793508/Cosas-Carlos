"""Punto de entrada FastAPI (Dia 1).

Expone los endpoints del MVP. La logica pesada vive en core/ y services/;
aqui solo orquestamos y respondemos.
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.config import all_symbols, settings
from app.core.backtest import run_backtests
from app.core.opportunity_engine import OpportunityEngine
from app.core.risk_engine import RiskEngine

engine = RiskEngine()
opportunities = OpportunityEngine(engine)

# Estado en memoria (en produccion viviria en Redis, ver docker-compose).
STATE = {"kill_switch": settings.kill_switch}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Startup: Investment Copilot")
    yield
    print("🛑 Shutdown")


app = FastAPI(title="Investment Copilot", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "online", "mode": "paper_trading", "kill_switch": STATE["kill_switch"]}


@app.get("/assets")
def assets():
    return {"universe": all_symbols(settings.quote_currency)}


@app.get("/risk/{base}")
def risk(base: str):
    """Risk score de un activo, ej. /risk/BTC."""
    symbol = f"{base.upper()}/{settings.quote_currency}"
    report = engine.compute_risk_profile(symbol)
    if report is None:
        raise HTTPException(404, f"Sin datos para {symbol}. Corre la ingesta primero.")
    return report


@app.get("/risk")
def risk_portfolio():
    """Risk score de todo el universo + score global promedio."""
    reports = [engine.compute_risk_profile(s) for s in all_symbols(settings.quote_currency)]
    reports = [r for r in reports if r]
    if not reports:
        raise HTTPException(404, "Sin datos. Corre la ingesta primero.")
    global_score = round(sum(r["risk_score"] for r in reports) / len(reports))
    return {"global_risk": global_score, "level": RiskEngine.autonomy_level(global_score), "assets": reports}


@app.get("/proposals")
def proposals(capital: float = 10_000.0):
    """Propuestas de trade vigentes para el universo cripto."""
    out = []
    for symbol in all_symbols(settings.quote_currency):
        df = engine.load_data(symbol)
        if df is None:
            continue
        prop = opportunities.build_proposal(symbol, df, capital)
        if prop:
            out.append(prop)
    return {"count": len(out), "proposals": out}


@app.get("/backtest")
def backtest(capital: float = 10_000.0):
    """Corre el backtest del universo cripto (evaluador de Etapa 1)."""
    return {"results": run_backtests(all_symbols(settings.quote_currency), capital)}


@app.post("/killswitch")
def kill_switch(activate: bool = True):
    """Freno de mano: bloquea toda ejecucion nueva."""
    STATE["kill_switch"] = activate
    return {"kill_switch": STATE["kill_switch"]}
