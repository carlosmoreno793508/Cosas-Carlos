# Motor de enriquecimiento — orquestar Wiza/Apollo/ZoomInfo (no clonar)

> Idea de Carlos (2026-07-16): Wiza saca de LinkedIn nombre/puesto/empresa/historial + enriquece email/teléfono. ¿Implementar algo similar? Respuesta: NO construir un scraper propio — orquestar las herramientas licenciadas que ya tenemos y agregar la capa de inteligencia.

## Lo más valioso: el HISTORIAL LABORAL
El work history (ej. Jorge Albor: GM 2011→hoy, antes Continental) es oro porque:
- **Cambio de empresa** = señal de venta + actualización de base (resuelve el problema tipo Homero Ruiz a escala).
- **Commodity/rol histórico** ("Wire Harnesses & Electronic Components") = segmentación ultra-precisa.
- Alimenta la sección "movimientos de personas" del Radar.

## Por qué NO clonar Wiza
1. Scrapear LinkedIn va contra sus términos → riesgo legal real (LinkedIn litiga scraping).
2. Técnicamente frágil (LinkedIn rompe scrapers seguido).
3. Ya resuelto: Wiza, Apollo, ZoomInfo conectados en la sesión, con licencia.

## La jugada: orquestar + capa de inteligencia
```
Wiza / Apollo / ZoomInfo  (motor de datos licenciado)
        ↓  Prokure orquesta (llamadas API)
GrowProkure agrega:  scoring · señales · match RFQ↔excedente · rastreo de movimientos de personas
        ↓
Base propia + Radar + marketplace
```
Diferenciador = qué haces con el dato (priorizar, cruzar, alertar), no extraerlo.

## Flujo del motor (lo que hará Prokure)
1. **Input:** empresa objetivo + rol (del ICP) — ej. "Compras/Ingeniería en EMS del Bajío".
2. **Enriquecer:** llamar a la herramienta conectada (Apollo/ZoomInfo/Wiza) → contactos + puesto + **historial** + email/tel.
3. **Normalizar** al esquema de la base (R1).
4. **Deduplicar** contra la Base Maestra (R2) por email y contacto+empresa.
5. **Clasificar:** vertical / lado / segmento / prioridad (R4) + **detectar movimientos** (empresa actual ≠ empresa en base → señal).
6. **Integrar** solo lo nuevo; conservar procedencia (R5).
7. **Reportar:** nuevos / duplicados / movimientos detectados.

## Cumplimiento (crítico)
- Usar las herramientas **dentro de sus términos**: investigación B2B legítima, **sin extracción masiva** ni reventa (lo prohíben ZoomInfo/Apollo/Wiza explícitamente).
- Base legal de interés legítimo B2B (R9). No scraping propio de LinkedIn.
- Consumir créditos con criterio (búsquedas acotadas por ICP, no barridos).

## Casos de uso inmediatos
- **Roster de proveedores (Oferta)** — llenar el lado vacío de la base.
- **Profundizar compradores** — sumar Ingeniería/Producción a cuentas existentes.
- **Rastreo de movimientos** — refrescar contactos que cambiaron de empresa (Radar + higiene).
- **Enriquecer un contacto** antes de una campaña (email/tel verificados).

> Estado: **diseño aprobado (2026-07-16).** GrowProkure orquesta herramientas licenciadas + capa de inteligencia; no construye scraper. Ejecuta Prokure con búsquedas acotadas por ICP.
