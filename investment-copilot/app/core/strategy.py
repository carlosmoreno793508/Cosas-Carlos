"""Estrategia — la fuente UNICA de verdad para decidir comprar/vender.

Tanto el backtest (mira el pasado) como el bot (opera hacia adelante) llaman a
`decide()`. Asi NUNCA se desincronizan: lo que el backtest valido es
exactamente lo que el bot ejecuta.

Reglas (estrategia v3 + Agente de Proteccion):
  ENTRAR  : sin posicion, precio > MA200 y riesgo fuera de zona roja.
  SALIR   : con posicion y...
      - precio < MA200            -> "EXIT_TREND"   (se rompio la tendencia)
      - cae >= PROTECTION_DD del pico -> "EXIT_PROTECT" (freno de emergencia)
  Si no, HOLD (con posicion) o FLAT (sin posicion).
"""
from __future__ import annotations

MAX_RISK_SCORE = 60      # >60 = zona roja: no se entra
PROTECTION_DD = 0.25     # Agente de Proteccion: sale si cae 25% desde el pico

ENTER, EXIT_TREND, EXIT_PROTECT, HOLD, FLAT = (
    "ENTER", "EXIT_TREND", "EXIT_PROTECT", "HOLD", "FLAT",
)


def decide(price: float, ma200: float, total_risk: float, holding: bool, peak_price: float) -> str:
    """Devuelve la accion para un activo dado su estado actual."""
    if holding:
        if price < ma200:
            return EXIT_TREND
        if peak_price > 0 and price <= peak_price * (1 - PROTECTION_DD):
            return EXIT_PROTECT
        return HOLD
    if price > ma200 and total_risk <= MAX_RISK_SCORE:
        return ENTER
    return FLAT
