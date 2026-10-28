# Embudo Inbound — GrowProkure / TID (borrador)

> Inspirado en el modelo de la competencia (New-Gen Consulting: anuncio → VSL → agendar llamada),
> pero adaptado a **nuestro motor: Click-to-WhatsApp + Vocero CRM** (el cliente escribe, el agente IA califica).
> Objetivo: que lleguen prospectos **inbound/warm** sin cold-email ni prospectar a mano.
> Fecha: 2026-10-12. Estado: BORRADOR para revisar.

---

## 0) El modelo (el flujo completo)

```
Anuncio (FB/IG Reels, ataca un dolor)
      ↓
Landing / VSL corto (1 video + 1 sola acción)
      ↓
Botón:  "Escríbenos por WhatsApp"   ← Click-to-WhatsApp (no "agendar llamada")
      ↓
Vocero CRM: agente IA califica en el chat (dentro de la ventana de 24h, texto libre)
      ↓
Lead calificado → pipeline → humano cierra / manda muestra (TID) o cotización (Astute)
```

**Por qué WhatsApp en vez de "agendar llamada":** menos fricción en LatAm, respuesta inmediata, y el agente IA de Vocero califica solo 24/7. Ellos usan llamada; nosotros usamos WhatsApp = más barato y más rápido.

---

## 1) El gancho del anuncio (lo más importante)

Regla: **nombrar el dolor exacto del cliente** en la primera línea (como hace la competencia: "deja los correos en frío…").

### Vertical TID (foil, tintas, empaque flexible) — dolor del comprador
- **A:** "¿Sigues parando la línea por falta de foil o tinta? Te conseguimos abasto confiable."
- **B:** "Convertidores de empaque: deja de rogarle a un solo proveedor. Muestras en días, no semanas."
- **C:** "¿Tu proveedor de tintas te quedó mal otra vez? Pide una muestra por WhatsApp y compara."

### Vertical Astute (componentes electrónicos / shortage) — dolor del comprador
- **A:** "¿Un componente en shortage te tiene parada la producción? Te lo buscamos."
- **B:** "Compradores de electrónica: deja de perseguir allocation. Cotiza por WhatsApp hoy."
- **C:** "¿Lead times imposibles? Encuentra el componente que nadie tiene. Escríbenos."

> Cada anuncio = 1 dolor + 1 promesa + 1 acción (WhatsApp). Probar 3-4 variantes y quedarse con la que convierta.

---

## 2) La landing / VSL (corta y con UNA sola acción)

Estructura de 5 bloques (video de 60-120 seg + texto de apoyo):

1. **Gancho (0-5 seg):** repite el dolor del anuncio. "Si tu línea para por falta de material, esto es para ti."
2. **Problema (agita):** lo que les cuesta hoy — paros, retrasos, depender de 1 proveedor, perder clientes.
3. **Solución:** cómo lo resolvemos (abasto/muestras/cotización rápida), sin jerga.
4. **Prueba:** 1-2 casos o números reales **(cuando los tengamos — NO inventar, R3)**. Mientras, logos/credenciales reales de TID/Astute.
5. **Una sola acción:** botón grande **"Escríbenos por WhatsApp"**. Nada más. Sin menú, sin formulario largo.

> Diferencia clave vs. la competencia: **no pedimos "agenda una llamada"** (fricción alta). Pedimos un mensaje de WhatsApp (fricción casi cero).

---

## 3) La oferta / garantía (diferenciador)

Copiar la lógica de "resultado o no pagas", pero **honesta y acotada** a lo que sí controlamos:
- **TID:** "Te mandamos una **muestra gratis** de foil/tinta para que la pruebes en tu línea antes de comprar."  ← muestra = su "garantía", bajo riesgo para el cliente.
- **Astute:** "Te **cotizamos sin costo** y solo cobras si el componente llega como lo prometimos."

> Evitar promesas que no controlamos (ventas garantizadas). La muestra/cotización gratis es un gancho real y cumplible.

---

## 4) El agente IA en Vocero (qué pregunta en el chat)

Cuando el prospecto escribe por WhatsApp, el agente califica en lenguaje natural:
1. ¿Qué material/componente necesitas? (producto)
2. ¿Qué volumen / cada cuánto? (tamaño de cuenta)
3. ¿Para cuándo lo necesitas? (urgencia)
4. ¿Empresa y tu puesto? (BANT básico)
5. (TID) ¿Te mando una muestra? → pide dirección. (Astute) ¿Te armo cotización? → pide specs.

→ El agente etiqueta: **caliente / tibio / frío**, lo mete al pipeline y avisa al humano si es caliente.

---

## 5) Cumplimiento (no negociable)

- **WhatsApp API oficial** (Meta Cloud API) — nada de automatización pirata = sin baneo.
- El cliente **inicia** la conversación (Click-to-WhatsApp) → ventana de 24h de texto libre, sin plantillas.
- Outbound solo a quien dio **opt-in**, con plantillas aprobadas. **Nunca** cold masivo (R10).
- No inventar casos ni números (R3): usar pruebas reales o ninguna.

---

## 6) Lo que falta para lanzarlo (checklist)

- [ ] Montar **Vocero** en VPS (Hostinger KVM1) + número de WhatsApp Business dedicado.
- [ ] Grabar 1 VSL corto por vertical (o versión texto+imagen para empezar).
- [ ] Armar la landing con botón Click-to-WhatsApp.
- [ ] Cargar 3-4 variantes de anuncio (los ganchos de arriba) en Meta Ads.
- [ ] Escribir el prompt del agente IA (secciones 4) en Vocero.
- [ ] Presupuesto de prueba de Meta Ads (empezar chico, medir costo por lead).

---

> Siguiente: cuando montemos Vocero, este embudo es el plan de go-to-market inbound.
> Ventaja vs. la competencia: mismo modelo, pero con WhatsApp (más barato/rápido en LatAm) y quedándonos el margen en vez de pagarle a una agencia.
