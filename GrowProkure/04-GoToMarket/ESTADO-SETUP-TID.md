# Estado del setup técnico — Piloto TID (plásticos / foil / tintas)

> Bitácora de la infraestructura de cold email de TID. Mismo flujo que Astute (ya probado). Iniciado: 2026-07-15.

## Dominios (ya comprados en Namecheap)
- **get-tid.com** (envío TID)
- **try-tid.com** (envío TID)
- Marca principal: growprokure.com (ya existe)

## Plan (mismo que Astute — 6 pasos)

1. **Google Workspace** — cuenta nueva con `get-tid.com` (SEPARADA de tidmexico.com.mx corporativo). Business Starter, mensual, región US.
2. **Crear 2-3 buzones por dominio** (carlos.moreno@, carlos@, c.moreno@) en get-tid.com y try-tid.com.
3. **DNS en Namecheap** (por dominio): MX (`smtp.google.com` pri 1) · SPF (`v=spf1 include:_spf.google.com ~all`) · DMARC (`v=DMARC1; p=none; rua=mailto:carlos.moreno@get-tid.com`) · DKIM (lo da Google). Borrar parking (CNAME www + URL Redirect @).
4. **Autorizar app Instantly "Confiable"** en el Admin de Google de la(s) cuenta(s) TID. Client-ID: `536726988839-pt93oro4685dtb1emb0pp2vjgjol5mls.apps.googleusercontent.com`
5. **Conectar buzones a Instantly** (Add New → Google → Login) + **prender warmup**.
6. Esperar 14 días → cargar contactos TID (del estudio Foil) + copy → lanzar.

## Contexto TID (ya tenemos inteligencia lista)
- Estudio Foil completo: 120 contactos / 63 emails / 5 segmentos.
- Contactos calientes: Bob Lenoir, Miguel Villafuerte, Jessica McConnell, Diego Alemán.
- Competidor: KURZ (378 compradores mapeados).
- Pitch: abasto local vs. importación · Bajío · solución integral · muestras gratis.
- Ver `02-Investigacion/plasticos/resumen-foil.md`.

## Estado (avance 2026-07-15)
- [x] Google Workspace get-tid.com — verificado + Gmail activo
- [x] Google Workspace try-tid.com — verificado + Gmail activo (2 cuentas, como Astute)
- [x] **DNS get-tid.com: COMPLETO** — verificación + SPF + MX + DKIM + DMARC ✅ (2026-07-15)
- [x] **DNS try-tid.com: COMPLETO** — verificación + SPF + MX + DKIM + DMARC ✅ (2026-07-15)
- [x] Buzones get-tid.com (carlos.moreno@ admin + carlos@ + carlosmoreno@ + c.moreno@)
- [~] Buzones try-tid.com (creando: carlos@, carlosmoreno@, c.moreno@)
- [x] **DKIM + DMARC en AMBOS dominios TID** ✅ (2026-07-15) — DKIM auto-verificando en Google
- [x] **App Instantly "Trusted" autorizada en AMBAS cuentas** ✅ (get-tid.com + try-tid.com, 2026-07-15)
- [x] **5 buzones TID conectados a Instantly** ✅ (2026-07-15): get-tid.com ×4 (carlos.moreno@, carlos@, carlosmoreno@, c.moreno@) + try-tid.com ×1 (carlos.moreno@)
- [x] **Warmup ACTIVO en los 5 buzones** ✅ 🔥 (flama verde confirmada, 2026-07-15) → listo aprox. 2026-07-29
- [ ] (14 días) lanzar campaña TID

## 🎊 SETUP TID COMPLETO AL 100% (2026-07-15)
Infraestructura de cold email de TID lista. Warmup de 14 días en curso. Único pendiente: en ~14 días (≈29 jul) cargar Tanda 1 (contactos del estudio Foil) + copy y lanzar a volumen bajo.

## ⚠️ Nota importante — límite de Google en try-tid.com (2026-07-15)
Google **bloqueó** la creación de los 3 buzones extra de try-tid.com (carlos@, carlosmoreno@, c.moreno@) por reuso del mismo teléfono de verificación en muchas cuentas nuevas. **Decisión: no forzarlo** (riesgo de suspensión). Con 5 buzones (~150 correos/día) sobra para el piloto.

### Estrategia de escalamiento a futuro (multi-cliente)
Para crecer sin el dolor de crear buzones a mano / verificación por teléfono:
- **Corto plazo:** seguir en **Instantly** (Astute + get-tid.com ya warmeando).
- **Mediano plazo (más clientes):** migrar a **Smartlead** (whitelabel multi-cliente, buzones ilimitados, API) + **Maildoso/Mailreef** como "fábrica" de buzones (dominio+DNS+buzón automático, sin teléfono). Combinación estándar de agencias de cold email.

> Estructura: 2 cuentas Workspace TID (get-tid.com + try-tid.com), ~6-8 buzones.
> Client-ID Instantly: `536726988839-pt93oro4685dtb1emb0pp2vjgjol5mls.apps.googleusercontent.com`

> ⚠️ Costo: cada buzón ~$8.40/mes. 6 buzones TID ≈ $50/mes más (sumado a los 7 de Astute).
