# Estado del enriquecimiento — 31 ago 2026

Trabajo hecho en la sesión del 30–31 de agosto, incluida la corrida autónoma nocturna.

## Gasto total

| Herramienta | Gasto | Saldo |
|---|---|---|
| ZoomInfo | **127 créditos** | no expone saldo por API |
| Wiza | **1 crédito de API, 0 de email** | 1330.5 API / 499 email |
| Apollo | 0 | sin autenticar (`/mcp`) |

Desglose ZoomInfo: 25 Top25 Astute · 78 Top100 Tsunami · 24 hueco México.
Ni un crédito en cuentas sin candidato válido: los agentes tenían prohibido enriquecer sin comprador identificado.

## Entregables

| Archivo | Qué es | Listos |
|---|---|---|
| `04-GoToMarket/Astute_Top25_ENRIQUECIDO.csv` | Top25 Astute con comprador real, alterno y confianza | 24 de 25 |
| `02-Investigacion/Tsunami_Prospectos_CLASIFICADO.csv` | CRM Tsunami clasificado, con cumplimiento y contactos gratis | 359 con correo |
| `02-Investigacion/Tsunami_Top100_ENRIQUECIDO.csv` | Lote de prueba comprado | 78 de 100 |
| `02-Investigacion/Tsunami_x_Mexico.csv` | Vista mexicana del CRM: 357 cuentas con planta en México | 287 con contacto |
| `02-Investigacion/Tsunami_MX_Hueco_ENRIQUECIDO.csv` | Las 38 con planta MX y sin comprador | 24 de 38 |
| `02-Investigacion/Estudios_Correos_En_Riesgo.csv` | Correos que probablemente reboten | 25 graves |

**Contactos nuevos accionables esta sesión: 126** (24 + 78 + 24).

## FILTROS OBLIGATORIOS antes de cualquier envío

1. `no_contactar != "SI"` — 8 cuentas con *DO NOT CALL* / blacklist / quiebra (CRFS, Qual-Pro, Vyrian, Dot Comps, Amigo Tecnología, McCain Traffic, Ruegger, Numbat). **R9.**
2. `tipo_final != "DUP/Inactivo"` — otras 100.
3. Excluir los **25 correos de severidad ALTA** de `Estudios_Correos_En_Riesgo.csv`. Enviar a buzones muertos castiga la reputación del dominio, justo durante el warm-up (**R12**).
4. Dominio secundario, nunca `growprokure.com` ni el corporativo de Astute (**R11**).

## Decisiones que esperan a Carlos

| # | Asunto | Qué hace falta |
|---|---|---|
| 1 | **SIIX EMS México** | Llamar al **+52 444 298-9130** y preguntar por el correo de **Cathy Cornejo, Compras Directas**. El dominio ya está confirmado: `@siix-global.com`. Solo falta la ortografía del nombre. Ni ZoomInfo ni Wiza la tienen. |
| 2 | **Turck Duotec** | ¿Turck México (Coahuila) o Duotec Group? Son empresas distintas. |
| 3 | **Electromax** | ¿San José CA o la planta de Orange County? |
| 4 | **Re-export del CRM sin truncar** | 41% de las URLs vienen cortadas. Es gratis y desbloquea varios cientos de los 3,262 sin clasificar. **La acción de mayor retorno pendiente.** |
| 5 | **31 posibles duplicados** | Moog GmbH vs Moog Inc, Rheinmetall, Zollner, Finisar/Coherent. Pueden ser plantas distintas — requiere criterio. |
| 6 | **Fase 2 de Tsunami** | Quedan 579 EMS/OEM sin comprar. Decidir con los resultados del lote de prueba en la mano. |

## Lo aprendido (aplica a todo lo que sigue)

- **El dominio de la matriz no sirve para la planta local.** Causa del rebote de SIIX: los correos eran `@siix.co.jp` (Japón) cuando el personal mexicano usa `@siix-global.com`. Hay 18 casos más del mismo patrón en los estudios — Jatco, Marquardt México, Hyundai Mobis, Astemo, Aisan, Ichimiya, Pollmann.
- **ZoomInfo en México: depende del tamaño.** Funciona en multinacionales con planta aquí (Molex, Siemens, Denso, Honeywell, Sony, Ford). Falla en EMS mexicanos chicos: tiene nombre y puesto correctos pero **sin correo** (SIIX, TKR, Bunker, Firstronic, Mextronics, Falco). Para esos, teléfono o LinkedIn.
- **La geografía no se infiere del dominio.** ASI y CE3 son canadienses, Anand y EME de India, Hensoldt alemana, Scanfil y Fideltronik polacas, CBL italiana — todas venían marcadas US. Segmentar campañas por TLD mandaría copy en español a Polonia.
- **Los estudios propios le ganan a ZoomInfo para elegir al comprador**, porque traen la bandera `¿Electrónica?` y puestos como *PCB Buyer* o *Senior Electronics Commodity Buyer* que ZoomInfo no distingue. ZoomInfo gana en verificar el correo.
