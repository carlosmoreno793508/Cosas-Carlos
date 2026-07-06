# 📋 Runbook — Investment Copilot

Manual operativo. Qué hace el sistema, cómo se opera y qué reglas nunca se rompen.

## 🧭 Reglas de oro (pegadas en la pared)

1. El sistema no improvisa.
2. El riesgo manda.
3. Toda excepción queda logueada.
4. Si algo no se entiende → no se ejecuta.
5. Siempre se puede pausar (Kill Switch manda sobre todo).

## 🚦 Niveles de autonomía

| Risk Score | Nivel | El sistema | Tú |
|-----------|-------|-----------|-----|
| 0–30 | 🟢 Autónomo | Ejecuta entradas/salidas | Solo ves reportes |
| 31–60 | 🟡 Confirmación | Arma la orden y espera | Apruebas/rechazas (1 tap) |
| 61–100 | 🔴 Protección | NO entra, protege capital | Decides si rompes la regla (queda logueado) |

## 🪙 Reglas por grupo de activo

| Grupo | Activos | Allocation máx. | Estrategia | Stop |
|-------|---------|----------------|-----------|------|
| **Core** | BTC, ETH | 40–50% del cripto | Trend following | Holgado (~2× ATR) |
| **Infra** | SOL, XRP, HBAR | 20–30% | Swing (solo si BTC alcista/lateral) | Medio (~1.5× ATR) |
| **Utility** | XLM, ALGO, IOTA, XDC | 5–10% c/u (máx 20% grupo) | Momentum | Estricto (~1× ATR); si cae >5% en 1h → cerrar |

## 🛡️ Kill Switch — disparadores automáticos

- **Hard stop global**: cartera cae >5% en el día → todo a cash (USDC/USDT).
- **API failure**: exchange da timeout 3 veces seguidas → pausar sistema.
- **Data stale**: precio sin actualizar > `STALE_DAYS` (3d) → bloquear entradas
  nuevas (implementado: `report["is_stale"]` en el Risk Engine).

Activar manualmente: `POST /killswitch?activate=true`.

## 🔁 Operación diaria

1. `run_cycle.py` (o el scheduler) corre a hora fija.
2. Actualiza datos → calcula riesgo → manda reporte a Telegram.
3. Revisas el reporte. Si hay 🟡, decides desde el chat/dashboard.
4. Todo queda registrado.

## ✅ Definition of Done del MVP

- [ ] Risk Score reproducible y estable (no fluctúa errático).
- [ ] Alertas llegan y no se duplican.
- [ ] Paper PnL coincide con precios históricos.
- [ ] Kill Switch detiene todo en < 2s.
- [ ] Logs completos. **Nada pasa a DONE sin log.**

## 🧪 Forward test (Etapa 1.5) — el bot en paper hacia adelante

Objetivo: ver al bot operar en mercado que aún no conoce, con dinero simulado,
antes de arriesgar un peso real. Duración sugerida: 2–6 semanas.

Arranque (una vez):
1. Crear bot de Telegram con `@BotFather` → obtener token y chat_id.
2. `cp .env.example .env` y poner `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`,
   `PAPER_CAPITAL` y `MAX_EXPOSURE`.
3. Primer ciclo manual: `python3 -m app.services.bot` (debe llegar mensaje a Telegram).

Mantenerlo corriendo (elige uno):
- **Manual** (más simple y a prueba de fallos): `python3 -m app.services.bot` una vez
  al día, más o menos a la misma hora. Con velas diarias, esto basta.
- **Automático**: `python3 -m app.services.scheduler` (deja la ventana abierta y el
  Mac despierto), o un cron: `30 8 * * * cd <ruta> && ./venv/bin/python -m app.services.bot >> bot.log 2>&1`.

Qué observar:
- El bot puede pasar **días sin operar**. Es NORMAL (pocas operaciones por diseño).
- El estado vive en `data_storage/bot_state.json` (posiciones + efectivo simulados).
- Kill Switch (`KILL_SWITCH=true` en `.env`) detiene toda operación nueva.

Criterio de éxito: el bot se comporta como el backtest (entra/sale con la lógica
esperada, sin errores), y el drawdown vivido está dentro de lo que toleras.

## 🔐 Seguridad

- API keys de exchange **sin permiso de retiro**.
- `.env` nunca se sube al repo (está en `.gitignore`).
- Para acceso remoto a la API: IP whitelist + auth básica (más simple y seguro
  que FaceID para el MVP).
