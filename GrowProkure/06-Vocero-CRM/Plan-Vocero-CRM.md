# Vocero CRM — Plan de instalación, requisitos Meta y costos

> Auditoría + plan para **kevinrivm/vocero-crm v1.5.0** (CRM de WhatsApp open-source, MIT).
> Uso previsto: **inbound/warm** para GrowProkure–TID (anuncios Click-to-WhatsApp → agente IA califica → pipeline → solicitudes de muestra TID). NO para cold blasting.
> Fecha: 2026-10-11. Fuente: código del repo (INSTALL-IA.md, docker-compose.yml, .env.example).

---

## A) Plan de instalación "Agent-First" (en tu VPS Hostinger)

El repo está hecho para que **la IA lo instale**: trae un guion `INSTALL-IA.md` que Claude Code sigue solo. Tú solo contestas 3 preguntas.

### Datos técnicos
- **Imagen Docker:** `ghcr.io/kevinrivm/vocero-crm:1.5.0` (linux/amd64, escucha en puerto `3000`).
- **Dos rutas de instalación:**
  - **Ruta A — Coolify** (panel que gestiona Docker + HTTPS). Más cómodo a futuro, pero hay que instalar Coolify en el VPS primero.
  - **Ruta B — Docker + Caddy** (docker-compose, HTTPS automático). **La más directa para tu Hostinger KVM2** si solo tiene Docker.
- La conexión de **WhatsApp y la IA NO se configuran en la instalación** → se hacen *dentro de la app* después (Ajustes → IA / Ajustes → WhatsApp).

### Requisitos previos (tú los consigues)
1. **Un dominio/subdominio** para el CRM, ej. `crm.tid...mx` o `crm.growprokure.com`, con **registro A apuntando a la IP del VPS**.
2. VPS con **Docker** (tu Hostinger KVM2 sirve). Si es ARM, se construye desde código (la imagen es amd64).
3. (Opcional) **Token de OpenRouter** si quieres el agente IA desde el arranque (se puede agregar después).

### El prompt "Agent-First" (pégalo en Claude Code, en el VPS o apuntando a él)
```
Instala Vocero CRM en mi VPS siguiendo su guia oficial INSTALL-IA.md:
https://github.com/kevinrivm/vocero-crm/blob/main/INSTALL-IA.md

Contexto / mis respuestas a las 3 preguntas:
- Dominio: crm.MIDOMINIO.com  (ya apunta por registro A a la IP de mi VPS)
- Token de OpenRouter: (lo agrego despues desde Ajustes -> IA)   # o pégalo si ya lo tienes
- Ruta: B  (mi VPS solo tiene Docker, sin panel Coolify)

Reglas:
- Genera TU todos los secretos (BETTER_AUTH_SECRET, ENCRYPTION_KEY de 32 bytes,
  META_WEBHOOK_VERIFY_TOKEN, POSTGRES_PASSWORD) con openssl. No me los pidas.
- Usa docker compose (app + Postgres 16 + Caddy). Caddy saca el HTTPS solo.
- Al terminar verifica que https://crm.MIDOMINIO.com/api/health responde ok:true
  y que /login carga. Dime el usuario/clave inicial o el flujo de alta.
- NO conectes WhatsApp ni la IA en la instalacion: eso lo hago yo en la app despues.
```
> En la **Ruta B** el propio repo trae `pnpm init-env --domain <dominio>` (crea el `.env` con secretos) y `pnpm doctor` (lo verifica) → luego `docker compose up -d`. Actualizar = `git pull` + `docker compose up -d`.

### Secretos que se generan (referencia)
```
openssl rand -base64 32   # BETTER_AUTH_SECRET
openssl rand -base64 32   # ENCRYPTION_KEY (32 bytes base64)
openssl rand -hex 32      # META_WEBHOOK_VERIFY_TOKEN
openssl rand -hex 24      # POSTGRES_PASSWORD
```
### Variables de entorno principales
`APP_BASE_URL=https://<dominio>` · `DATABASE_URL=postgresql://postgres:<pwd>@postgres:5432/vocero` · `BETTER_AUTH_SECRET` · `ENCRYPTION_KEY` · `META_WEBHOOK_VERIFY_TOKEN` · `META_GRAPH_API_VERSION=v25.0` · (opc.) `OPENROUTER_API_TOKEN`, `OPENROUTER_MODEL=anthropic/claude-sonnet-4.5`.

