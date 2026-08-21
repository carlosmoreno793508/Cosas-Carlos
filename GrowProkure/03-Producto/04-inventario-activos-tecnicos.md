# Inventario de activos técnicos (existentes)

> Consolidación de "toda la información": aplicaciones y herramientas que YA existen en los repos de Carlos y que son relevantes para GrowProkure. Se documentan aquí aunque el código viva en otro repo.

---

## 1. Astute Buscador de Componentes (app funcional)

**Qué es:** una app web real y desplegada para **búsqueda de precios de componentes electrónicos**. Encaja directo en el vertical Electrónica — es potencial **lead magnet** y pieza de la Capa 4 (Plataforma).

- **Repo:** `carlosmoreno793508/Astute`
- **Rama del app:** `claude/component-price-lookup-kknxym` (la rama `main` solo tiene un README placeholder)
- **PR de localización:** Astute #5 (borrador), rama `claude/smt-specialist-job-study-jesh1p`

### Stack técnico
| Capa | Tecnología |
|---|---|
| Frontend | `index.html` + `app.js` + `styles.css` (vanilla JS, sin framework) + `astute-buscador.html` (copia standalone) |
| Backend | `server.py` — **Python stdlib** (`ThreadingHTTPServer` + `urllib` + `json`), sin dependencias |
| Endpoints | `/api/health`, `/api/search`, estáticos |
| Proveedores de precios | Patrón pluggable: **Mouser, DigiKey, Nexar/Octopart, Z2Data**, demo, auto |
| Deploy | GitHub Pages (`.github/workflows/pages.yml`, manual) |
| Estado | Stateless (sin base de datos) |
| i18n | ES/EN (default por navegador + cookie + switch en footer) — ya implementado |

### Cómo encaja en GrowProkure
- **Capa 3/4:** herramienta de valor para compradores (buscar precios/segunda fuente) → gancho para el lado demanda.
- **Lead magnet:** "busca tu componente" gratis → captura contactos de procurement.
- **Reutilizable:** el backend Python/FastAPI de la propuesta de arquitectura puede absorber este buscador.

---

## 2. Estudios de mercado (ver índices en 02-Investigacion)

| Estudio | Repo | Índice en GrowProkure |
|---|---|---|
| Electrónica MX/USA | `Astute` | `02-Investigacion/electronica/estudio-astute-indice.md` |
| Foil (plásticos) | `tid` | `02-Investigacion/plasticos/estudio-foil-indice.md` |

---

## 3. Otros repos/sesiones detectados (por clasificar)

De la lista de sesiones de Carlos, posiblemente relevantes:
- "Electronic components search tool" / "Electronic component price lookup tool" → probablemente el Buscador de arriba.
- "Electronic component weights" → ¿datos de componentes?
- `tid` → "Pagina Web" (HTML estático), scripts Python, estudio Foil.
- No relacionados con GrowProkure: Natacion, Swimcloud, Crypto trading, Spotify, TV app, NCSA/reclutamiento, Gael.

> Pendiente: cuando Carlos pegue/comparta los resúmenes, se integran los datos de mercado reales. Este inventario centraliza el "dónde está cada cosa".
