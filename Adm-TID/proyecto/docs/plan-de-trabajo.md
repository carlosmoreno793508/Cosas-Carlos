# Plan de trabajo — Proyecto (sistema de ventas con IA, vertical industrial)

**Ámbito:** Proyecto
**Fecha:** 2026-07-18
**Base:** expediente competitivo (Zolutium, LeadSales) + experiencia de Carlos en manufactura/maquila/nearshoring.

> Documento vivo. El agente `adm-tid` lo mantiene junto con `reglas.md` y `pendientes.md`.

---

## 0. La tesis en una frase

> **Mientras Zolutium y LeadSales venden "IA para cualquier negocio", nosotros vendemos el sistema de ventas con IA hecho para la industria de manufactura/maquila de México y LATAM — con leads de compradores reales (OEM/EMS/Tier 1), no citas genéricas.**

**Por qué ganamos:** ningún competidor toca el vertical industrial. Nuestro foso es el conocimiento del negocio (compradores, RFQs, supply chain, nearshoring), no "más IA".

---

## 1. Decisiones que dependen de ti (bloquean el diseño)

Antes de construir, hay que cerrar 3 definiciones. Todo lo demás se deriva de aquí:

| # | Decisión | Opciones | Por qué importa |
|---|----------|----------|-----------------|
| **D1** | **Modelo de negocio** | (a) SaaS: vendemos el software por suscripción · (b) Servicio: entregamos leads/citas cualificadas · (c) Híbrido | Cambia el precio, el pitch y qué construimos primero |
| **D2** | **Cómo lo construimos** | (a) Sobre plataforma existente (GoHighLevel u similar, rápido y barato) · (b) A medida (más control, más caro/lento) · (c) Híbrido: plataforma + capa propia de inteligencia industrial | Define tiempo y costo del MVP |
| **D3** | **Cliente objetivo del MVP** | ¿Le vendemos a fabricantes/maquilas que quieren vender más? ¿O a distribuidores de componentes? ¿O usamos el sistema para TU propia prospección primero? | Enfoca el primer caso de uso |

👉 **Recomendación inicial:** D1→(c) híbrido, D2→(c) plataforma + capa propia, D3→empezar usándolo para prospección propia de TID (validas antes de vender). Pero es tu decisión.

---

## 2. Estructura del sistema (los bloques a construir)

Igual que Zolutium/LeadSales, pero verticalizado:

```
┌─────────────────────────────────────────────────────────┐
│  1. ATRACCIÓN      Ads (Meta/Google) + contenido vertical │
│                    industrial → landing                   │
├─────────────────────────────────────────────────────────┤
│  2. LANDING/VSL    Headline vertical + video + oferta +   │
│                    prueba social VERIFICABLE              │
├─────────────────────────────────────────────────────────┤
│  3. CALIFICACIÓN   Formulario B2B industrial (tipo        │
│                    comprador, volumen, certificaciones)   │
├─────────────────────────────────────────────────────────┤
│  4. IA / AGENTE    Responde, califica y agenda por        │
│                    WhatsApp (+ lee planos/specs/PDF ✅)   │
├─────────────────────────────────────────────────────────┤
│  5. CRM/PIPELINE   RFQs, cotizaciones, seguimiento        │
├─────────────────────────────────────────────────────────┤
│  6. INTELIGENCIA   Prospección (Apollo/ZoomInfo),         │
│                    nuevas inversiones, nearshoring        │
└─────────────────────────────────────────────────────────┘
```

**Diferenciadores clave frente a la competencia (ya validados en el expediente):**
- ✅ La IA **lee documentos técnicos** (planos, specs, PDFs) — LeadSales NO puede.
- ✅ Calificación por **variables industriales reales** (OEM/EMS/Tier 1, volumen, certificaciones) — nadie lo hace.
- ✅ **Prueba social verificable** — anti-patrón de Zolutium (testimonios duplicados, marcas falsas).
- ✅ **Inteligencia de mercado industrial** integrada — ni Zolutium ni LeadSales la tienen.

---

## 3. Roadmap por fases

### Fase 0 — Definición (esta semana)
- [ ] Cerrar D1, D2, D3 (arriba).
- [ ] Redactar propuesta de valor / posicionamiento vertical (P3).
- [ ] Definir el ICP (perfil de cliente ideal) exacto: ¿maquila? ¿fabricante? ¿distribuidor? ¿tamaño? ¿región?

### Fase 1 — MVP (lo mínimo para vender)
- [ ] Landing + VSL vertical (headline anti-genérico).
- [ ] Formulario de calificación B2B industrial (P10).
- [ ] CRM + WhatsApp (agenda automática).
- [ ] IA SDR básica (responde y agenda).
- [ ] 1 caso/demo con datos reales de la industria.

### Fase 2 — Inteligencia
- [ ] Base de conocimiento del agente (catálogos, specs, FAQs técnicas).
- [ ] Soporte de documentos técnicos en la IA (P11).
- [ ] Prospección automática (Apollo/ZoomInfo) integrada al pipeline.
- [ ] Pipeline de RFQs/cotizaciones.

### Fase 3 — Escala y foso
- [ ] Inteligencia de mercado (inversiones, nearshoring, vacantes, noticias del sector).
- [ ] Portal para clientes.
- [ ] Casos de éxito verificables por vertical (electrónica, automotriz, etc.).

### Fase 4 — Plataforma
- [ ] Directorio/matchmaking compradores–proveedores.
- [ ] Analítica predictiva.
- [ ] API para integraciones.

---

## 4. Lo siguiente e inmediato

1. **Tú:** decidir D1, D2, D3 (o pedirme que te arme un comparativo para decidir).
2. **Yo (en cuanto decidas):** redactar la propuesta de valor + el guion del VSL vertical (el "anti-Zolutium").
3. **Yo:** diseñar el formulario de calificación industrial (P10).

---

## 5. Enlace con pendientes

Este plan reordena y da contexto a los pendientes ya abiertos (`pendientes.md`): P1 (alcance), P3 (posicionamiento), P4 (canales/voz), P10 (formulario), P11 (documentos). Se agregan D1–D3 como decisiones raíz.
