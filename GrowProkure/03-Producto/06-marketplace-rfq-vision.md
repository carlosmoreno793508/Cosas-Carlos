# Visión — Marketplace de RFQs ("LinkedIn Industrial") — Capa 4 + 5 hechas producto

> Idea de Carlos (2026-07-16): una app tipo LinkedIn donde los **compradores suben RFQs abiertos** y los **proveedores** (electrónica / plásticos) reciben una **alerta para participar**. Ej.: *"Un EMS en Guadalajara subió un RFQ de electrónicos — participa."* Comunidad **funcional y monetizable**. Este documento la aterriza sin arriesgar de más.

## Qué es
Un **marketplace de RFQs de dos lados**, vertical (electrónica + plásticos/decoración). Es el endgame del modelo two-sided: fusiona **Capa 4 (Plataforma)** + **Capa 5 (Comunidad)** en un producto que factura y crea el foso definitivo.

## Por qué es fuerte
- **Efecto de red:** compradores atraen proveedores y viceversa; crece solo.
- **Moat / activo:** al pasar los RFQs por GrowProkure, somos dueños de la **señal de demanda** — el dato más defensible de la industria (Capa 1 + 2 realizadas).
- **Monetización natural:** los proveedores ya pagan por leads (Astute/TID). Aquí compran acceso a demanda real y caliente.

## El riesgo #1 — arranque en frío (chicken & egg)
- Compradores no suben RFQs sin proveedores buenos; proveedores no entran sin RFQs.
- **Específico de RFQs:** los grandes (Jabil, etc.) tienen sistemas de compras propios + NDAs. Exponer demanda es sensible.
- **Hay que validar ANTES de construir la app**, o queda vacía.

## La cuña (donde sí funciona)
Apuntar a donde la **velocidad > confidencialidad**:
- Cortos / shortages urgentes (= pitch actual de Astute)
- Segundas fuentes que se buscan rápido
- Partes difíciles / EOL
- Compradores medianos sin sistema de sourcing propio

**RFQs anónimos:** mostrar *"EMS Tier-1 en Guadalajara busca 10k pzs de [componente] — participa"* en vez del nombre. Se revela identidad solo al hacer match. Protege al comprador, engancha al proveedor.

## Clave: el cold email es el bootstrap, no un proyecto aparte
No se construye la app primero. El piloto actual (datos + máquina de correo) **es** cómo se arranca el marketplace.

```
FASE 0 — Concierge / manual (AHORA):
  Cuando un comprador diga "busco X" o "tengo un corto", Carlos alerta
  manualmente a proveedores de la base (1,276 contactos).
  Valida: ¿compradores comparten RFQs? ¿proveedores responden?
  (Hacer cosas que no escalan — así arrancaron los marketplaces.)

FASE 1 — No-code:
  Formulario (buyer sube RFQ) + alertas por correo/WhatsApp a proveedores
  de esa categoría. Airtable/Notion + Instantly. SIN app.

FASE 2 — App ligera:
  Feed tipo LinkedIn + alertas, con flujo de RFQs YA probado.

FASE 3 — Plataforma completa:
  Dashboard, matching automático, pagos, reputación.
```

## Monetización (modelo recomendado)
| Modelo | Quién paga | Nota |
|---|---|---|
| **Suscripción proveedor** ⭐ | Proveedor | Recibir/responder RFQs de su categoría. El mejor. |
| Pay-per-RFQ | Proveedor | Acceso por RFQ calificado |
| Destacado / ads | Proveedor | Aparecer primero |
| Compradores GRATIS | — | Imán de demanda |

**Regla de oro:** paga el lado que recibe valor (proveedores/leads); va gratis el lado que crea el imán (compradores/RFQs).

## Preguntas a validar (Fase 0)
1. ¿Los compradores están dispuestos a compartir un RFQ (aunque sea anónimo)?
2. ¿Qué % de proveedores responde a una alerta de RFQ?
3. ¿Qué categorías/segmentos generan más RFQs (electrónica cortos vs. plásticos)?
4. ¿Cuánto pagaría un proveedor por acceso a RFQs calificados?
5. Confidencialidad: ¿el anonimato resuelve la objeción del comprador?

## Cómo se conecta al plan
- Es la evolución de Capa 4 + 5. **No cambia** el piloto actual (Astute/TID cold email); lo aprovecha.
- Se construye por fases; la app real solo cuando los RFQs ya fluyan (evita construir software en vacío).

## Competencia / referencias (a estudiar)
- Xometry, Fictiv (manufactura on-demand), Thomasnet (directorio+RFQ), Scoutbee/Keelvar (sourcing IA), Octopart/SourcENGINE (partes electrónicas). Ninguno es un "feed de RFQs con alertas" enfocado a MX electrónica+plásticos → hueco.

---

> Estado: **visión aprobada como dirección de largo plazo (2026-07-16).** Arranque = Fase 0 concierge, en paralelo al piloto de cold email. Revisar métricas de Fase 0 antes de invertir en app.
