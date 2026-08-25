"""Motor de ejecucion en papel (paper trading).

Simula ordenes REALISTAS: aplica slippage y comision para no engañarnos con
resultados optimistas. Mantiene posiciones virtuales y calcula PnL.

Solo cripto se ejecuta aqui (modo 'paper'). La bolsa es advisory: no pasa por
este motor, solo se avisa.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

SLIPPAGE = 0.001    # 0.1% peor precio al entrar/salir
COMMISSION = 0.001  # 0.1% de comision por lado


@dataclass
class Position:
    symbol: str
    size: float
    entry_price: float   # precio efectivo ya con slippage
    stop: float
    target: float
    opened_at: str
    peak: float = 0.0    # maximo precio visto desde la entrada (para el stop de proteccion)

    def __post_init__(self):
        if not self.peak:
            self.peak = self.entry_price

    def unrealized_pnl(self, price: float) -> float:
        return (price - self.entry_price) * self.size


@dataclass
class PaperBroker:
    """Cartera virtual con una posicion por simbolo (MVP)."""

    cash: float
    equity_start: float = field(default=0.0)
    positions: dict[str, Position] = field(default_factory=dict)
    closed: list[dict] = field(default_factory=list)
    interest_earned: float = 0.0   # rendimiento tipo CETES acumulado en el efectivo
    last_accrual: str = ""         # ultima fecha en que se aplico el rendimiento (para el bot)

    def __post_init__(self):
        if not self.equity_start:
            self.equity_start = self.cash

    # --- rendimiento del efectivo (CETES) ---
    def accrue_cash_yield(self, annual_rate: float, days: float = 1.0) -> float:
        """Aplica rendimiento tipo CETES al efectivo ocioso (compuesto diario).

        Modela el "Agente de Proteccion": el dinero que NO esta en cripto no se
        queda en 0%, gana la tasa CETES mientras espera. Devuelve el interes ganado.
        """
        if annual_rate <= 0 or days <= 0 or self.cash <= 0:
            return 0.0
        interest = self.cash * ((1 + annual_rate) ** (days / 365.0) - 1)
        self.cash += interest
        self.interest_earned += interest
        return interest

    # --- ordenes ---
    def buy(self, symbol: str, price: float, size: float, stop: float, target: float, when: str) -> bool:
        eff = price * (1 + SLIPPAGE)                 # entras un poco mas caro
        cost = eff * size
        fee = cost * COMMISSION
        if symbol in self.positions or cost + fee > self.cash:
            return False
        self.cash -= cost + fee
        self.positions[symbol] = Position(symbol, size, eff, stop, target, when)
        return True

    def sell(self, symbol: str, price: float, when: str, reason: str) -> bool:
        pos = self.positions.pop(symbol, None)
        if pos is None:
            return False
        eff = price * (1 - SLIPPAGE)                 # sales un poco mas barato
        proceeds = eff * pos.size
        fee = proceeds * COMMISSION
        self.cash += proceeds - fee
        pnl = (eff - pos.entry_price) * pos.size - fee
        self.closed.append(
            {
                "symbol": symbol,
                "entry": pos.entry_price,
                "exit": eff,
                "size": pos.size,
                "pnl": pnl,
                "reason": reason,
                "opened_at": pos.opened_at,
                "closed_at": when,
            }
        )
        return True

    # --- estado ---
    def equity(self, prices: dict[str, float]) -> float:
        held = sum(p.unrealized_pnl(prices.get(s, p.entry_price)) + p.entry_price * p.size
                   for s, p in self.positions.items())
        return self.cash + held

    def stats(self, prices: dict[str, float]) -> dict:
        eq = self.equity(prices)
        wins = [t for t in self.closed if t["pnl"] > 0]
        return {
            "equity": round(eq, 2),
            "return_pct": round((eq / self.equity_start - 1) * 100, 2),
            "cash": round(self.cash, 2),
            "interest_earned": round(self.interest_earned, 2),
            "open_positions": len(self.positions),
            "trades_closed": len(self.closed),
            "win_rate_pct": round(len(wins) / len(self.closed) * 100, 1) if self.closed else 0.0,
        }

    # --- persistencia (para que el bot recuerde entre corridas) ---
    def to_dict(self) -> dict:
        return {
            "cash": self.cash,
            "equity_start": self.equity_start,
            "positions": {s: asdict(p) for s, p in self.positions.items()},
            "closed": self.closed,
            "interest_earned": self.interest_earned,
            "last_accrual": self.last_accrual,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PaperBroker":
        b = cls(cash=d["cash"], equity_start=d.get("equity_start", d["cash"]))
        b.positions = {s: Position(**p) for s, p in d.get("positions", {}).items()}
        b.closed = d.get("closed", [])
        b.interest_earned = d.get("interest_earned", 0.0)
        b.last_accrual = d.get("last_accrual", "")
        return b
