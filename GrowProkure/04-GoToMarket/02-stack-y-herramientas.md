# Stack y herramientas — decisión final

> Estado 2026-07-12. Presupuesto aprobado ~$100–200/mes (baja de $150–300 porque los datos ya están cubiertos con ZoomInfo/Apollo/Wiza).

## Stack del piloto (Astute)

| Función | Herramienta elegida | Plan / costo | Notas |
|---|---|---|---|
| **Envío + warm-up** | **Instantly.ai** | Growth — **$47/mes** ($37.60 anual) | Buzones y warm-up ILIMITADOS. Link: https://instantly.ai/pricing. NO comprar su add-on de leads. |
| **Dominios de prospección** | **GoDaddy** (quédate ahí) | ~$10–15 c/u anual | 2–3 dominios secundarios. Guía en `05-guia-dominios-dns-godaddy.md`. |
| **Buzones de correo** | **Google Workspace** | ~$7/usuario/mes × 4–6 | Business Starter. Se conectan a Instantly. |
| **Datos B2B / contactos** | **ZoomInfo + Apollo + Wiza** | Ya conectados | Cubren minería y enriquecimiento. Cero costo extra. |
| **Verificación de correos** | **NeverBounce / Bouncer** | Por volumen (~$0–50) | Limpiar listas antes de enviar. Apollo/ZoomInfo ya dan correos verificados en parte. |
| **Agenda de reuniones** | **Cal.com** (o Calendly) | Free / $15 | Prospectos agendan solos. |
| **CRM** | **Aplazado** (usar Instantly + Google Sheets al inicio) | $0 | HubSpot free después. No sobre-ingenierizar el arranque. |
| **SOPs / video** | **Loom** | Free | Grabar cada proceso → manuales. |

**Costo mensual real de arranque: ~$100–150/mes** (Instantly $47 + Workspace ~$50 + dominios prorrateados + verificación variable).

## Hosting / sitio web (aclaración importante)

- **No migrar a AWS por ahora.** El hosting del sitio es un proyecto aparte que NO aporta al piloto.
- Los **dominios de prospección** se compran y configuran en GoDaddy igual de bien.
- El sitio de marca (`growprokure.com`) puede ir después en cualquier host (GoDaddy, Vercel, Netlify o AWS). El prototipo que construimos es HTML estático → se puede alojar gratis en Vercel/Netlify/GitHub Pages cuando toque.
- **Regla de oro del cold email:** NUNCA envíes frío desde tu dominio principal (`growprokure.com` o el corporativo de Astute). Solo desde dominios secundarios. Protege la reputación.

## Accesos (quién controla qué)

- Las cuentas (GoDaddy, Google Workspace, Instantly) van **a tu nombre / con tu pago**. Yo (Claude) **no tengo acceso directo** a ellas; te doy las guías paso a paso y los contenidos.
- Los datos B2B (ZoomInfo/Apollo/Wiza) sí los puedo consultar desde aquí para armar listas e inteligencia.
