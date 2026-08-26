"""Servicio de datos de mercado (Dia 2).

Descarga OHLCV historico, lo limpia y lo guarda en CSV (MVP) listo para que el
RiskEngine lo consuma. Mejoras sobre el borrador original:

  * Fallback multi-exchange: Binance esta geo-bloqueado en muchas IPs de nube
    (responde 451). Intentamos varios exchanges publicos en orden.
  * Relleno de huecos correcto: OHLC se rellena con el ultimo cierre conocido,
    pero el volumen de una vela faltante es 0 (no se arrastra el anterior).
  * pandas 2.2+: usamos .ffill() en vez de fillna(method=...) (deprecado).
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone

import ccxt
import pandas as pd

from app.config import all_symbols, settings

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")


def _build_exchange():
    """Devuelve el primer exchange de la lista que logre conectar."""
    last_err: Exception | None = None
    for ex_id in settings.exchange_list:
        try:
            ex = getattr(ccxt, ex_id)({"enableRateLimit": True})
            ex.load_markets()
            print(f"🔌 Conectado a {ex_id}")
            return ex
        except Exception as e:  # geo-block, red, etc.
            print(f"   ⚠️  {ex_id} no disponible ({type(e).__name__}); probando siguiente...")
            last_err = e
    raise RuntimeError(f"Ningun exchange disponible. Ultimo error: {last_err}")


def fetch_historical_data(exchange, symbol: str, timeframe: str, years: int) -> list[list]:
    """Descarga velas paginando desde `years` atras hasta hoy."""
    print(f"🔄 Descargando {symbol} ({years} anios) desde {exchange.id}...")
    start = datetime.now(timezone.utc) - timedelta(days=years * 365)
    since = int(start.timestamp() * 1000)
    now_ms = int(time.time() * 1000)

    all_candles: list[list] = []
    while True:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
        except Exception as e:
            print(f"   ❌ Error en {symbol}: {e}")
            break
        if not ohlcv:
            break

        all_candles.extend(ohlcv)
        last_ts = ohlcv[-1][0]
        since = last_ts + 1
        if last_ts >= now_ms - 60_000 or len(ohlcv) < 2:
            break
        time.sleep(exchange.rateLimit / 1000)

    return all_candles


def clean_and_save(symbol: str, candles: list[list], timeframe: str) -> pd.DataFrame | None:
    """Convierte a DataFrame, rellena huecos y guarda en CSV."""
    if not candles:
        print(f"⚠️  Sin datos para {symbol}")
        return None

    df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.drop_duplicates(subset=["timestamp"]).set_index("date").sort_index()

    # Reindexar al rango completo diario para detectar huecos (exchange caido).
    full_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D", tz="UTC")
    missing = len(full_range) - len(df)
    df = df.reindex(full_range)
    if missing > 0:
        print(f"   🩹 Rellenando {missing} velas faltantes...")
        # Volumen faltante = 0 (no hubo operaciones registradas para nosotros).
        df["volume"] = df["volume"].fillna(0.0)
        # OHLC: arrastrar el ultimo cierre conocido a todas las columnas de precio.
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].ffill()

    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{symbol.replace('/', '_')}_{timeframe}.csv")
    df.to_csv(path)
    print(f"✅ {symbol}: {len(df)} velas -> {path}")
    return df


def run_ingestion(symbols: list[str] | None = None) -> None:
    """Descarga y guarda el universo completo (o la lista dada)."""
    symbols = symbols or all_symbols(settings.quote_currency)
    print("🚀 INGESTA DE DATOS")
    print("-" * 40)
    exchange = _build_exchange()
    for symbol in symbols:
        candles = fetch_historical_data(exchange, symbol, settings.timeframe, settings.history_years)
        clean_and_save(symbol, candles, settings.timeframe)
    print("-" * 40)
    print("🏁 Ingesta completada.")


if __name__ == "__main__":
    run_ingestion()
