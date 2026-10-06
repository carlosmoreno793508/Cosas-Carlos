# Guía 06 — intervals.icu: el pipe GRATIS para el Polar de Carlos (adiós TCX manual)

**Por qué:** intervals.icu es un agregador **gratis** que, con UNA API key, trae tus datos de
**Polar Flow** (y Garmin/Strava/COROS/Oura si algún día los conectas). Reemplaza el export manual
de TCX y evita Junction ($/mes) para fuentes que no son WHOOP.

El código ya está: `software/intervals_sync.py` (baja actividades + wellness y los mapea al formato
del pipeline) y `tid_multi.py` ya reconoce la fuente `intervals`.

---

## Parte A — Conectar tu Polar en intervals.icu (una sola vez)

1. Crea cuenta GRATIS en **https://intervals.icu** y **confirma tu email** (el bloque de
   *Developer Settings* no aparece hasta confirmar).
2. En **Settings**, conecta tu fuente: **Polar Flow** (autoriza con tu cuenta Polar). A partir de
   ahí, cada entreno que grabes con la app Polar llega solo a intervals.icu.
3. En **Settings → Developer** (hasta el fondo; en celular ponlo horizontal o el botón Generate se
   corta): copia tu **Athlete ID** y genera tu **API Key**. Trátala como contraseña.

## Parte B — Darme la llave (sin pegarla en el chat)

🔒 La API key va **directo a un secreto**, nunca al chat:
- **Para pruebas locales (Mac):** ponla en `software/.env` como
  `INTERVALS_API_KEY=tu_key` (y opcional `INTERVALS_ATHLETE_ID=0`).
- **Para la nube (GitHub Actions):** repo → Settings → Secrets and variables → Actions →
  **New repository secret** → nombre `INTERVALS_API_KEY`, valor = tu key.

> El usuario de auth es el **texto literal `API_KEY`** y tu key va de *password* — el script ya lo
> maneja; solo necesito la key en el secreto.

## Parte C — Cambiar tu fuente a `intervals` (lo hago yo cuando confirmes)

En `software/atletas.json`, tu entrada pasa de `"fuente": "agregador"` a:

```json
{ "slug": "carlos-moreno", "nombre": "Carlos Moreno", "deporte": "running",
  "reloj": "Polar", "fuente": "intervals", "perfil": "perfil-carlos.json", "activo": true }
```

**Avísame cuando tengas (1) el Polar conectado en intervals.icu y (2) la API key en el secreto**, y
yo: cambio tu fuente, disparo un run y valido que tus corridas + wellness entren al reporte. En ese
primer run reviso el crudo (`intervals_raw_*.json`) por si hay que afinar algún nombre de campo.

---

## Qué ganas
- **Cero export manual de TCX** — tus entrenos de Polar fluyen solos al reporte.
- **$0** — plan gratis de intervals.icu; sin Junction.
- Base para sumar Garmin/Oura/COROS en el futuro con la misma llave.

> Nota: WHOOP por intervals.icu **sí** pide membresía WHOOP. Para WHOOP gratis (Gael) la vía es
> **NOOP (BLE)**, aparte.
