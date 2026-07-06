"""Dashboard del Investment Copilot (Streamlit).

Vista limpia y sin ruido del estado del bot: capital, riesgo, posiciones y
operaciones. Lee el mismo estado que el bot (data_storage/bot_state.json).

Uso:
    streamlit run dashboard.py
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app.config import active_symbols, settings
from app.services import dashboard_data as dd

st.set_page_config(page_title="Investment Copilot", page_icon="🧠", layout="wide")
st.title("🧠 Investment Copilot")
st.caption("Modo paper (dinero simulado) · El riesgo manda")

snap = dd.portfolio_snapshot()
stats = snap["stats"]

# --- Estado del sistema ---
if snap["kill_switch"]:
    st.error("🛑 KILL SWITCH ACTIVO — el bot no abre nuevas operaciones")
else:
    st.success("🟢 Sistema activo")

# --- Metricas principales ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Capital (equity)", f"${stats['equity']:,.2f}", f"{stats['return_pct']:+.2f}%")
c2.metric("Efectivo", f"${stats['cash']:,.2f}")
c3.metric("Posiciones abiertas", stats["open_positions"])
c4.metric("Operaciones cerradas", stats["trades_closed"])

# --- Riesgo ---
st.subheader("🛡️ Riesgo")
active = active_symbols(settings.quote_currency)
rows = dd.risk_table(active)
g = dd.global_risk(rows)
if g:
    st.metric("Riesgo global", f"{g['score']}/100", g["level"])
if rows:
    df = pd.DataFrame(
        [
            {
                "Activo": r["symbol"],
                "Precio": f"${r['price']:,.4f}",
                "Riesgo": r["risk_score"],
                "Nivel": r["level"],
                "Tendencia": r["details"]["trend"],
                "Drawdown %": r["details"]["drawdown_pct"],
            }
            for r in rows
        ]
    )
    st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.info("Aún no hay datos de riesgo. Corre la ingesta: `python3 -m app.services.market_data`")

# --- Posiciones abiertas ---
st.subheader("💼 Posiciones abiertas")
if snap["positions"]:
    dfp = pd.DataFrame(
        [
            {
                "Activo": p["symbol"],
                "Entrada": f"${p['entry']:,.4f}",
                "Precio": f"${p['price']:,.4f}",
                "PnL": f"${p['pnl']:,.2f}",
                "PnL %": f"{p['pnl_pct']:+.2f}%",
                "Desde": p["opened_at"],
            }
            for p in snap["positions"]
        ]
    )
    st.dataframe(dfp, hide_index=True, use_container_width=True)
else:
    st.info("Sin posiciones abiertas.")

# --- Grafica precio vs MA200 ---
st.subheader("📈 Precio vs MA200")
if active:
    sym = st.selectbox("Activo", active)
    hist = dd.price_history(sym)
    if hist is not None and not hist.empty:
        chart_df = hist.reset_index()
        chart_df = chart_df.rename(columns={chart_df.columns[0]: "fecha"})
        # Quita la zona horaria (Altair no la traga en el eje x).
        chart_df["fecha"] = pd.to_datetime(chart_df["fecha"], utc=True).dt.tz_localize(None)
        st.line_chart(chart_df, x="fecha", y=["close", "ma200"])
    else:
        st.info("Sin histórico para graficar.")

# --- Historial de operaciones ---
if snap["closed"]:
    st.subheader("📜 Historial de operaciones")
    st.dataframe(pd.DataFrame(snap["closed"]), hide_index=True, use_container_width=True)

obs = dd.observation_universe()
if obs:
    st.caption("👀 En observación (no operado): " + ", ".join(obs))
