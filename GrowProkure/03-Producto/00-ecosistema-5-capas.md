# GrowProkure — Ecosistema de 5 capas (mapa maestro)

> Construimos las 5 capas **en paralelo**, no en secuencia de años. Cada capa tiene un MVP que arranca ya. Este documento es el mapa; cada capa apunta a su entregable concreto.

**GrowProkure — Industrial Growth Intelligence.** Motor de inteligencia y oportunidades para la cadena de suministro industrial (Electrónica + Plásticos/decoración), que sirve a proveedores y compradores.

---

## Capa 1 — DATOS (el activo defensible)

Base de datos industrial propia de dos lados.

- **MVP ahora:** esquema de base de datos + primeras listas de cuentas objetivo (ver `03-Producto/01-data-layer-esquema.md` y `04-GoToMarket/06-icp-y-cuentas-objetivo.md`).
- **Fuente:** ZoomInfo + Apollo + Wiza (ya conectados) + estudios Astute y Foil.
- **Meta:** 500 empresas / 5,000 contactos año 1 → 100,000.

## Capa 2 — INTELIGENCIA (motor de señales)

IA que detecta oportunidades: expansiones, nuevas plantas, RFQs, EOL, fusiones, aranceles, riesgo de suministro.

- **MVP ahora:** framework de señales + catálogo de disparadores por vertical (ver `03-Producto/02-motor-de-senales.md`).
- **Automatización:** enriquecimiento con las APIs conectadas; alertas.

## Capa 3 — SERVICIOS (lo que factura ya)

Generación de oportunidades vía la máquina de cold email + inteligencia.

- **MVP ahora:** oferta + secuencias de correo + operación (piloto Astute).
- **Entregables:** ver `04-GoToMarket/` (copy, plan, tracking).

## Capa 4 — PLATAFORMA (dashboard)

Visualización para clientes: cuentas objetivo, oportunidades, competencia, compradores, riesgo.

- **MVP ahora:** prototipo de landing + dashboard (ver `05-Recursos/prototipo/`). Se construye en HTML primero, sin backend, para validar la experiencia.
- **Después:** app real cuando haya 10–20 clientes y datos históricos.

## Capa 5 — COMUNIDAD (retención + datos)

Red privada "Industrial Intelligence Network": buyers, procurement, supply chain.

- **MVP ahora:** calendario de contenido LinkedIn + estructura de comunidad (ver `04-GoToMarket/08-calendario-contenido.md`).
- **Formato:** 1 webinar/mes + 1 reporte/mes + networking trimestral.

---

## Cómo se conecta todo (flujo)

```
DATOS ──► INTELIGENCIA ──► SERVICIOS ──► factura (proveedores)
  ▲            │                │
  │            ▼                ▼
COMUNIDAD ◄── PLATAFORMA ◄── oportunidades/reuniones
  (compradores alimentan datos; el efecto de red crece)
```

## Estado de construcción (checklist vivo)

- [x] Concepto, fusión, verticales, nombre (GrowProkure)
- [x] Cliente cero (Astute) definido
- [x] Capa 1: esquema de datos (`01-data-layer-esquema.md`) + ICP + listas objetivo (`04-GoToMarket/06`)
- [x] Capa 2: framework de señales (`02-motor-de-senales.md`)
- [x] Capa 3: oferta + copy (`04-GoToMarket/04`) + plan 30-60-90 (`03`) + tracking (`07`)
- [x] Capa 4: prototipo landing/dashboard (`05-Recursos/prototipo/index.html`)
- [x] Capa 5: calendario de contenido + estructura comunidad (`04-GoToMarket/08`)
- [ ] Laboratorio técnico montado (dominios + warm-up) — depende de Carlos (guía lista en `04-GoToMarket/05`)
