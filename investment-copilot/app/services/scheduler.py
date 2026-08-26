"""Scheduler — el reloj del bot.

Corre el ciclo del bot automaticamente a una hora fija cada dia (por defecto
8:30 AM). Mantenlo corriendo en tu Mac o en un VPS y el bot trabaja solo.

Uso:
    python -m app.services.scheduler        # queda corriendo; Ctrl+C para parar
"""
from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.bot import run_bot_cycle

HOUR, MINUTE = 8, 30  # hora local del ciclo diario


def main() -> None:
    sched = BlockingScheduler()
    sched.add_job(run_bot_cycle, "cron", hour=HOUR, minute=MINUTE, id="daily_bot")
    print(f"⏰ Scheduler activo. El bot correra todos los dias a las {HOUR:02d}:{MINUTE:02d}.")
    print("   (deja esta ventana abierta; Ctrl+C para detener)")
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Scheduler detenido.")


if __name__ == "__main__":
    main()
