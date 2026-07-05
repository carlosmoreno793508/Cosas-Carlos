# 🧠 Investment Copilot

Sistema híbrido de apoyo a la inversión (cripto + bolsa) para uso personal.
**Ingeniería, no gambling.** El sistema propone, el riesgo manda y el humano
tiene la última palabra.

> Estado actual: **MVP en construcción**. Ya funciona el núcleo del cerebro
> (Risk Engine) validado con pruebas. Ingesta de datos, API y alertas de
> Telegram listas para conectar.

---

## 🎯 Qué hace (hoy)

- **Ingesta** OHLCV histórico del universo cripto (fallback multi-exchange).
- Calcula un **Risk Score 0–100** por activo con 3 factores duros
  (tendencia, volatilidad, drawdown).
- Traduce el score a un **nivel de autonomía**: 🟢 Autónomo / 🟡 Confirmar / 🔴 Protección.
- Expone todo por **API** y envía un **reporte diario a Telegram**.

## 🏗️ Arquitectura (regla de oro: el core no depende de la UI)

```
app/
├── config.py              # Universo + settings centralizados (.env)
├── main.py                # API FastAPI: /health /risk /killswitch
├── core/
│   └── risk_engine.py     # 🧠 Lógica pura, testeable sin red
├── services/
│   ├── market_data.py     # Ingesta CCXT + limpieza de huecos
│   └── alert_service.py   # Bot de Telegram
tests/
└── test_risk_engine.py    # Pruebas con datos sintéticos
run_cycle.py               # Job diario: datos → riesgo → alerta
```

## 🚀 Cómo arrancar

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar credenciales
cp .env.example .env        # y edita TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID

# 3. Correr las pruebas del cerebro (no requieren internet)
pytest -q

# 4. Descargar datos y calcular riesgo
python -m app.services.market_data     # ingesta histórica
python -m app.core.risk_engine         # reporte en terminal

# 5. Ciclo completo con alerta a Telegram
python run_cycle.py

# 6. Levantar la API
uvicorn app.main:app --reload          # http://localhost:8000/docs
```

Con Docker (incluye Postgres + Redis):

```bash
docker compose up -d --build
```

## 📐 Fórmula del Risk Score

```
RiskScore = Tendencia·0.40 + Volatilidad·0.30 + Drawdown·0.30
```

| Factor | Cómo se mide |
|--------|--------------|
| Tendencia (40%) | Precio vs MA200 + pendiente de la MA50 |
| Volatilidad (30%) | ATR% actual vs su media de 90 días (normalizado) |
| Drawdown (30%) | Caída desde el máximo móvil de 1 año |

Ver `runbook.md` para reglas por grupo de activo y operación diaria.

## 🧪 Etapa 1 — ¿funciona? (backtest)

El evaluador corre la estrategia sobre toda la historia con **costos reales**
(slippage 0.1% + comisión 0.1%) y reporta rendimiento, max drawdown, # de
operaciones y % de aciertos:

```bash
python -m app.core.backtest        # o GET /backtest
```

Criterio para pasar a Etapa 2: la estrategia sobrevive a los costos y el max
drawdown es tolerable para tu perfil.

## 🔀 Modelo híbrido

- **Cripto** (`BTC/USDT`, …) → el sistema **ejecuta** (paper, luego real).
- **Acciones/ETFs** (`SPY`, `QQQ`) → **advisory**: el sistema avisa, tú
  ejecutas en IBKR. Como es tu propio dinero, esto **no** es asesoría regulada.

## 🗺️ Roadmap corto

- [x] Estructura + config + Risk Engine con pruebas
- [x] Ingesta con fallback multi-exchange
- [x] API + alertas Telegram
- [x] Motor de oportunidades + paper trading (slippage + comisión)
- [x] Backtest (evaluador de Etapa 1)
- [ ] APScheduler para el reporte diario automático
- [ ] Dashboard (Streamlit)
- [ ] Persistir candles/risk en Postgres (hoy es CSV)
- [ ] Etapa 2: multi-usuario (solo si Etapa 1 convence)

## ⚠️ Nota

Sistema de apoyo a decisiones, **no** asesoría financiera. Empieza siempre en
modo *paper*. Las API keys de exchanges deben ir **sin permiso de retiro**.
