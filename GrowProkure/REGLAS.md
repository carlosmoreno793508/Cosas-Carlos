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

- **R9 — Base legal B2B.** Solo outreach con interés legítimo B2B. Cumplir CAN-SPAM (identificación, opt-out, sin engaño) y privacidad.
- **R10 — Sin scraping masivo.** ZoomInfo/Apollo/Wiza solo para investigación legítima, dentro de sus términos. Nada de extracción masiva o reventa.
- **R11 — Dominios de prospección, nunca el principal.** Cold email solo desde dominios secundarios; jamás desde `growprokure.com` ni el corporativo de Astute/TID.
- **R12 — Warm-up obligatorio.** 14 días mínimo antes de enviar en frío desde un buzón nuevo.

## 4. Reglas del proyecto / repo

- **R13 — Casa única.** El negocio vive en `Cosas-Carlos/GrowProkure`. Los estudios crudos pueden vivir en `Astute`/`tid` como fuentes.
- **R14 — Versionar deliverables.** Archivos fuente (Excel/estudios) se suben a `02-Investigacion/`; entregables consolidados a `05-Recursos/`.
- **R15 — Marca vs. nombre interno.** Marca comercial = GrowProkure. Tagline = "Industrial Growth Intelligence".

---

## Registro de cambios de reglas

| Fecha | Cambio | Por |
|---|---|---|
| 2026-07-12 | Creación inicial (R1–R15) | Prokure |
