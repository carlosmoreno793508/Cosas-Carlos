# REGLAS de GrowProkure — datos y proyecto

> Reglas vigentes del proyecto. Las mantiene el agente **Prokure**. Carlos puede pedir agregar/editar reglas y Prokure actualiza este archivo.

## 1. Reglas de la base de datos (Capa 1)

- **R1 — Esquema único.** Todo contacto se normaliza a: `Vertical, Pais, Lado, Empresa, Contacto, Puesto, Funcion, Ciudad, Estado, Email, Telefono, Segmento, Prioridad, LinkedIn, Fuente, Origen`.
- **R2 — Deduplicar siempre.** Antes de integrar, quitar duplicados por email (minúsculas) y por (contacto+empresa). Reportar cuántos se removieron.
- **R3 — Email real o vacío.** No inventar emails. Sin `@` = vacío. Marcar genéricos (info@, ventas@) aparte de nominales.
- **R4 — Clasificar cada registro.** Vertical (Electronica/Plasticos) + Lado (Demanda/Oferta) + País + Segmento + Prioridad.
- **R5 — Conservar procedencia.** Nunca borrar la columna `Fuente`/`Origen`.
- **R6 — Respetar la Confianza.** No promover "Medium" a "confirmado" sin verificar.

## 2. Reglas de los dos lados

- **R7 — Oferta = clientes GrowProkure** (Astute en electrónica, TID en plásticos). Demanda = compradores objetivo (OEMs/EMS/fabricantes de piezas).
- **R8 — Los datos son de GrowProkure**, no del cliente. El activo (base + señales) siempre se queda en el proyecto.

## 3. Reglas de cumplimiento (outreach)

- **R0 — Autorización de marca.** Carlos autoriza expresamente representar a **TID** y a **Astute** en el outreach y usar sus marcas en los dominios de envío y correos (confirmado 2026-07-12). El outreach de electrónica sale como Astute; el de plásticos como TID.
- **R9 — Base legal B2B.** Solo outreach con interés legítimo B2B. Cumplir CAN-SPAM (identificación, opt-out, sin engaño) y privacidad.
- **R10 — Sin scraping masivo.** ZoomInfo/Apollo/Wiza solo para investigación legítima, dentro de sus términos. Nada de extracción masiva o reventa.
- **R11 — Dominios de prospección, nunca el principal.** Cold email solo desde dominios secundarios; jamás desde `growprokure.com` ni el corporativo de Astute/TID.
- **R12 — Warm-up obligatorio.** 14 días mínimo antes de enviar en frío desde un buzón nuevo.

## 4. Reglas del proyecto / repo

- **R13 — Casa única.** El negocio vive en `Cosas-Carlos/GrowProkure`. Los estudios crudos pueden vivir en `Astute`/`tid` como fuentes.
- **R14 — Versionar deliverables.** Archivos fuente (Excel/estudios) se suben a `02-Investigacion/`; entregables consolidados a `05-Recursos/`.
- **R15 — Marca vs. nombre interno.** Marca comercial = GrowProkure. Tagline = "Industrial Growth Intelligence".

## 5. Tarea recurrente de Prokure — ingesta automática de contactos

- **R16 — Vigilar fuentes y jalar nuevos contactos sin duplicar.** Cada vez que exista un Excel con contactos nuevos en las **fuentes designadas**, Prokure lo lee, normaliza al esquema, **deduplica contra la Base Maestra** (por email y contacto+empresa), integra solo los nuevos, y reporta cuántos entraron / cuántos eran duplicados. Nunca sobrescribe ni borra; solo agrega lo nuevo y conserva procedencia.

### Fuente principal: la bandeja `_INBOX`
- **`GrowProkure/02-Investigacion/_INBOX/`** — Prokure vigila esta carpeta. Cualquier Excel de contactos que caiga aquí (subido a GitHub o adjunto en el chat) se procesa y deduplica.

### Sesiones que GENERAN datos (privadas, NO accesibles por enlace)
> No se puede jalar de ellas por URL (403 + no son archivos). Sirven de referencia de procedencia. Para ingresar sus datos: exportar el Excel de la sesión → soltarlo en `_INBOX`.
- Electronics Market Study USA — `session_01Wky57mGqmGTn1ePKbirQGc`
- Estudio de Mercado Ind Electronica Mx — `session_01Jt3zc4PjFjrNF4kCWEcfjR`
- Foil market study repository sync — `session_01Tk81EzGn8v9qPK2bZcTCus`

> Nota de acceso: si en el futuro una fuente es un repo privado (`Astute`, `tid`) en alcance de la sesión, o una carpeta de Google Drive con conector autorizado, Prokure también puede jalar de ahí directamente.

---

## Registro de cambios de reglas

| Fecha | Cambio | Por |
|---|---|---|
| 2026-07-12 | Creación inicial (R1–R15) | Prokure |
