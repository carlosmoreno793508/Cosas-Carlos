# Prompt Maestro — Astute Market & Sales Intelligence Engine (V2)

> Especificación del motor de inteligencia comercial de Astute. Convierte los estudios crudos + CRM en un sistema accionable: Master Company DB, scoring de oportunidad, Top 100 / Top 25, ABM y plan 30/60/90. Filosofía: **datos → inteligencia → oportunidad → acción → ventas**. Precisión y utilidad comercial sobre volumen. **Nunca inventar** (UNKNOWN / INFERRED / SOURCED).

## Inputs
- Estudio Electrónica México (Directorio, Contactos, Compras y Sourcing, Evidencia Importación)
- US Electronics SMT Study (Directory, Contacts, Purchasing & Sourcing, Import Evidence)
- LATAM + Caribe (Directorio Empresas, Hubs, Contactos, Metodología)
- **CRM Clientes Tsunami** (4,659 clientes — para separar cliente existente vs. prospecto)

## Herramientas de enriquecimiento (fase externa, selectiva — R10)
- **ZoomInfo** — verificar contactos, compras/commodity managers, señales de empresa.
- **Wiza** — enriquecer email/teléfono + historial laboral (movimientos de personas).
- **Apollo** — enriquecer/verificar contacto y empresa.
- ImportYeti / Panjiva — evidencia de importación (supply chain).
- Uso **acotado por ICP, sin extracción masiva ni reventa** (dentro de términos de cada tool).

## Áreas comerciales de Astute (distribuidor independiente)
Cost Savings · Shortages · Excess Inventory · EOL/LTB · MRO · Hard-to-find · Obsolescence · Supply Chain support · Alternative sourcing · Franchise/authorized · Broker sourcing · Consignment.
> Regla: una línea SMT NO basta. Debe existir **hipótesis razonable de necesidad de componentes** que Astute pueda surtir.

## Metodología del score (build automatizado)
- **Master Company ID:** nombre normalizado (minúsculas, sin sufijos legales/geográficos); merge por clave; aliases conservados; no fusionar por parecido dudoso.
- **SMT Evidence Score (0-5):** derivado de Confianza + Evidencia del directorio (5=Alta+evidencia SMT/PCBA … 0=nada). No verificado en planta.
- **Opportunity Score (0-100):** manufacturing + SMT(15) + intensidad de componentes(industria) + complejidad de compras(#contactos) + supply-chain pain + escala + atractivo de industria + import(5) + EOL(5) + disponibilidad de contacto(5). Es **priorización**, no un hecho.
- **Tsunami match:** exacto (HIGH) / contención de nombre (POSSIBLE, revisar a mano). Clasifica EXISTING CUSTOMER / EXISTING (posible) / PROSPECT.
- **Contact priority:** A (decisor compras) · B (influencer/ejecutivo) · C (ingeniería/calidad) · D (baja).
- **Oportunidad por cuenta:** INFERRED a partir de industria/import (no verificada).

## Calibración pendiente (v2 — decisiones a revisar)
- ⚠️ **Fabricantes de semiconductores** (TSMC, Qorvo, Analog Devices, MACOM, Qualcomm) salen alto por "industria semiconductor", pero son **fabricantes de componentes, no compradores** típicos de un distribuidor. Revisar si son fit real (posible sólo para MRO/excedentes) o falso positivo → bajar peso.
- ⚠️ **373 "EXISTING (posible)"** requieren revisión manual antes de excluir del ranking de prospectos.
- Compras centralizadas (global) vs. local: marcar decisor real (LOCAL/REGIONAL/GLOBAL) — pendiente enriquecer.

## Output (Excel: `Astute_Intelligence_Engine.xlsx`)
1. **Master Company DB** — todas las empresas normalizadas + score + tier + Tsunami + contacto primario.
2. **Top 100 Prospectos** — mayor probabilidad de negocio (no los más grandes).
3. **Top 25 Atacar Ya** — prospecto + contacto de compras con email + hipótesis de oportunidad.
4. **Tsunami – Cuentas Existentes** — cross-sell / nueva planta / nuevo comprador.
5. **Metodología y Calidad** — trazabilidad y confianza.

## Fases
1. Auditoría ✅ · 2. Normalización ✅ · 3. Dedup + Tsunami ✅ · 4. SMT validation ✅ · 5. Score ✅ · 6. Top 100/25 ✅ · **7. Enriquecimiento externo (ZoomInfo/Wiza) del Top 25** ⏳ · 8. Sales triggers en vivo ⏳ · 9. ABM + 30/60/90 ⏳ · 10. Fact-check final ⏳

> Estado: **Build v1 generado (2026-08-27)** sobre datos reales. Núcleo listo; falta capa externa (triggers en vivo, verificación de email, plant-level) — selectiva en Top 25.
