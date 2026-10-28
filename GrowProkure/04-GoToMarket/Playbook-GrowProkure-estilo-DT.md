# Playbook GrowProkure — estilo DT Marketing Digital (con IA SDR propio)

> Blueprint decodificado del modelo DT (agencia de agendamiento B2B) adaptado a GrowProkure/TID/Astute.
> Modelo: **vender el RESULTADO (reuniones/muestras), no la herramienta.** Nicho + garantía + 3 canales + IA SDR.
> Fecha: 2026-10-28. Estado: borrador accionable.

---

## 1) El modelo en una frase
Conseguir reuniones calificadas con **compradores industriales** (electrónica/EMS para Astute; foil/tintas/empaque para TID), combinando **LinkedIn + correo + un IA SDR**, con una **garantía por escrito**. Tú (o el cliente) solo hablas con empresas que ya quieren hablar.

---

## 2) El mecanismo: "Tres canales. Una sola secuencia."
Igual que DT, pero con TUS piezas:

```
LinkedIn ───┐
Correo    ──┼─► UNA secuencia que decide por dónde entrar ──► Reunión / Muestra
IA SDR    ──┘     (Vocero/WhatsApp = inbound + calificación)
```

- **LinkedIn:** conexión + mensajes personalizados a los 112 decisores de compras.
- **Correo:** correo en frío hiperpersonalizado (B2B, no spam masivo).
- **IA SDR = Vocero/WhatsApp:** responde, califica y agenda **24/7** (este es tu "Setter IA").
- **La secuencia** decide: si abre LinkedIn → sigue por ahí; si responde correo → pasa a WhatsApp/llamada; si escribe por WhatsApp (inbound) → el agente IA califica.

---

## 3) Cómo armar TU propio IA SDR (lo que preguntaste)

**Un IA SDR = software que prospecta, escribe, responde, califica y agenda solo.** No es magia: es automatización + un LLM que personaliza + buena data. Se arma en 2 mitades:

### Mitad A — INBOUND (ya la tienes) ✅
- **Vocero / el agente IA (Claude).** Cuando alguien escribe por WhatsApp (de un anuncio o del correo/LinkedIn), el agente:
  1. Pregunta: material/componente, volumen, urgencia, empresa/puesto.
  2. Califica (caliente/tibio/frío).
  3. Agenda o pide dirección para la muestra (TID) / specs para cotizar (Astute).
- **Esto es tu Setter IA.** Ya está diseñado; solo falta montarlo (Vocero o Leadsales prueba gratis).

### Mitad B — OUTBOUND (lo que falta) ⬜
Para salir a buscar en frío a los 112 contactos por LinkedIn + correo, opciones:
| Opción | Qué es | Costo | Nota |
|---|---|---|---|
| **Instantly / Smartlead** | Correo en frío a escala + IA que personaliza | ~$30-100/mes | Lo más directo para el correo |
| **HeyReach / Expandi / Dripify** | Automatización de LinkedIn (conexiones+mensajes) | ~$40-100/mes | Ojo límites de LinkedIn (no banear) |
| **Clay** | Enriquece + personaliza con IA a escala | ~$150/mes | Potente, más avanzado |
| **Apollo** | Base + secuencias + correo en uno | tiene plan free | Todo-en-uno para empezar |
| **Hazlo manual al inicio** | Tú + plantillas con IA (Claude) | $0 | Para validar con los primeros 20-30 |

> **Recomendación:** al inicio, **manual + plantillas con IA** sobre los 112 (validar que el mensaje funciona), y cuando funcione, automatizar con 1 herramienta de correo (Instantly) + 1 de LinkedIn. No compres 4 herramientas de golpe.

---

## 4) La secuencia paso a paso (para los 112 contactos, ya enriquecidos)
Pre-requisito: enriquecer los 112 en ZoomInfo (LinkedIn + correo directo). Luego:

- **Día 1 — LinkedIn:** conexión con nota corta (sin vender). *"Hola [nombre], veo que llevas compras en [empresa]. Trabajo con abasto de [foil/componentes]; me gustaría conectar."*
- **Día 2 — Correo 1:** el dolor + la oferta cumplible. *"¿Han tenido paros por falta de [material]? Te mando una muestra gratis / cotización sin costo."*
- **Día 4 — LinkedIn mensaje** (si aceptó): valor, no pitch.
- **Día 6 — Correo 2:** caso/prueba (cuando la tengas) o recordatorio suave.
- **Día 9 — Correo 3 (cierre suave):** *"¿Te late que te mande la muestra o lo dejamos para otro momento?"*
- **En cualquier punto que respondan → entra el IA SDR (Vocero/WhatsApp)** a calificar y agendar.

**Regla:** si responde interesado → humano cierra. El IA SDR hace el trabajo pesado; tú cierras.

---

## 5) Tu garantía (cumplible y por escrito)
Copia la lógica de DT, pero **solo promete lo que controlas** (R3):
- **TID:** *"Te mandamos una muestra gratis de foil/tinta para que la pruebes en tu línea. Si no te sirve, no compras."*
- **Astute:** *"Cotización sin costo; solo pagas si el componente llega como lo prometimos."*
- **NUNCA** prometer "X ventas garantizadas" — eso no lo controlas.

---

## 6) Cumplimiento (no negociable)
- **LinkedIn/correo en frío B2B:** legítimo, pero **personalizado y acotado** — nada de blasting masivo (R10). Respetar límites de LinkedIn (pocas conexiones/día) para no banear.
- **WhatsApp:** solo **inbound** o con **opt-in** (API oficial). Nada de cold masivo por WhatsApp (ban).
- **No inventar** datos ni casos (R3).

---

## 7) Qué está LISTO vs qué FALTA
| Pieza | Estado |
|---|---|
| Combustible: 112 decisores filtrados | ✅ (falta enriquecer en ZoomInfo) |
| IA SDR inbound (Vocero/agente) | 🟡 diseñado, falta montar |
| Herramienta outbound (correo/LinkedIn) | ⬜ elegir 1 |
| Secuencia de mensajes | ✅ (arriba; falta redactar finales) |
| Oferta + garantía | ✅ definida |
| Primer envío a 20-30 contactos | ⬜ **el siguiente paso real** |

---

## 8) El siguiente paso concreto
1. Enriquecer los 112 en ZoomInfo (ya tienes `ZoomInfo_Upload_Verticales.csv` + el prompt de terminal).
2. Con 20-30 ya enriquecidos → mandar la **secuencia manual** (LinkedIn + correo) para validar el mensaje.
3. Montar Vocero/Leadsales para recibir y calificar (IA SDR inbound).
4. Medir: ¿cuántos responden? ¿cuántos agendan/piden muestra? → de ahí se decide automatizar.

> No necesitas la "máquina completa" para empezar. Con 20 correos + LinkedIn bien hechos ya sabes si jala.
