# Guía para novatos — Datos de WHOOP por API directa

**Objetivo:** ver los datos reales de WHOOP de Gael entrando al sistema, **directo de la API oficial
de WHOOP** (sin pagar agregador). Es una ruta alterna al plan Vital/Terra, ideal para la primera prueba.

> Complementa el ítem **0.2** del tracker. El código está en `tid-max/software/`.

## Qué vas a lograr
Un comando (`python whoop_sync.py`) que descarga recovery, HRV, sueño, strain y workouts de Gael
y los guarda como JSON. **Primer dato real por API propia. 🎉**

> ⚠️ Recuerda: WHOOP da métricas **ya procesadas**, no la señal cruda (PPG/IBI). Para DFA-α1 cruda
> sigue en pie el Polar H10 / EVK (ver `analisis/bandas-dato-crudo.md`). Esto es para **integración**, no para validar el pipeline.

## Parte 1 — En el portal de WHOOP (ya hecho ✅)
En `developer-dashboard.whoop.com` la app **GAEL SYNC** ya quedó con:
- **Redirect URL:** `http://localhost:8765/callback`
- **Scopes:** los 6 de lectura marcados
- **Client ID** y **Client Secret** copiados

> El scope `offline` (para acceso permanente) **no es un checkbox** del portal: lo agrega el script
> al autorizar. Por eso no aparece en la lista de la app.

## Parte 2 — Preparar el código (el dev, ~10 min)
```bash
cd tid-max/software
pip install -r requirements.txt
cp .env.example .env
```
En `.env` pega el **Client ID** y el **Client Secret**.

## Parte 3 — Autorizar con la cuenta de Gael (una sola vez)
```bash
python whoop_auth.py
```
1. Se abre el navegador en el login de WHOOP.
2. Entra con **usuario y contraseña de WHOOP de Gael** → **Autorizar**.
3. La pestaña dice "Listo, ya puedes cerrar". El **Refresh Token** se guarda solo.

## Parte 4 — Descargar los datos (repetible)
```bash
python whoop_sync.py
```
Verás un resumen (recovery, HRV, FC reposo, sueño, strain, # workouts) y el JSON crudo en `datos/`.

## Quién hace qué
| Tú (fundador) | El desarrollador |
|---|---|
| Ya creaste la app GAEL SYNC y copiaste las llaves | Instala, pega llaves en `.env` |
| Autorizas con la cuenta de Gael (paso 3) | Corre `whoop_sync.py` y revisa el JSON |
| Confirmas que ves los datos | Deja la ingesta lista para el pipeline (0.5) |

**Al terminar:** avisa "ya jalé datos de WHOOP por API" para anotar el avance de 0.2 en el tracker.
