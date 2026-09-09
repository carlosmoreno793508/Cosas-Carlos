# Arquitectura y tecnología (backend) — GrowProkure

> Resumen del stack técnico. Filosofía: **no construir SaaS antes de validar.** Hoy = prototipo estático. Después = app real cuando haya 10–20 clientes y datos. Este documento describe las 3 etapas para que tengas el panorama completo.

---

## Etapa 0 — HOY (prototipo, sin backend)

Lo que ya existe. Cero costo, cero servidores.

| Componente | Tecnología | Notas |
|---|---|---|
| Prototipo landing/dashboard | **HTML + CSS + JavaScript** (un archivo) | `05-Recursos/prototipo/index.html`. Localizado ES/EN. |
| Localización (i18n) | JS + cookie + `navigator.language` | Sin librerías, sin backend. |
| Hosting (cuando toque) | **Vercel / Netlify / GitHub Pages** | Estático = gratis. |
| "Base de datos" inicial | **Google Sheets / Airtable** | Suficiente para el piloto. Ver `01-data-layer-esquema.md`. |
| Operación de correo | **Instantly.ai** (SaaS externo) | No lo construimos, lo usamos. |

---

## Etapa 1 — MVP de plataforma (cuando haya tracción)

App real con login para que los clientes vean su tablero de señales. Stack recomendado, moderno y económico:

| Capa | Tecnología recomendada | Por qué |
|---|---|---|
| **Frontend** | **Next.js (React)** + TypeScript + Tailwind | Rápido, SEO, un solo framework para web y dashboard. |
| **Backend / API** | **Next.js API routes** o **Node.js (NestJS)** | Menos piezas; mismo lenguaje que el front. |
| **Base de datos** | **PostgreSQL** (via **Supabase** o **Neon**) | Relacional, encaja con el esquema de `01-data-layer`. Supabase da auth + API gratis al inicio. |
| **Auth** | **Supabase Auth** o **Clerk** | Login de clientes sin construirlo desde cero. |
| **ORM** | **Prisma** | Modela empresas/contactos/señales con tipado. |
| **Hosting** | **Vercel** (front+API) + **Supabase** (DB) | Escala solo; costo bajo al arranque. |
| **Archivos/PDF** (reportes) | **Supabase Storage** o S3 | Reportes mensuales de inteligencia. |

> Nota AWS: si en el futuro prefieres AWS, el equivalente es **RDS (Postgres) + Lambda/ECS + Amplify/CloudFront + Cognito (auth) + S3**. Más potente pero más complejo; para el MVP, Vercel + Supabase es más rápido y barato.

---

## Etapa 2 — El motor de inteligencia (la parte de IA)

Lo que hace único a GrowProkure: convertir datos crudos en señales priorizadas.

| Componente | Tecnología | Función |
|---|---|---|
| **Ingesta de datos** | Jobs programados (**cron** en Vercel / **Supabase Edge Functions**) | Jalan datos de las APIs (abajo). |
| **Fuentes de datos B2B** | **ZoomInfo API, Apollo API, Wiza API** | Empresas, contactos, scoops, intent, job postings. Ya conectadas vía MCP. |
| **Enriquecimiento** | Wiza / Apollo | Correos verificados, datos de contacto. |
| **Motor de señales** | Reglas + **LLM (Claude API)** | Clasifica noticias/eventos en tipos de señal (EOL, expansión…) y asigna score de prioridad. |
| **Scoring** | Lógica propia + embeddings | Prioriza oportunidades (el "92, 88, 74…" del tablero). |
| **Automatización de outreach** | **Instantly API** | Empuja los contactos priorizados a campañas. |
| **Orquestación IA** | **Claude (Anthropic API)** | Redacción de copy personalizado, resúmenes de cuenta, reportes. |

### Flujo de datos (end-to-end)
```
APIs (ZoomInfo/Apollo/Wiza) ─► Ingesta (cron) ─► Postgres
                                                   │
                          Motor de señales (reglas + Claude) ─► score
                                                   │
                              Dashboard (Next.js)  +  Instantly (campañas)
```

---

## Seguridad y cumplimiento

- **Datos B2B** bajo términos de ZoomInfo/Apollo/Wiza: solo investigación legítima, sin scraping masivo, base legal de interés legítimo, cumplimiento CAN-SPAM / privacidad.
- **Secrets/API keys** en variables de entorno (Vercel/Supabase), nunca en el repo.
- **Backups** automáticos de Postgres (Supabase/Neon los dan).

---

## Resumen de decisión

- **Ahora:** HTML estático + Google Sheets + Instantly. No construir más.
- **MVP (con clientes):** Next.js + Supabase (Postgres) + Prisma + Vercel.
- **IA:** Claude API + APIs de datos (ZoomInfo/Apollo/Wiza) + Instantly API.
- **AWS:** opcional a futuro; no necesario para arrancar.

> Regla: cada pieza que no aporte al piloto, se pospone. La tecnología sigue al negocio, no al revés.