### Después de instalar (dentro de la app)
1. **Ajustes → IA:** pega proveedor + modelo + llave (OpenRouter con Claude), "Probar conexión".
2. **Ajustes → WhatsApp:** conecta tu número vía la Cloud API de Meta (ver sección B).
3. Define el **pipeline** y el **prompt del agente** (en lenguaje natural, describiendo tu negocio: Astute = componentes/shortage; TID = foil/tintas + muestras).

---

## B) Requisitos de Meta (WhatsApp Cloud API) + costos

Vocero usa la **API oficial de WhatsApp (Meta Graph API v25.0)** → compliant, bajo riesgo de ban. Pero exige el setup oficial de Meta:

### Checklist Meta (orden recomendado)
1. **Meta Business Manager** (cuenta de empresa) — con **verificación de negocio** (te piden comprobante fiscal/domicilio; puede tardar días).
2. **Meta App** en developers.facebook.com con el producto **WhatsApp** agregado → de ahí sacas **App Secret** y el **token**.
3. **WhatsApp Business Account (WABA)** + **número telefónico dedicado** a la API.
   - ⚠️ El número **NO puede estar en uso en la app normal de WhatsApp/WhatsApp Business**. Usa un número nuevo (o libéralo antes).
   - Aprobación del **Display Name** (nombre que ve el cliente).
4. **Token permanente** (recomendado: *System User token* en Business Settings, no el token temporal de 24h).
5. **Webhook:** apúntalo a `https://<tu-dominio>/` del CRM con el `META_WEBHOOK_VERIFY_TOKEN` que generaste. (Opcional: `META_APP_SECRET` para validar firma.)
6. **Plantillas de mensaje (templates):** para escribir **fuera de la ventana de 24h** (o iniciar conversación) Meta exige **plantillas aprobadas** por categoría (utility / marketing / authentication). Se mandan a revisión y tardan de minutos a 1-2 días.
   - Dentro de la **ventana de 24h** (el cliente te escribió primero) puedes responder **texto libre** sin plantilla → por eso esto brilla en **inbound**.

### Costos (estimado — VERIFICAR precios actuales de Meta, cambian)
| Concepto | Costo aprox. | Nota |
|---|---|---|
| **WhatsApp Cloud API (Meta)** | Por **mensaje/conversación**, según categoría y país (MX). Marketing es el más caro; utility/service más barato; **service dentro de 24h suele ser gratis**. | Meta migró a cobro **por mensaje** en 2025. Revisa la tabla oficial de precios MX antes de proyectar volumen. |
| **VPS (Hostinger KVM2)** | ~**unos USD/mes** (el que ya usas). | Corre app + Postgres + Caddy sin problema. |
| **LLM del agente (OpenRouter/Claude)** | **centavos por conversación** (tokens). | Controlable con el modelo que elijas. |
| **Dominio** | el que ya tengas. | Solo un subdominio. |

**Traducción:** el software es gratis (MIT), pero **operarlo tiene 3 costos reales**: mensajes de Meta + VPS + tokens de IA. Para inbound/warm en volúmenes chicos-medianos es barato; para marketing masivo, Meta cobra por mensaje.

### Recomendación de alcance
- **Empieza inbound:** anuncios **Click-to-WhatsApp** (el cliente inicia → 24h de texto libre → el agente califica) → mínimo fricción de plantillas y costo.
- **Outbound** (plantillas) solo para seguimientos puntuales a quienes ya opten-in. **Nunca** cold masivo.

---

## C) Enriquecimiento de contactos — estado y siguiente paso
(Lo seguimos en paralelo, no depende de Vocero.)
- **Wiza:** se quedó en **0 créditos API** (500 email, 0 phone) → no puede enriquecer; hay que recargar.
- **ZoomInfo:** desconectado en la sesión remota → se reconecta en claude.ai → Connectors (o en terminal con `/mcp`) y se usa su **Enhance** (ya tienes el CSV `ZoomInfo_Upload_Nuevos.csv` listo).
- **Siguiente paso:** reconectar ZoomInfo y correr el **Enhance** con los 109 nuevos (y de paso las textiles de la sesión CLT).

---

> Estado: auditoría + plan listos (2026-10-11). Repo auditado: integración WhatsApp **oficial** (Cloud API), stack Next.js 15 + Postgres/Drizzle, secretos cifrados (AES-256-GCM), webhooks firmados (HMAC). Proyecto de 1 dev — bien hecho; tú mantienes el VPS.
