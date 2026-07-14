# Estado del setup técnico — Piloto Astute (electrónica)

> Bitácora de avance de la infraestructura de cold email. Actualizado: 2026-07-12.

## ✅ Hecho

| Componente | Detalle |
|---|---|
| **Dominios (Namecheap)** | growprokure.com (marca), get-tid.com, try-tid.com, astute-supply.com, get-astute.com |
| **Instantly** | Cuenta creada, plan Growth |
| **Google Workspace** | Business Starter, plan mensual, región US, prueba 14 días (pago inicia 28 jul 2026) |
| **Dominios verificados en Workspace** | get-astute.com ✅ · astute-supply.com ✅ |
| **DNS get-astute.com** | MX (smtp.google.com pri 1) ✅ · DKIM ✅ · SPF (`v=spf1 include:_spf.google.com ~all`) ✅ · DMARC (`v=DMARC1; p=none; rua=...`) ✅ |
| **Gmail activado** | get-astute.com ✅ · astute-supply.com ✅ |
| **Buzones creados (get-astute.com)** | carlos.moreno@ (admin) · carlos@ · c.moreno@ |

## Estructura de cuentas (CONFIRMADO 2026-07-12)

**Son 2 cuentas de Workspace separadas** (ambas llamadas "Astute Supply"), 7 buzones en total. Decisión: **dejar así** (funciona para Instantly; consolidar no vale la pena). Implica 2 suscripciones (~$59/mes total por 7 buzones).

| Cuenta | Dominio | Buzones |
|---|---|---|
| 1 | astute-supply.com | carlos.moreno@ (admin), carlos@, c.moreno@, carlosmoreno@ (4) |
| 2 | get-astute.com | carlos.moreno@ (admin), carlos@, c.moreno@ (3) |

## ✅ COMPLETADO (2026-07-13): Instantly + Warmup

- App "Instantly oAuth Email v1" autorizada como **Confiable** en Google Admin de AMBAS cuentas (astute-supply.com + get-astute.com).
- **Los 7 buzones conectados a Instantly** (vía Google OAuth).
- **Warmup ACTIVADO en los 7** (flama verde). Calentamiento gradual de 14 días en curso.
- 🎉 **Infraestructura de cold email COMPLETA.**

### Warmup iniciado: 2026-07-13 → listo aprox. 2026-07-27 (14 días)

## ✅ DNS COMPLETO EN AMBOS DOMINIOS (2026-07-13)

| Dominio | MX | DKIM | SPF | DMARC |
|---|---|---|---|---|
| get-astute.com | ✅ | ✅ | ✅ | ✅ |
| astute-supply.com | ✅ | ✅ | ✅ | ✅ |

**🎊 Infraestructura de cold email COMPLETA al 100%.**

## ⏳ Único pendiente (en ~14 días, warmup listo ~2026-07-27)
- Revisar Health Score (debe subir a 90-100%).
- Cargar Tanda 1 (`Astute_Tanda1_contactos.xlsx`) + copy (`04-copy-cold-email-electronica.md`).
- Lanzar primera campaña de Astute a volumen bajo.
   - SPF: `v=spf1 include:_spf.google.com ~all`
   - DMARC: `v=DMARC1; p=none; rua=mailto:carlos.moreno@astute-supply.com`
3. **Crear 2-3 buzones en astute-supply.com** (carlos.moreno@, carlos@, c.moreno@).
4. **Guardar/confirmar contraseñas** de todos los buzones (se necesitan para Instantly).
5. **Conectar los 6 buzones a Instantly** (vía Google OAuth) + **prender WARM-UP**.
6. **Esperar 14 días de warm-up** antes de cualquier envío.
7. Luego: cargar Tanda 1 (`Astute_Tanda1_contactos.xlsx`) + copy (`04-copy-cold-email-electronica.md`) y lanzar campaña a volumen bajo.

## Notas
- Región Workspace = US (para pagar con tarjeta americana). No afecta entregabilidad.
- MX puede tardar hasta 24h en propagar del todo, pero ya se activó Gmail.
- Buzones = nombres de persona real (mejor entregabilidad).
- Regla de oro: enviar SOLO desde estos dominios secundarios, nunca desde el corporativo. Warm-up obligatorio 14 días.
