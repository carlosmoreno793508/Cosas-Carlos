# Base de datos maestra (Capa 1) — consolidación de estudios

> **Propósito (Carlos):** todos los estudios de mercado que subimos son la materia prima para construir NUESTRA base de datos — el activo defensible de GrowProkure. Este documento registra cada fuente y cómo se consolida en una sola base de dos lados (oferta + demanda), por vertical.

## Qué alimenta la base de datos (CIFRAS REALES — archivos verificados 2026-07-12)

> Archivos ya versionados en `02-Investigacion/`. Conteos verificados leyendo los Excel.

| Fuente (estudio) | Vertical | Empresas | Contactos | Con email | Archivo |
|---|---|---|---|---|---|
| Estudio Electrónica **México** | Electrónica | **244** | **738** | **666** | `electronica/Estudio_Electronica_Mexico.xlsx` |
| Estudio Electrónica **USA (SMT)** | Electrónica | **207** | **408** | **401** | `electronica/US_Electronics_SMT_Study.xlsx` |
| **Foil / Tintas (TID)** | Plásticos-decoración | **46** | **191** | **93** | `plasticos/Contactos_Foil_TID_Global.xlsx` |
| **TOTALES** | 2 verticales | **~497** | **1,337** | **1,160** | (crece con cada campaña) |

> 📈 **La base ya es grande:** ~1,337 contactos, de los cuales **1,160 tienen email** — lista para operar campañas de inmediato.

### Detalle por estudio

**Electrónica México (244 empresas / 738 contactos / 666 emails):**
- Top estados: Baja California 37, Chihuahua 33, Querétaro 27, Nuevo León 24, Tamaulipas 24, Coahuila 21, Guanajuato 14, SLP 13.
- Hojas: Directorio, Contactos, Compras y Sourcing (567), Evidencia Importación (218), Notas.

**Electrónica USA-SMT (207 empresas / 408 contactos / 401 emails):**
- Top estados: CA 52, MI 19, TX 14, AZ 12, MA 12, IL 11, FL 8, WI 8.
- Hojas: Directory, Contacts, Purchasing & Sourcing (255), Import Evidence (196), Notes.
- Incluye columna "SMT Lines (Qty)" y evidencia de importación por empresa.

**Foil/Tintas TID (46 empresas / 191 contactos / 93 emails):**
- Base de prospección (Wiza+Apollo+ZoomInfo): 35 empresas, 120 contactos, 63 email, **20 en Bajío**.
- **5 segmentos confirmados:** Plásticos 74 · Gráficos 17 · Cosméticos 16 · Seguridad 4 · Decorado 9.
- Agenda propia (iPhone, validada): 71 contactos, 30 email, 61 teléfono, **19 vigentes**.

> ⚠️ **Importante:** el estudio de Foil **aplica igual a tintas** (tampografía / serigrafía) — es el mismo mercado de decoración sobre plástico, mismos compradores. La base trata "foil + tintas" como un solo vertical.

## Modelo de dos lados en la base

Cada empresa/contacto se clasifica por **lado** (el diferenciador de GrowProkure):

| Vertical | Lado OFERTA (proveedores) | Lado DEMANDA (compradores) |
|---|---|---|
| **Electrónica** | Distribuidores/EMS (Astute, TTI, Arrow…) | OEMs/EMS que compran componentes (las 359 empresas US+MX) |
| **Plásticos (foil+tintas)** | Casas de decoración (TID) | Fabricantes de piezas plásticas (Guala, Hella, P&G, Mabe, Whirlpool…) |

## Esquema (ver `01-data-layer-esquema.md`)

Las 4 tablas ya definidas absorben todos los estudios:
- **`empresas`** ← directorios (Region, Company, Type, City, State, Sector, Confidence, Website, Source) de MX + US + foil.
- **`contactos`** ← hojas de contactos (nombre, título, rol, email, teléfono, accuracy).
- **`senales`** ← importaciones (HS codes), vacantes SMT, KURZ buyers, importaciones SAT (foil).
- **`campanas`/`reuniones`** ← se llenan al operar.

> Campos extra útiles ya presentes en los estudios: `confidence` (High/Medium), `smt_pcba_evidence`, `likely_location`, `source`. Se mapean directo al esquema.

## Plan para construir la base (pasos)

1. **Reunir los archivos fuente** en `02-Investigacion/` (los 2 .xlsx de electrónica + los 10 docs de foil/tid). ← pendiente de subir/copiar.
2. **Normalizar** a las 4 tablas del esquema (un solo formato, sin importar de qué estudio venga).
3. **Deduplicar** (empresas repetidas entre estudios; ej. Whirlpool/Mabe aparecen en electrónica y en foil).
4. **Clasificar lado** (oferta/demanda) y **vertical** cada registro.
5. **Cargar señales** (HS codes de importación, KURZ, vacantes).
6. **Conectar** al tracking de campañas (`04-GoToMarket/07-plantilla-tracking.csv`).

## Dónde vive la base

- **Ahora (MVP):** Google Sheets / Airtable con las 4 pestañas (rápido, editable).
- **Después:** PostgreSQL (Supabase) — ver `03-arquitectura-backend.md`.

## Fuentes de crecimiento continuo (la base se auto-alimenta)

- ZoomInfo / Apollo / Wiza (enriquecimiento)
- Trade-data por HS code (nuevos importadores = nuevos compradores)
- Importaciones SAT (México)
- Cada respuesta/reunión de campaña
- Estudios futuros (nuevos verticales o regiones)

## Pendiente

- [ ] Subir/copiar los archivos fuente a `02-Investigacion/`.
- [ ] Construir el Sheet/Airtable maestro con las 4 pestañas.
- [ ] Cargar y deduplicar los ~850 registros iniciales.
