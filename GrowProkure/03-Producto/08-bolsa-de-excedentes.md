# Bolsa de Excedentes (sobre-inventario) — el lado OFERTA del marketplace

> Idea de Carlos (2026-07-16): publicar listas de sobre-inventario a los socios / mandar correo para que lo consideren, y **meterlo como una fase del roadmap**. Es la otra mitad del marketplace (oferta), y el punto de arranque más fácil.

## En qué FASE entra (roadmap del marketplace)
La Bolsa de Excedentes se puede arrancar MUY temprano porque es fácil de sembrar. Se mapea a las fases del marketplace (`06-marketplace-rfq-vision.md`):

| Fase | Qué se hace con excedentes |
|---|---|
| **Fase 0 · Concierge (ahora)** | Los proveedores mandan su lista de excedente por correo → Prokure la normaliza → Carlos la reenvía a compradores relevantes de la base. 100% manual, valida demanda. |
| **Fase 1 · No-code** | Sección **"Bolsa de Excedentes"** en el Radar (newsletter) + correo dedicado a socios con los excedentes del mes. Formulario para que el proveedor suba su lista. |
| **Fase 2 · App ligera** | Tablero buscable "Se ofrece" junto al de "Se busca" (RFQs). Match automático excedente ↔ RFQ. |
| **Fase 3 · Plataforma** | Alertas en tiempo real, precios, reputación del proveedor, cierre de operación. |

> 👉 Arranca en **Fase 0/1** (correo + sección en el Radar) — no necesitas la app. Es el primer tablero real del marketplace porque la oferta es fácil de conseguir.

## Qué es
- **RFQ** = comprador dice "BUSCO X" → señal de **demanda**.
- **Excedente** = proveedor dice "TENGO X para mover" → señal de **oferta**.
- Juntos = marketplace de dos tableros: **"Se busca"** (RFQs) + **"Se ofrece"** (excedentes).

## Por qué es el mejor punto de arranque
Resuelve la mitad del problema de arranque en frío: los proveedores **quieren** compartir su excedente (es capital muerto que urge vender). No hay que convencerlos → se siembra el lado oferta rápido.

## Triple valor
- **Proveedor:** liquida E&O (excess & obsolete), recupera capital muerto.
- **Comprador:** encuentra partes difíciles/EOL o mejores precios → razón para suscribirse.
- **GrowProkure:** nueva base (activo), sección de newsletter, palanca de monetización, y material de match.

## Cómo entra al ecosistema
- **Base nueva "Excedentes"** (schema abajo), mantenida por **Prokure** (ingesta, normaliza, dedup, clasifica, cruza vs. demanda).
- **Distribución:** sección "Bolsa de Excedentes" en el Radar + **correo dedicado a socios** + (futuro) tablero buscable en la app.
- **Match:** cruzar excedentes vs. RFQs abiertos y vs. consumo conocido de compradores → "tienes comprador para esto".

## Esquema de la base (tabla Excedentes)
`MPN (part number) · Fabricante · Descripción · Cantidad · DateCode/Lote · Condición (nuevo/usado/refurb) · Empaque (MOQ/reel/tray) · Trazabilidad (franquiciado / mercado abierto) · PrecioObjetivo · Moneda · Ubicación · Proveedor · Vertical · FechaAlta · Vence · Notas · Fuente`

## Monetización
| Modelo | Quién paga |
|---|---|
| Gratis listar (sembrar oferta) + comprador paga acceso/alertas tempranas | Comprador |
| Listado destacado (aparecer primero) | Proveedor |
| Fee por match cerrado | El que cierra |
> Regla: el lado que recibe valor paga; el que crea el imán (excedente barato) va gratis/fácil.

## Cuidados (crítico en electrónica)
- **Falsificación/trazabilidad:** el mercado de excedentes tiene counterfeit. Capturar condición, date code, franquiciado vs. mercado abierto. Alinea con el ángulo anti-counterfeit (Astute).
- **Frescura:** el stock se mueve → manejar caducidad (Vence) de cada lista; no publicar lo ya vendido.
- **Cumplimiento:** solo listar lo que el proveedor tiene derecho a vender.

## Rol de Prokure
Ingesta de listas de excedente (Excel) igual que contactos: normaliza al schema, deduplica, valida, clasifica, y **cruza contra demanda/RFQs**. Reporta matches.

## Conexión al marketplace
Marketplace = 2 tableros: **SE BUSCA** (RFQs / demanda) + **SE OFRECE** (excedentes / oferta). El excedente es el más fácil de arrancar → buen primer tablero real.

> Estado: **idea aprobada (2026-07-16).** Siguiente: definir plantilla de captura de excedentes + sección en el Radar + tarea de ingesta/match en Prokure. Complementa `03-Producto/06-marketplace-rfq-vision.md`.
