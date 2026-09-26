# Estudio de mercado — Electrónica USA (SMT Specialist)

> Resumen e integración del estudio de mercado de la industria electrónica en EUA, enfocado en empresas con líneas SMT (Surface Mount Technology). Deliverable real en Excel + metodología reutilizable. Complementa el estudio de México.

## Deliverables (archivos Excel)

| Archivo | Contenido |
|---|---|
| **`US_Electronics_SMT_Study.xlsx`** | **148 empresas** + **63 contactos** (ZoomInfo, con email/teléfono) + hoja de import-data. 4 hojas: Directory, Contacts, Import Evidence, Notes. |
| **`Estudio_Electronica_Mexico.xlsx`** | **211 empresas** + **333 contactos**. Hojas: Directorio, Contactos. (Es el formato base que se replicó en inglés para USA.) |

> Pendiente: copiar estos .xlsx al repo (`02-Investigacion/electronica/`) desde el repo `Astute`/origen, o adjuntarlos, para tenerlos versionados en GrowProkure.

### Estructura del Directorio (columnas)
`Region · Company · Type · City · State · Address · Sector · SMT/PCBA Evidence · Confidence · Website · Source`

### Cobertura USA (148 empresas)
Por estado: CA 35 · TX 13 · AZ 11 · MA 9 · FL 8 · IL 8 · MN 7 · WI 6 · CO 6 + 21 estados más.
Incluye EMS grandes (Jabil, Sanmina, Flex, Benchmark, Plexus, Kimball, Key Tronic, SigmaTron, Nortech, Zentech) + PCBA regionales + OEM/semiconductores (TI, Microchip, onsemi, Amkor, Analog Devices, ADTRAN).

### Contactos (63, enriquecidos con email + teléfono)
Por función: **Purchasing/Sourcing 40 · Technical/Process Eng. 13 · Materials/Planning 10**. Accuracy 95–99%. Nota: 39 son US; el resto están en plantas overseas (columna "Likely Location" lo indica).

## Metodología (reutilizable — este es el valor a largo plazo)

### A) Mapa de fuentes de vacantes SMT (para monitoreo continuo)
- **Bolsas generales:** LinkedIn Jobs (~311 posts US live), Indeed, ZipRecruiter, Glassdoor, Built In.
- **Específicas de electrónica (mayor señal):** **SMTA Career Center**, **IPC / electronics.org**.
- **ATS (career pages a escala):** Ashby, Greenhouse, Lever, Workday — buscar "SMT".
- **Staffing especializado:** Blue Signal, Redline Group, ProTech.
- **Career pages EMS/OEM:** Jabil, Sanmina, Celestica, Flex, Benchmark, Plexus, Foxconn/FII, Kimball, SMTC.

### B) Datos de importación / aduana (encuentra a los employers reales)
Toda empresa con línea SMT importa equipo y materiales → registros de bill-of-lading (CBP) públicos. Buscar por HS code = lista de importadores US = employers objetivo.

| HS Code | Qué captura | Sirve para |
|---|---|---|
| **8486** | Máquinas de ensamble SMT / semiconductores | Compradores de equipo SMT |
| **8479.89** | Pick-and-place (algunos) | Importadores de máquinas SMT |
| **8534** | PCBs sin componentes | Fabricantes/ensambladores de PCB |
| **8542** | Circuitos integrados | Manufactura electrónica de alto volumen |
| **8537.10** | Tableros ensamblados (PCBA) | OEMs que importan sub-ensambles |
| **3810 / 3506** | Pasta/flux de soldadura, adhesivos | **Línea SMT ACTIVA** (consumibles = producen ahora) |

**Plataformas de trade-data:** ImportYeti (gratis), ImportGenius, Panjiva (S&P), Volza, USITC HTS (verificar códigos).
> Nota: la data gratuita de aduana es solo marítima (ocean BOL); aéreo y algunos carriers no aparecen. Buena muestra, no 100%.

## Cómo se conecta a GrowProkure

- **Capa 1 (Datos):** 148 empresas US + 211 MX + contactos = base real del vertical electrónica (lado demanda = compradores de componentes = clientes objetivo para Astute).
- **Capa 2 (Señales):** ⭐ Los **HS codes de consumibles (3810/3506)** son una señal poderosa: quien importa pasta de soldadura cada mes tiene línea SMT activa = comprador vivo de componentes. **Integrar al motor de señales.**
- **Capa 3 (Servicios):** los 63 contactos (Purchasing/Sourcing) alimentan directo las campañas del piloto Astute.

## Caveats (honestidad del estudio)
- Las vacantes vivas caducan rápido → el valor es el **mapa de fuentes** para monitoreo, no una lista congelada.
- Contactos cubren 13 de 148 empresas (se enfocaron créditos ZoomInfo en top EMS) → ampliable.
- Confidence column: High = confirmado/HQ conocido; Medium = verificar antes de outreach.

## Pendiente
- [ ] Versionar los 2 .xlsx en GrowProkure.
- [ ] Integrar HS codes 3810/3506 al motor de señales (`03-Producto/02-motor-de-senales.md`).
- [ ] Fusionar directorio US + MX en la base de datos maestra (Capa 1).
