"""Estado del bot (paper) en texto — para revisar como va de un vistazo.

Uso:
    python -m app.services.bot_status
"""
from __future__ import annotations

from app.services import dashboard_data as dd


def main() -> None:
    snap = dd.portfolio_snapshot()
    s = snap["stats"]

    print("\n🤖 ESTADO DEL BOT (paper)")
    print("=" * 44)
    print(f"💼 Equity:      ${s['equity']:,.2f}  ({s['return_pct']:+.2f}%)")
    print(f"💵 Efectivo:    ${s['cash']:,.2f}")
    print(f"📊 Posiciones:  {s['open_positions']} abiertas")
    print(f"🔁 Operaciones: {s['trades_closed']} cerradas  (aciertos {s['win_rate_pct']}%)")
    print(f"🛑 Kill switch: {'ACTIVO' if snap['kill_switch'] else 'apagado'}")

    if snap["positions"]:
        print("\n📌 POSICIONES ABIERTAS")
        for p in snap["positions"]:
            print(f"   {p['symbol']:<10} entrada ${p['entry']:,.4f}  ahora ${p['price']:,.4f}  "
                  f"PnL {p['pnl_pct']:+.2f}%")
    else:
        print("\n📌 Sin posiciones abiertas — todo en efectivo (mercado bajista).")

    if snap["closed"]:
        print("\n📜 ULTIMAS OPERACIONES CERRADAS")
        for t in snap["closed"][-5:]:
            print(f"   {t['symbol']:<10} {t.get('reason', ''):<14} PnL ${t['pnl']:,.2f}")

    print("=" * 44)


if __name__ == "__main__":
    main()
