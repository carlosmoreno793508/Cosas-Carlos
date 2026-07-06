"""Motor de Oportunidades (Dia 4).

Convierte indicadores + Risk Score en una PROPUESTA de trade concreta:
entrada, stop (por ATR y grupo), objetivo (R/R), tamano por riesgo y modo de
ejecucion. NO ejecuta nada: solo propone. La ejecucion la hace paper_engine
(cripto) o simplemente se avisa (bolsa, modo advisory).

Regla dura del sistema: solo se propone COMPRA cuando la tendencia es alcista
(precio > MA200) y el riesgo no esta en zona roja. "No atrapes cuchillos".
"""
from __future__ import annotations

import pandas as pd

from app.config import asset_class, execution_mode, group_of, stop_mult
from app.core.risk_engine import RiskEngine

# Parametros de la estrategia MVP.
RR_TARGET = 2.0        # objetivo = 2x el riesgo por unidad
RISK_PER_TRADE = 0.01  # se arriesga 1% del capital por operacion
MAX_RISK_SCORE = 60    # >60 (zona roja) => no se propone entrada


class OpportunityEngine:
    def __init__(self, risk_engine: RiskEngine | None = None):
        self.risk = risk_engine or RiskEngine()

    def build_proposal(self, symbol: str, df: pd.DataFrame, capital: float) -> dict | None:
        """Devuelve una propuesta de compra o None si no hay setup valido."""
        ind = self.risk.calculate_indicators(df).dropna(subset=["ma200", "atr"])
        if ind.empty:
            return None

        row = ind.iloc[-1]
        risk_score = float(row["total_risk"])
        entry = float(row["close"])
        atr = float(row["atr"])

        # Filtros: tendencia alcista + riesgo fuera de zona roja + ATR valido.
        bullish = entry > float(row["ma200"])
        if not bullish or risk_score > MAX_RISK_SCORE or atr <= 0:
            return None

        stop = entry - stop_mult(symbol) * atr
        risk_per_unit = entry - stop
        if risk_per_unit <= 0:
            return None

        target = entry + RR_TARGET * risk_per_unit
        size = (capital * RISK_PER_TRADE) / risk_per_unit  # sizing por riesgo

        return {
            "symbol": symbol,
            "asset_class": asset_class(symbol),
            "group": group_of(symbol),
            "execution_mode": execution_mode(symbol),
            "level": RiskEngine.autonomy_level(risk_score),
            "risk_score": int(round(risk_score)),
            "entry": round(entry, 6),
            "stop": round(stop, 6),
            "target": round(target, 6),
            "rr": RR_TARGET,
            "size": round(size, 6),
            "notional": round(size * entry, 2),
            "date": row.name.date().isoformat(),
        }
