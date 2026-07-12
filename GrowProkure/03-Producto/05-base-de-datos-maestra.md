# Base de datos maestra (Capa 1) — consolidación de estudios

> **Propósito (Carlos):** todos los estudios de mercado que subimos son la materia prima para construir NUESTRA base de datos — el activo defensible de GrowProkure. Este documento registra cada fuente y cómo se consolida en una sola base de dos lados (oferta + demanda), por vertical.

## Qué alimenta la base de datos

| Fuente (estudio) | Vertical | Empresas | Contactos | Con email | Notas |
|---|---|---|---|---|---|
| Estudio Electrónica **México** | Electrónica | **211** | **333** | sí | `Estudio_Electronica_Mexico.xlsx` (repo Astute) |
| Estudio Electrónica **USA (SMT)** | Electrónica | **148** | **63** | sí (ZoomInfo) | `US_Electronics_SMT_Study.xlsx` |
| Estudio **Foil / Tintas (TID)** | Plásticos-decoración | 120 (prospección) + 378 (KURZ) | **120** | **63** | Repo `tid`, 10 docs + PDF |
| **TOTALES (aprox.)** | 2 verticales | **~850+** | **~500+** | ~130+ | Crece con cada campaña |

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
