# Guía de lanzamiento en Instantly (para novato)

> Cómo lanzar o programar la campaña de cold email. Aplica igual para Astute y TID (cambiando lista y buzones).

## Archivos listos para subir
- `Astute_Tier1_Clave_Instantly.csv` — 63 clave (arrancar con estos)
- `Astute_Instantly_LISTO.csv` — 1,651 completos, ordenados (clave primero)
- (TID) `TID_Tanda1_contactos.xlsx` — 125, Tier A primero

## Paso a paso

### 1. Crear campaña
- app.instantly.ai → **Campaigns** → **+ New Campaign** → nombre `Astute — Tanda 1`.

### 2. Subir leads
- Pestaña **Leads** → **Upload CSV** → subir el CSV.
- Mapear: `email`→Email · `first_name`→First Name · `company_name`→Company Name.

### 3. Secuencia (4 correos)
- **Step 1 (Día 0):** Subject `{{companyName}} — cortos y segundas fuentes` + Email 1.
- **+ Add step:** esperar **3 días** → Email 2.
- **+ step:** esperar **4 días** (día 7) → Email 3.
- **+ step:** esperar **5 días** (día 12) → Email 4.
- Variables de Instantly: `{{firstName}}` y `{{companyName}}`.

### 4. Buzones
- **Options/Accounts** → seleccionar los 7 buzones de Astute (rotación).

### 5. Configuración (deliverability)
- Daily limit: **10-15 por buzón** al inicio, subir gradual.
- Horario: **L-V, 9:00-17:00, America/Mexico_City**.
- **Stop on reply: ON.**
- **Open tracking / Link tracking: OFF.**
- Warmup: dejar **PRENDIDO** (sigue en paralelo).

### 6. Lanzar o programar
- **Launch** (arriba derecha). Para programar: fijar fecha/hora de inicio antes de Launch.

### 7. Monitorear
- **Unibox** → todas las respuestas. Clasificar: auto-reply (ignorar) · real (responder con pitch) · opt-out (quitar).

## Orden de envío recomendado
Tier 1 (clave) → Tier 2 (decisor) → Tier 3 (comprador) → Tier 4 (directorio). Subir Tier 1 primero; agregar los demás conforme avanza.

## Reglas de oro
- Enviar SOLO desde los dominios secundarios (get-astute/astute-supply/get-tid/try-tid). NUNCA desde el correo de trabajo (astutegroup.com/tidmexico.com.mx) ni growprokure.com.
- Warmup 14 días cumplidos antes de enviar.
- Volumen bajo al inicio; subir gradual.
