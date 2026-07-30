# WHOOP — prueba de datos directos (API v2)

Prueba mínima para **jalar los datos de WHOOP de Gael directo de la API oficial** (sin agregador),
y confirmar que el flujo de datos funciona. Cubre el ítem **0.2** del tracker por la ruta de API directa.

> **Qué SÍ trae:** recovery, HRV diaria, sueño, strain/cycles, workouts, perfil y medidas.
> **Qué NO trae:** PPG/IBI **crudo** (WHOOP no lo expone). Para DFA-α1 cruda → Polar H10 / EVK.

## Requisitos
- Python 3.9+
- La app **GAEL SYNC** ya creada en `developer-dashboard.whoop.com` con:
  - Redirect URL = `http://localhost:8765/callback`
  - Scopes de lectura marcados (recovery, cycles, sleep, workout, profile, body_measurement)
  - Su **Client ID** y **Client Secret**

## Instalación (una vez)
```bash
cd tid-max/software
python -m venv .venv && source .venv/bin/activate   # opcional pero recomendado
pip install -r requirements.txt
cp .env.example .env
```
Abre `.env` y pega tu **Client ID** y **Client Secret** (el Refresh Token se llena solo en el paso 1).

## Paso 1 — Autorizar (una sola vez)
```bash
python whoop_auth.py
```
Se abre el navegador → inicia sesión con la cuenta de WHOOP de **Gael** → **Autorizar**.
Al terminar, el **Refresh Token** queda guardado en `.env`. No hay que repetirlo (salvo que se revoque).

## Paso 2 — Descargar datos (cuantas veces quieras)
```bash
python whoop_sync.py
```
Renueva el acceso, descarga todo y deja el JSON crudo en `./datos/`, con un resumen en pantalla:
```
Atleta:            Gael ...
Recovery reciente: 68 %
HRV (rMSSD):       74 ms
FC en reposo:      52 lpm
Sueno (rendim.):   88 %
Strain del dia:    12.4
Workouts jalados:  8
```

## Paso 3 — Dashboard en Excel (opcional, estético)
```bash
python whoop_dashboard.py
open TID-MAX-WHOOP.xlsx        # en Mac
```
Toma el JSON de `datos/` y genera `TID-MAX-WHOOP.xlsx` con:
- **Dashboard**: tarjetas KPI (recovery, HRV, FC reposo, sueño, strain) con color por zona
  (verde/amarillo/rojo) y gráficas de tendencia de recovery y HRV.
- Hojas de detalle: **Recovery, Sueño, Strain, Workouts** con formato y escala de color.

### Natación (volumen real) — porque WHOOP no lo mide
WHOOP **no mide la distancia de nado** (sin GPS en alberca / no cuenta vueltas). Para ver el
volumen real, crea un registro manual:
```bash
cp registro-natacion.ejemplo.csv datos/registro-natacion.csv
```
Edita `datos/registro-natacion.csv` (ábrelo en Excel) con una fila por día:
`fecha, km_natacion, sesiones_nado, min_pesas, notas`.
Al correr `whoop_dashboard.py`, el panel muestra la banda **NATACIÓN** (km real, sesiones, pesas),
una hoja **Natación** con gráfica de km/día, y marca el Km de WHOOP como *no confiable*.
Ver la oportunidad de producto en `../analisis/oportunidades-producto.md` (OPP-01).

## Seguridad
- El `.env` y la carpeta `datos/` están en `.gitignore` — **no se suben** al repo.
- El **Client Secret** y el **Refresh Token** son como contraseñas: no los pegues en chats ni capturas.

## Notas técnicas
- OAuth 2.0 (authorization code) contra `https://api.prod.whoop.com`.
- WHOOP **rota el refresh token** en cada renovación; `whoop_sync.py` lo re-guarda solo.
- Endpoints API **v2** (`/developer/v2/...`). La v1 fue deprecada en 2025.
- Límite de la app en modo desarrollo: hasta 10 usuarios WHOOP (suficiente para la prueba).
