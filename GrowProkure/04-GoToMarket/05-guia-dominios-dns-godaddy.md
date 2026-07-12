# Guía — Dominios de prospección + DNS (GoDaddy + Google Workspace)

> Objetivo: dejar lista la infraestructura de correo en frío que protege la reputación. Todo se hace en GoDaddy (no necesitas migrar a AWS).

## Paso 0 — Concepto clave

- **Dominio principal** (`growprokure.com`) = marca/sitio. **NO se usa para enviar frío.**
- **Dominios secundarios** (los de abajo) = para las campañas de cold email. Si algo se quema, el principal queda intacto.

## Paso 1 — Comprar dominios secundarios (en GoDaddy)

Compra **2–3 variantes** parecidas a la marca del piloto. Ideas (verifica disponibilidad):

- Para GrowProkure: `growprokure.co`, `getgrowprokure.com`, `growprokure.net`, `try-growprokure.com`
- Para el piloto Astute (si Astute autoriza usar su marca): `astute-supply.com`, `astute-sourcing.com`, `try-astute.com` (⚠️ confirmar con Astute antes de registrar su marca).

> Regla: 1 dominio secundario ≈ 2–3 buzones ≈ ~30–45 envíos/día tras el warm-up. Para el volumen del piloto, 2–3 dominios bastan.

## Paso 2 — Crear buzones en Google Workspace

1. Ve a https://workspace.google.com → plan **Business Starter** (~$7/usuario/mes).
2. Agrega cada dominio secundario como dominio en Workspace (Admin → Cuenta → Dominios).
3. Crea **2–3 buzones por dominio** con nombres de persona real (ej. `carlos@`, `c.moreno@`, `ventas@` — mejor nombres de persona que genéricos).

## Paso 3 — Configurar DNS en GoDaddy (por cada dominio)

Entra a GoDaddy → tu dominio → **DNS → Administrar zonas**. Agrega estos registros (Google te da los valores exactos en el Admin de Workspace):

### 3.1 MX (recibir correo)
| Tipo | Nombre | Valor | Prioridad |
|---|---|---|---|
| MX | @ | `smtp.google.com` | 1 |

### 3.2 SPF (autoriza a Google a enviar por ti)
| Tipo | Nombre | Valor |
|---|---|---|
| TXT | @ | `v=spf1 include:_spf.google.com ~all` |

### 3.3 DKIM (firma los correos)
- En Workspace Admin → **Apps → Google Workspace → Gmail → Autenticar correo** → genera la clave DKIM.
- Copia el registro que te da y agrégalo en GoDaddy:
| Tipo | Nombre | Valor |
|---|---|---|
| TXT | `google._domainkey` | (la clave larga que genera Google) |

### 3.4 DMARC (política anti-spoofing)
| Tipo | Nombre | Valor |
|---|---|---|
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@tudominio.com` |

> Empieza con `p=none` (solo monitorea). Cuando todo esté estable, puedes subir a `p=quarantine`.

## Paso 4 — Conectar a Instantly + Warm-up

1. En Instantly → **Email Accounts → Add** → conecta cada buzón de Google (vía OAuth o IMAP/SMTP).
2. Activa **Warmup** en cada buzón.
3. **Espera 14 días MÍNIMO** antes de enviar cualquier campaña en frío. Esto es obligatorio: Google/Microsoft marcan como spam los dominios nuevos que envían frío de inmediato.

## Paso 5 — Verificar que todo quedó bien

- Usa https://www.mail-tester.com (envía un correo de prueba, te da score /10; busca 9–10).
- Verifica SPF/DKIM/DMARC en https://mxtoolbox.com.

## Checklist

- [ ] 2–3 dominios secundarios comprados en GoDaddy
- [ ] Google Workspace dado de alta + dominios agregados
- [ ] 2–3 buzones por dominio creados
- [ ] MX + SPF + DKIM + DMARC configurados en cada dominio
- [ ] Buzones conectados a Instantly + warm-up activado
- [ ] Score de mail-tester 9+/10
- [ ] ⏳ Esperar 14 días de warm-up antes de campañas
