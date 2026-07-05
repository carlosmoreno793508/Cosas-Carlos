"""Motor de Riesgo (Dia 3) — el cerebro del sistema.

Calcula un Risk Score 0-100 (0 = cielo despejado, 100 = tormenta perfecta) a
partir de tres factores tecnicos duros:

    Tendencia  (40%) : precio vs MA200 + pendiente MA50
    Volatilidad(30%) : ATR% actual vs su media de 90 dias
    Drawdown   (30%) : caida desde el maximo movil de 1 anio

Diseno clave: la matematica NO depende del almacenamiento. `compute_from_df`
recibe un DataFrame y se puede probar con datos sinteticos (sin red, sin CSV).
`compute_risk_profile` es solo un wrapper que lee el CSV y llama a la logica.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")

# Ponderaciones de la formula maestra (deben sumar 1.0).
W_TREND, W_VOL, W_DD = 0.40, 0.30, 0.30

# Si el ultimo dato tiene mas de estos dias de antiguedad => datos rancios.
STALE_DAYS = 3


class RiskEngine:
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir

    # ---------- carga (infraestructura, separable) ----------
    def load_data(self, symbol: str, timeframe: str = "1d") -> pd.DataFrame | None:
        path = os.path.join(self.data_dir, f"{symbol.replace('/', '_')}_{timeframe}.csv")
        if not os.path.exists(path):
            print(f"❌ Sin datos para {symbol}. Corre market_data.py primero.")
            return None
        df = pd.read_csv(path)
        date_col = "date" if "date" in df.columns else df.columns[0]
        df[date_col] = pd.to_datetime(df[date_col], utc=True)
        return df.set_index(date_col).sort_index()

    # ---------- indicadores (logica pura, testeable) ----------
    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # 1. TENDENCIA: precio vs MA200; penaliza si la MA50 apunta hacia abajo.
        df["ma50"] = df["close"].rolling(50).mean()
        df["ma200"] = df["close"].rolling(200).mean()
        below = df["close"] < df["ma200"]
        ma50_falling = df["ma50"] < df["ma50"].shift(5)
        df["trend_score"] = np.where(below, 100.0, 0.0)
        # Aunque el precio siga arriba de la MA200, una MA50 cayendo suma riesgo.
        df.loc[~below & ma50_falling, "trend_score"] = 40.0

        # 2. VOLATILIDAD: ATR% actual vs su media de 90 dias (normalizado en %).
        prev_close = df["close"].shift(1)
        tr = pd.concat(
            [
                df["high"] - df["low"],
                (df["high"] - prev_close).abs(),
                (df["low"] - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)
        df["atr"] = tr.rolling(14).mean()
        df["atr_pct"] = df["atr"] / df["close"] * 100
        vol_ma90 = df["atr_pct"].rolling(90).mean()
        # Score gradual: 0 si esta tranquila, hasta 100 si dobla su media historica.
        ratio = (df["atr_pct"] / vol_ma90).clip(lower=0)
        df["vol_score"] = ((ratio - 1.0) * 100).clip(0, 100)

        # 3. DRAWDOWN: caida desde el maximo movil de 1 anio.
        roll_max = df["close"].rolling(365, min_periods=1).max()
        df["drawdown"] = (df["close"] - roll_max) / roll_max
        df["dd_score"] = np.select(
            [df["drawdown"] < -0.15, df["drawdown"] < -0.05],
            [100.0, 50.0],
            default=0.0,
        )

        df["total_risk"] = (
            df["trend_score"] * W_TREND
            + df["vol_score"] * W_VOL
            + df["dd_score"] * W_DD
        )
        return df

    # ---------- perfil (une todo) ----------
    def compute_from_df(self, symbol: str, df: pd.DataFrame) -> dict | None:
        df = self.calculate_indicators(df).dropna(subset=["ma200", "atr_pct"])
        if df.empty:
            print(f"⚠️  {symbol}: historia insuficiente (se necesitan >200 velas).")
            return None

        latest = df.iloc[-1]
        last_date = latest.name.to_pydatetime()
        age_days = (datetime.now(timezone.utc) - last_date).days
        is_stale = age_days > STALE_DAYS

        return {
            "symbol": symbol,
            "date": last_date.date().isoformat(),
            "price": float(latest["close"]),
            "risk_score": int(round(float(latest["total_risk"]))),
            "is_stale": is_stale,  # bloquea nuevas entradas si True (Kill Switch)
            "level": self.autonomy_level(float(latest["total_risk"])),
            "details": {
                "trend": "BAJISTA" if latest["trend_score"] > 50 else "ALCISTA",
                "atr_pct": round(float(latest["atr_pct"]), 2),
                "vol_score": int(round(float(latest["vol_score"]))),
                "drawdown_pct": round(float(latest["drawdown"]) * 100, 2),
                "age_days": age_days,
            },
        }

    def compute_risk_profile(self, symbol: str, timeframe: str = "1d") -> dict | None:
        df = self.load_data(symbol, timeframe)
        if df is None:
            return None
        return self.compute_from_df(symbol, df)

    @staticmethod
    def autonomy_level(score: float) -> str:
        """Traduce el score al nivel de autonomia hibrida de Carlos."""
        if score < 30:
            return "🟢 AUTONOMO"
        if score < 60:
            return "🟡 CONFIRMAR"
        return "🔴 PROTECCION"


if __name__ == "__main__":
    from app.config import all_symbols, settings

    engine = RiskEngine()
    print("\n📊 REPORTE DE RIESGO ACTUAL")
    print("=" * 40)
    for asset in all_symbols(settings.quote_currency):
        report = engine.compute_risk_profile(asset)
        if report:
            print(f"\n🔹 {report['symbol']}  ${report['price']:,.2f}")
            print(f"   Riesgo: {report['risk_score']}/100  {report['level']}")
            print(f"   {report['details']}")
    print("\n" + "=" * 40)
