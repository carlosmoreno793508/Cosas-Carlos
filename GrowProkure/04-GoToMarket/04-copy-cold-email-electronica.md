# Copy de Cold Email — Vertical Electrónica (piloto Astute)

> Secuencia lista para cargar en Instantly. Dirigida a compradores / commodity managers / procurement en OEMs y EMS. Ángulo: dolores reales de la cadena de componentes electrónicos (EOL/obsolescencia, escasez/allocation, segunda fuente, lead-times, nearshoring). Personaliza `{{variables}}`.

**Idioma:** primario **inglés** (compradores US y corporativos MX suelen operar en inglés). Abajo hay variante en español para plantas en México.

**Reglas de entregabilidad:** correos cortos, sin imágenes, sin links en el primer correo, 1 sola pregunta, texto plano. Máx ~75–100 palabras.

---

## Secuencia A — Inglés (4 correos)

### Email 1 — Día 0 (Problema + relevancia)
**Asunto:** `{{company}} — EOL & allocation risk`

```
Hi {{first_name}},

Quick question — how is {{company}} handling components going EOL or into
allocation right now? Most commodity teams I talk to are firefighting
last-time-buys and scrambling for second sources.

We help procurement teams de-risk exactly that: hard-to-find parts,
obsolescence coverage, and franchised second-source options before a
line-down hits.

Worth a 15-min call to see if it's relevant to your {{commodity}} spend?

Carlos
```

### Email 2 — Día 3 (Prueba / especificidad)
**Asunto:** `re: {{company}} — EOL & allocation risk`

```
Hi {{first_name}},

Following up. Where we usually add value fast:

- Sourcing obsolete / hard-to-find parts (avoiding line-downs)
- Franchised, traceable second sources (no counterfeit risk)
- Shortening lead times on allocated commodities

If avoiding a line-down this quarter is worth 15 minutes, I'll bring
2–3 ideas specific to {{company}}.

Carlos
```

### Email 3 — Día 7 (Ángulo nearshoring / MX)
**Asunto:** `Nearshoring your component supply?`

```
Hi {{first_name}},

With more manufacturing moving to Mexico, a lot of teams are re-balancing
their component supply base closer to the plant.

If {{company}} is looking at second sources or shorter lead times as part
of that shift, that's squarely what we do.

Open to a quick call next week?

Carlos
```

### Email 4 — Día 12 (Break-up / última llamada)
**Asunto:** `Should I close this out?`

```
Hi {{first_name}},

Haven't heard back, so I'll assume component risk isn't top of mind right
now — totally fair.

If that changes (an EOL notice, an allocation surprise, a line-down),
reply "hey Carlos" and I'll jump in.

Thanks,
Carlos
```

---

## Secuencia B — Español (variante para plantas en México)

### Correo 1 — Día 0
**Asunto:** `{{company}} — riesgo de obsolescencia (EOL)`

```
Hola {{first_name}},

Pregunta rápida: ¿cómo está manejando {{company}} los componentes que
entran en EOL o en allocation? La mayoría de los equipos de compras andan
apagando incendios con last-time-buys y buscando segundas fuentes.

Justamente ayudamos a compras a blindar eso: partes difíciles de
conseguir, cobertura de obsolescencia y segundas fuentes franquiciadas
antes de que pare una línea.

¿Vale una llamada de 15 min para ver si aplica a tu gasto en
{{commodity}}?

Carlos
```

*(Correos 2–4: mismos ángulos que la secuencia en inglés, traducidos.)*

---

## Variables a llenar (desde ZoomInfo/Apollo/Wiza + estudio Astute)

| Variable | Ejemplo | Fuente |
|---|---|---|
| `{{first_name}}` | Juan | enriquecimiento |
| `{{company}}` | Mabe | lista objetivo |
| `{{commodity}}` | pasivos / semiconductores / conectores | por cuenta |
| `{{title}}` | Commodity Manager | enriquecimiento |

## A/B testing (qué probar primero)

1. **Asunto:** "EOL & allocation risk" vs "Should we second-source {{commodity}}?"
2. **Ángulo del Email 1:** obsolescencia vs escasez vs nearshoring.
3. **CTA:** "15-min call" vs "should I send 2–3 ideas?"

## Métricas objetivo (piloto)

- Open rate: >50% (si baja, problema de entregabilidad/asunto)
- Reply rate: >5% (bueno para frío B2B)
- Positive reply → reunión: la métrica que importa.
