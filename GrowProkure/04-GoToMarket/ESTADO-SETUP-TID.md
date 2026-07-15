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

## Estado
- [ ] Paso 1: Google Workspace (get-tid.com)
- [ ] Paso 2: buzones
- [ ] Paso 3: DNS
- [ ] Paso 4: autorizar Instantly
- [ ] Paso 5: conectar + warmup
- [ ] Paso 6: (14 días) lanzar

> ⚠️ Costo: cada buzón ~$8.40/mes. 6 buzones TID ≈ $50/mes más (sumado a los 7 de Astute).
