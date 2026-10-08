// Plan de marketing CLT México → Latinoamérica: fuente del Excel (src/generar-plan-marketing.py), español e inglés.
// Cifras de presupuesto y metas: estimación a validar con CLT.

const es = {
  meta: {
    file: "Plan_Marketing_CLT_Mexico_Latam_ES",
    title: "Plan de Marketing CLT",
    subtitle: "Posicionar la impresión híbrida textil de CLT como la n.º 1 en México y llevarla a Latinoamérica",
    preparedBy: "Preparado por: TID México · VSP Printing, Inc. · CEB",
    preparedFor: "Para: socios del grupo y CLT",
    date: "Octubre 2026",
    conf: "Documento confidencial",
    contact: "Contacto: Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
    footer: "Plan de marketing CLT — TID / VSP / CEB — Confidencial",
    estimateNote: "Nota: metas y presupuestos son estimaciones propias; se ajustarán con la cotización de CLT y los primeros 6 meses de resultados.",
  },
  body: [
    { h1: "1. Resumen ejecutivo" },
    { p: "Objetivo: que en 24 meses CLT sea la marca de referencia en impresión híbrida textil (serigrafía + digital) en México, la primera que piense un estampador o una maquila de exportación cuando quiera diferenciarse, y que en el año 3 repliquemos el modelo en Latinoamérica." },
    { bullets: [
      "Hoy nadie es dueño de la categoría en México: no hay distribuidor formal de híbridos chinos y la competencia en tintas compite por precio (ScreenTec) o por aprobaciones de marca (Avient). El primero que eduque al mercado se queda con la categoría.",
      "Posicionamiento: «Serigrafía + digital en un solo paso, con química y servicio en México». No vendemos una máquina: vendemos color ilimitado al costo de la serigrafía, efectos que el DTF no logra y un socio técnico local.",
      "Estrategia: marketing por cuentas (ABM) sobre las 17 cuentas del 80/20, sala de demostración como motor de ventas, contenido visual que muestre los efectos, ferias clave y consumibles como puerta de entrada.",
      "Metas: 2 · 5 · 8 líneas híbridas en los años 1–3, 30 talleres comprando consumibles en el año 1 y el 60% de las cuentas prioritarias con demostración o prueba en su tela.",
      "Presupuesto de marketing año 1: ~US$50 mil (US$20 mil ya incluidos en la inversión de lanzamiento); proponemos que CLT cofinancie una parte con un fondo cooperativo.",
    ] },

    { h1: "2. Punto de partida" },
    { table: {
      cols: ["Tema", "Lo que sabemos", "Implicación para marketing"],
      widths: [1900, 3800, 3660],
      rows: [
        ["Mercado", "102,492 unidades económicas textiles; ~1,400–1,900 empresas alcanzables; 82 prospectos identificados (47 estampadores/fabricantes y 35 OEM)", "Mercado concentrado: pocas cuentas grandes deciden el volumen; marketing de precisión, no masivo"],
        ["Contexto", "Aranceles 2026 de hasta 35% a prendas de países sin tratado; las maquilas buscan valor agregado y tirajes cortos", "Mensaje de oportunidad: producir aquí lo que antes se importaba, con efectos premium"],
        ["Competencia", "Kornit (DTG alto costo), pulpos M&R/ROQ/MHM, Avient y Matsui en tintas premium, ScreenTec y marcas económicas en precio, DTF en tirajes cortos", "Diferenciarnos por solución completa y servicio, no por precio"],
        ["Marca CLT", "Fabricante chino listado en bolsa, poco conocido en México", "Construir confianza: pruebas en la tela del cliente, casos, sala demo y servicio local"],
        ["Grupo", "TID (12 años, Querétaro), VSP (20+ años, California), CEB (importación)", "Credibilidad local y cobertura frontera; marca paraguas «CLT por TID»"],
      ],
    } },

    { h1: "3. Objetivos" },
    { table: {
      bold: true,
      cols: ["Indicador", "Año 1", "Año 2", "Año 3"],
      widths: [3960, 1800, 1800, 1800],
      rows: [
        ["Líneas híbridas instaladas (acumulado)", "2", "7", "15"],
        ["Talleres comprando consumibles CLT", "30", "70", "120"],
        ["Cuentas 80/20 con demo o prueba en su tela", "10 de 17", "17 de 17", "+ Latam"],
        ["Leads calificados (MQL)", "300", "600", "900"],
        ["Demostraciones realizadas", "40", "80", "120"],
        ["Conocimiento de marca en cuentas prioritarias", "60%", "85%", "90%"],
        ["Países con presencia", "México", "México + EE. UU. (VSP)", "+ 2–3 países Latam"],
      ],
    } },
    { note: "Líneas por año: 2, 5 y 8 (igual que la propuesta a CLT). Consumibles: incluye talleres sin máquina CLT. Estimación a validar." },

    { h1: "4. Mercado meta y segmentos" },
    { table: {
      cols: ["Segmento", "Quiénes", "Qué necesitan", "Mensaje", "Prioridad"],
      widths: [1700, 2200, 2000, 2360, 1100],
      rows: [
        ["OEM de exportación", "Maquilas con serigrafía en Baja California, Puebla, Yucatán, Nuevo León (Ink Throwers, MD International, Vertical Knits, Codipsa)", "Volumen, calidad constante, efectos para marcas de EE. UU., cumplimiento químico", "«Efectos premium a velocidad de pulpo, con soporte en México»", "1"],
        ["Estampadores industriales", "Maquila de serigrafía por volumen (ADN, KW, SerigrafiarteSP)", "Bajar costo por pieza, quitar cambios de pantalla, ganar clientes nuevos", "«Color ilimitado al costo de la serigrafía»", "1"],
        ["Deportivo, uniformes y licencias", "Charly, Diermi, Uniformes Carmen, Reitex", "Nombres y números variables, sublimado sobre algodón oscuro, campañas", "«Personaliza cada pieza sin parar la línea»", "2"],
        ["Marcas de moda y diseño", "Marcas nacionales y diseñadores", "Diferenciación: silicona vidrio, efecto bordado, 3D", "«Lo que tu competencia no puede imprimir»", "2"],
        ["Talleres medianos", "Talleres con pulpo manual o automático", "Mejores siliconas y pastas, capacitación", "«Química profesional con asesoría técnica»", "3 (consumibles)"],
      ],
    } },

    { h1: "5. Compradores: quién decide y qué le decimos" },
    { table: {
      cols: ["Perfil", "Le importa", "Le mostramos", "Objeción típica → respuesta"],
      widths: [1700, 2400, 2560, 2700],
      rows: [
        ["Dueño / director general", "Retorno, riesgo, flujo de efectivo", "Calculadora de retorno con sus números; inversión por etapas; financiamiento", "«Es mucho dinero» → estación digital sobre su pulpo actual primero"],
        ["Gerente de planta / producción", "Piezas por hora, paros, mano de obra", "Demo con 400+ piezas/hora; menos pantallas y cambios", "«Mis operadores no saben» → capacitación incluida y técnico local"],
        ["Ingeniería / procesos", "Estabilidad, curado, lavado, mantenimiento", "Fichas técnicas, pruebas de lavado, plan de mantenimiento", "«Cabezales chinos fallan» → refacciones en México y póliza de servicio"],
        ["Compras", "Precio, crédito, entrega, proveedor confiable", "Inventario local (CEB), precio en pesos, crédito a 30–60 días", "«ScreenTec es más barato» → costo por pieza y efectos que ellos no tienen"],
        ["Diseño", "Libertad creativa, efectos nuevos", "Muestrario físico, recetas de efectos, prueba con su diseño", "«No sé si se ve bien en tela» → muestra con su arte en 72 horas"],
      ],
    } },

    { h1: "6. Posicionamiento y marca" },
    { h2: "Declaración de posicionamiento" },
    { p: "Para estampadores y maquilas que necesitan diferenciarse sin perder volumen, CLT por TID es la única solución híbrida llave en mano en México: máquina, química y servicio local que combinan el costo de la serigrafía con el color ilimitado del digital y efectos especiales que el DTF no logra." },
    { h2: "Frases propuestas (a probar con clientes)" },
    { bullets: [
      "«Serigrafía + digital. Un solo paso.» (principal)",
      "«Imprime lo que antes era imposible.» (efectos especiales)",
      "«Color ilimitado al costo de la serigrafía.» (retorno)",
    ] },
    { h2: "Tres pilares de mensaje y sus pruebas" },
    { table: {
      cols: ["Pilar", "Promesa", "Pruebas"],
      widths: [2000, 3400, 3960],
      rows: [
        ["Productividad", "Más piezas por hora y menos costo por pieza", "400–450 piezas/hora; 40–70% menos tinta que DTG; tiraje rentable desde 500 piezas"],
        ["Diferenciación", "Efectos que venden más caro", "Silicona tipo vidrio, efecto bordado, 3D, foil, descarga; muestrario físico"],
        ["Respaldo local", "Un socio, no un importador", "Sala demo en Querétaro, técnicos TID/VSP, inventario CEB, capacitación y garantía"],
      ],
    } },
    { h2: "Arquitectura de marca" },
    { bullets: [
      "Marca de producto: CLT (respetando su identidad y guía de marca).",
      "Respaldo: «Distribuidor oficial en México: TID México · VSP · CEB». En comunicación local: «CLT por TID».",
      "Nombre del programa de capacitación: «Academia Híbrida CLT» (certificación de operadores; genera lealtad y consumo de química).",
    ] },

    { h1: "7. Mezcla de marketing" },
    { table: {
      cols: ["Elemento", "Decisión"],
      widths: [1900, 7460],
      rows: [
        ["Producto", "Tres paquetes: Inicio (química + estación digital sobre el pulpo del cliente), Pro (pulpo + estación híbrida + química + póliza) y Completo (línea con DTG). Siempre con instalación, capacitación y servicio."],
        ["Precio", "Precio por valor (costo por pieza), en pesos y dólares. Programa «Clientes fundadores»: condiciones especiales para los primeros 5 compradores a cambio de caso de éxito y visitas a su planta. Financiamiento o arrendamiento con terceros y química en consignación para cuentas clave."],
        ["Plaza", "Venta directa a cuentas 80/20 (vendedor + dirección). Sala demo en Querétaro; frontera atendida con VSP; consumibles por pedido directo, tienda en línea B2B y, desde el año 2, 2–3 distribuidores de química en Guadalajara, Puebla y León."],
        ["Promoción", "ABM, demostraciones, ferias, contenido visual, LinkedIn, WhatsApp, relaciones públicas y referidos (detalle en secciones 9–12)."],
      ],
    } },

    { h1: "8. Plan por fases en México" },
    { table: {
      cols: ["Fase", "Meses", "Objetivo", "Acciones clave"],
      widths: [1700, 1100, 2400, 4160],
      rows: [
        ["0. Preparar", "0–3", "Tener todo listo para vender", "Kit de marca en español, página web /clt, catálogo y fichas, videos de efectos, muestrario físico, CRM y WhatsApp Business, calculadora de retorno, lista de 82 cuentas con contactos"],
        ["1. Lanzar", "3–9", "Que el mercado sepa que existimos", "Inauguración de la sala demo, FESPA México, ABM a las 17 cuentas, primeros 2 «clientes fundadores», lanzamiento de siliconas y pastas a talleres"],
        ["2. Probar y escalar", "9–18", "Convertir pruebas en ventas", "Casos de éxito en video, «Días Híbridos» en Guadalajara, León, Puebla, Monterrey, Tijuana y Mérida, webinars mensuales, programa de referidos, Academia Híbrida"],
        ["3. Liderar", "18–36", "Ser la referencia de la categoría", "Ponencias en ferias y cámaras, alianzas con escuelas de diseño, distribuidores de química, comunidad de clientes, salto a Latinoamérica"],
      ],
    } },

    { h1: "9. Marketing por cuentas (ABM) para las 17 cuentas 80/20" },
    { bullets: [
      "Paso 1 — Investigar: mapa de cada cuenta (decisores, marcas que surte, equipo instalado, procesos que terceriza).",
      "Paso 2 — Muestra personalizada: imprimir su propio diseño (o el de una marca que surten) con efectos híbridos y entregarlo en caja con calculadora de retorno a su volumen. Costo aproximado: US$150–250 por cuenta.",
      "Paso 3 — Visita y demo: invitación a la sala demo o demostración en su planta con su tela.",
      "Paso 4 — Prueba piloto: corrida corta en producción real con técnico CLT/TID; medir costo por pieza y calidad.",
      "Paso 5 — Propuesta: paquete a la medida con financiamiento; si es «cliente fundador», condiciones especiales.",
      "Seguimiento semanal en el CRM; meta: 10 de 17 cuentas con demo o prueba en el año 1.",
    ] },

    { h1: "10. Canales y tácticas" },
    { table: {
      cols: ["Canal", "Para qué", "Táctica", "Indicador"],
      widths: [1700, 2200, 3660, 1800],
      rows: [
        ["Sala de demostración", "Cerrar ventas", "Demos agendadas, pruebas con tela del cliente, talleres de efectos", "Demos/mes; % que pasa a propuesta"],
        ["LinkedIn", "Llegar a decisores de OEM", "Perfil de empresa y del director, casos, videos cortos; anuncios a cargos de planta y compras", "Leads de OEM; reuniones"],
        ["Instagram, TikTok y YouTube", "Mostrar los efectos", "Reels de antes/después, «cómo se hizo», efecto vidrio y bordado de cerca", "Alcance; mensajes recibidos"],
        ["WhatsApp Business", "Atención y reabasto", "Catálogo, listas de difusión de promociones, pedidos de consumibles", "Tiempo de respuesta; pedidos"],
        ["Sitio web y buscadores", "Captar búsquedas", "Página /clt con calculadora; contenido para «impresión híbrida textil», «silicona para serigrafía», «efecto bordado», «pasta base agua»", "Visitas; formularios"],
        ["Correo", "Nutrir prospectos", "Secuencia de 6 correos por perfil; boletín mensual con casos", "Apertura; clics; demos"],
        ["Ferias y Días Híbridos", "Volumen de contactos", "Demostración en vivo, muestras con el logo del visitante", "Leads por evento; costo por lead"],
        ["Relaciones públicas", "Credibilidad", "Prensa especializada en impresión y textil; cámaras CANAINTEX y CANAIVE", "Menciones; invitaciones"],
        ["Referidos", "Crecimiento orgánico", "Descuento en química por cliente referido que compre", "Ventas referidas"],
      ],
    } },

    { h1: "11. Contenido" },
    { table: {
      cols: ["Pilar de contenido", "Formatos", "Frecuencia"],
      widths: [2600, 4960, 1800],
      rows: [
        ["Efectos que venden", "Reels de 15–30 s, fotos macro, muestrario", "3 por semana"],
        ["Números que convencen", "Calculadora de retorno, comparativos costo por pieza vs. DTF y DTG", "1 al mes"],
        ["Casos de clientes", "Video de 2 minutos en planta, ficha de caso", "1 por trimestre (desde el mes 9)"],
        ["Academia Híbrida", "Webinars, guías técnicas, recetas de efectos, certificación", "1 webinar al mes"],
        ["Detrás de la marca", "Planta CLT, equipo técnico, sala demo, ferias", "2 al mes"],
      ],
    } },
    { note: "Todo el contenido en español; versión en inglés para VSP y cuentas OEM con matriz en EE. UU." },

    { h1: "12. Eventos y ferias" },
    { table: {
      cols: ["Evento", "Dónde", "Para qué", "Año"],
      widths: [2800, 1900, 3360, 1300],
      rows: [
        ["FESPA México", "Ciudad de México", "Lanzamiento con línea híbrida en operación", "1, 2, 3"],
        ["Inauguración sala demo", "Querétaro", "Evento con las 17 cuentas, cámaras y prensa", "1"],
        ["Días Híbridos (roadshow)", "Guadalajara, León, Puebla, Monterrey, Tijuana, Mérida", "Demos en la planta de un cliente o aliado local", "1–2"],
        ["Intermoda", "Guadalajara", "Marcas de moda y diseñadores", "2"],
        ["PRINTING United", "EE. UU.", "Cuentas OEM con matriz en EE. UU., junto con VSP y CLT", "1, 2, 3"],
        ["Apparel Sourcing Show", "Guatemala", "Entrada a Centroamérica", "2–3"],
        ["Colombiatex de las Américas", "Medellín", "Entrada a Colombia y región andina", "3"],
        ["Perú Moda", "Lima", "Entrada a Perú", "3"],
      ],
    } },
    { note: "Fechas por confirmar en cada calendario anual." },

    { h1: "13. Embudo comercial año 1" },
    { table: {
      bold: true,
      cols: ["Etapa", "Meta año 1", "Conversión", "Responsable"],
      widths: [3160, 1800, 1800, 2600],
      rows: [
        ["Contactos generados (ferias, digital, ABM)", "900", "—", "Marketing"],
        ["Leads calificados (MQL)", "300", "33%", "Marketing + atención al cliente"],
        ["Demostraciones o pruebas", "40", "13%", "Vendedor + técnico"],
        ["Propuestas formales", "12", "30%", "Vendedor"],
        ["Líneas híbridas vendidas", "2", "17%", "Dirección + vendedor"],
        ["Talleres con consumibles", "30", "10% de los MQL", "Atención al cliente"],
      ],
    } },

    { h1: "14. Presupuesto de marketing (estimación)" },
    { table: {
      bold: true,
      cols: ["Concepto", "Año 1", "Año 2", "Año 3"],
      widths: [4560, 1600, 1600, 1600],
      rows: [
        ["Identidad, web, catálogo y fichas técnicas", "US$6k", "US$3k", "US$4k"],
        ["Video y fotografía (efectos, demos, casos)", "US$5k", "US$6k", "US$6k"],
        ["Kits de muestras ABM y muestrario", "US$6k", "US$7k", "US$8k"],
        ["Ferias (stand, traslado de máquina, viáticos)", "US$18k", "US$25k", "US$32k"],
        ["Inauguración sala demo y Días Híbridos", "US$6k", "US$8k", "US$8k"],
        ["Publicidad digital (LinkedIn, Meta, YouTube, Google)", "US$5k", "US$9k", "US$12k"],
        ["Herramientas (CRM, WhatsApp, correo)", "US$1.5k", "US$2k", "US$3k"],
        ["Imprevistos", "US$2.5k", "US$5k", "US$7k"],
        ["Total", "US$50k", "US$65k", "US$80k"],
      ],
    } },
    { p: "Del año 1, US$20 mil ya están en la inversión inicial (concepto «Lanzamiento») y parte de las ferias en el gasto de operación de la propuesta. El año 3 incluye la entrada a Latinoamérica. Proponemos pedir a CLT un fondo cooperativo de marketing equivalente al 3–5% de las compras del distribuidor." },

    { h1: "15. Indicadores y seguimiento" },
    { bullets: [
      "Tablero mensual: leads por canal, costo por lead, demos, propuestas, ventas, ventas de consumibles y recompra.",
      "Indicadores de negocio: costo de adquisición por línea, ingreso de consumibles por línea instalada, satisfacción del cliente (encuesta NPS) a 90 días.",
      "Indicadores de marca: seguidores y alcance, menciones en prensa, búsquedas de «CLT» e «impresión híbrida» en México.",
      "Revisión trimestral con CLT: resultados, ajustes de mensaje y presupuesto, uso del fondo cooperativo.",
    ] },

    { h1: "16. Expansión a Latinoamérica" },
    { table: {
      cols: ["Ola", "Cuándo", "Países", "Por qué", "Cómo entramos"],
      widths: [1000, 1300, 2100, 2760, 2200],
      rows: [
        ["1", "Año 2–3", "El Salvador, Honduras, Guatemala", "Maquila de exportación con serigrafía para marcas de EE. UU. (Hanes, Gildan, Tegra); cerca de México", "Venta directa desde México + técnico itinerante; Apparel Sourcing Show"],
        ["2", "Año 3", "Perú y Colombia", "Algodón y tejido de punto de exportación (Topy Top, Textiles Camones); ferias fuertes", "Agente o distribuidor local con soporte técnico de TID; Colombiatex y Perú Moda"],
        ["3", "Año 3–4", "República Dominicana, Haití y resto de Sudamérica", "Zonas francas con serigrafía (Gildan, Hansae)", "Desde Centroamérica y VSP; distribuidores de química"],
      ],
    } },
    { bullets: [
      "Condición para entrar: México con al menos 5 líneas instaladas y casos de éxito documentados.",
      "Se reutiliza todo el material en español; ajustes locales por país (precios, crédito, logística).",
      "Prospectos ya identificados: 122 empresas en Centroamérica, Caribe y Sudamérica (27 de prioridad A).",
    ] },

    { h1: "17. Lo que pedimos a CLT para el marketing" },
    { bullets: [
      "Uso de marca, guía de identidad y material original (fotos, videos, fichas técnicas) para adaptarlo al español.",
      "Fondo cooperativo de marketing del 3–5% de las compras del distribuidor.",
      "Máquina de demostración en consignación o con descuento para la sala demo y las ferias.",
      "Presencia de un ingeniero de CLT en el lanzamiento y en FESPA México.",
      "Certificados químicos para OEM (por ejemplo OEKO-TEX ECO PASSPORT o ZDHC) y pruebas de lavado, si los tiene.",
      "Canalización a TID / CEB de todos los prospectos de México y Latinoamérica que lleguen a CLT.",
    ] },

    { h1: "18. Riesgos del plan" },
    { table: {
      cols: ["Riesgo", "Mitigación"],
      widths: [3900, 5460],
      rows: [
        ["Desconfianza hacia maquinaria china", "Pruebas en la tela del cliente, casos locales, garantía y refacciones en México"],
        ["Ciclo de venta largo en OEM (aprobación de marcas)", "Empezar por consumibles y estaciones digitales; usar la aprobación de un cliente para abrir a otros de la misma marca"],
        ["Presupuesto limitado", "Concentrar el 80% del gasto en las 17 cuentas y en la sala demo; fondo cooperativo de CLT"],
        ["Guerra de precios en consumibles", "Vender costo por pieza y asesoría técnica, no precio por kilo"],
        ["Dependencia de una sola persona de ventas", "CRM al día, materiales estandarizados y capacitación cruzada con TID"],
      ],
    } },

    { h1: "19. Calendario de los primeros 12 meses" },
    { table: {
      cols: ["Trimestre", "Marketing", "Ventas"],
      widths: [1500, 4260, 3600],
      rows: [
        ["T1 (meses 1–3)", "Kit de marca, web /clt, videos, muestrario, CRM, calculadora de retorno", "Contactos de las 82 cuentas; primeros envíos de muestras a las 17 cuentas"],
        ["T2 (meses 4–6)", "Inauguración de la sala demo, campaña LinkedIn e Instagram, primer webinar", "10 demos; lanzamiento de consumibles a talleres"],
        ["T3 (meses 7–9)", "FESPA México, Días Híbridos en Guadalajara y León", "Primer «cliente fundador»; 20 talleres con consumibles"],
        ["T4 (meses 10–12)", "Primer caso de éxito en video, Días Híbridos en Puebla y Tijuana, plan del año 2", "Segunda línea; 30 talleres con consumibles; plan Latam"],
      ],
    } },
  ],
};

const en = {
  meta: {
    file: "CLT_Marketing_Plan_Mexico_Latam_EN",
    title: "CLT Marketing Plan",
    subtitle: "Making CLT’s hybrid textile printing No. 1 in Mexico and taking it to Latin America",
    preparedBy: "Prepared by: TID México · VSP Printing, Inc. · CEB",
    preparedFor: "For: group partners and CLT",
    date: "October 2026",
    conf: "Confidential document",
    contact: "Contact: Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
    footer: "CLT marketing plan — TID / VSP / CEB — Confidential",
    estimateNote: "Note: targets and budgets are our own estimates; they will be adjusted with CLT’s quotation and the first 6 months of results.",
  },
  body: [
    { h1: "1. Executive summary" },
    { p: "Goal: within 24 months, make CLT the reference brand for hybrid textile printing (screen + digital) in Mexico, the first name a printer or export contractor thinks of when they want to stand out, and replicate the model in Latin America in year 3." },
    { bullets: [
      "Nobody owns the category in Mexico today: there is no formal distributor of Chinese hybrids, and ink competitors fight on price (ScreenTec) or on brand approvals (Avient). Whoever educates the market first owns the category.",
      "Positioning: “Screen + digital in one pass, with chemistry and service in Mexico.” We do not sell a machine: we sell unlimited color at screen printing cost, effects DTF cannot achieve and a local technical partner.",
      "Strategy: account-based marketing (ABM) on the 17 accounts in the 80/20, the demo room as the sales engine, visual content that shows the effects, key trade shows and consumables as the entry point.",
      "Targets: 2 · 5 · 8 hybrid lines in years 1–3, 30 shops buying consumables in year 1 and 60% of priority accounts with a demo or test on their fabric.",
      "Year-1 marketing budget: ~US$50k (US$20k already in the launch investment); we propose CLT co-funds part through a co-op fund.",
    ] },

    { h1: "2. Starting point" },
    { table: {
      cols: ["Topic", "What we know", "Marketing implication"],
      widths: [1900, 3800, 3660],
      rows: [
        ["Market", "102,492 textile businesses; ~1,400–1,900 reachable companies; 82 prospects identified (47 printers/manufacturers and 35 OEMs)", "Concentrated market: a few large accounts drive volume; precision marketing, not mass marketing"],
        ["Context", "2026 tariffs of up to 35% on apparel from countries without a trade agreement; contractors seek added value and short runs", "Opportunity message: produce here what used to be imported, with premium effects"],
        ["Competition", "Kornit (high-cost DTG), M&R/ROQ/MHM carousels, Avient and Matsui in premium inks, ScreenTec and budget brands on price, DTF in short runs", "Differentiate on the complete solution and service, not price"],
        ["CLT brand", "Listed Chinese manufacturer, little known in Mexico", "Build trust: tests on the customer’s fabric, cases, demo room and local service"],
        ["Group", "TID (12 years, Querétaro), VSP (20+ years, California), CEB (importer)", "Local credibility and border coverage; umbrella brand “CLT by TID”"],
      ],
    } },

    { h1: "3. Objectives" },
    { table: {
      bold: true,
      cols: ["Metric", "Year 1", "Year 2", "Year 3"],
      widths: [3960, 1800, 1800, 1800],
      rows: [
        ["Hybrid lines installed (cumulative)", "2", "7", "15"],
        ["Shops buying CLT consumables", "30", "70", "120"],
        ["80/20 accounts with a demo or test on their fabric", "10 of 17", "17 of 17", "+ Latam"],
        ["Marketing-qualified leads (MQL)", "300", "600", "900"],
        ["Demos delivered", "40", "80", "120"],
        ["Brand awareness among priority accounts", "60%", "85%", "90%"],
        ["Countries with presence", "Mexico", "Mexico + U.S. (VSP)", "+ 2–3 Latam countries"],
      ],
    } },
    { note: "Lines per year: 2, 5 and 8 (same as the proposal to CLT). Consumables include shops without a CLT machine. Estimate to be validated." },

    { h1: "4. Target market and segments" },
    { table: {
      cols: ["Segment", "Who", "What they need", "Message", "Priority"],
      widths: [1700, 2200, 2000, 2360, 1100],
      rows: [
        ["Export OEMs", "Contractors with screen printing in Baja California, Puebla, Yucatán, Nuevo León (Ink Throwers, MD International, Vertical Knits, Codipsa)", "Volume, consistent quality, effects for U.S. brands, chemical compliance", "“Premium effects at carousel speed, supported in Mexico”", "1"],
        ["Industrial printers", "Volume contract screen printers (ADN, KW, SerigrafiarteSP)", "Lower cost per piece, fewer screen changes, new customers", "“Unlimited color at screen printing cost”", "1"],
        ["Sports, uniforms and licensing", "Charly, Diermi, Uniformes Carmen, Reitex", "Variable names and numbers, full color on dark cotton, campaigns", "“Personalize every piece without stopping the line”", "2"],
        ["Fashion brands and designers", "Domestic brands and designers", "Differentiation: glass silicone, embroidery effect, 3D", "“What your competitors can’t print”", "2"],
        ["Mid-size shops", "Shops with manual or automatic carousels", "Better silicones and pastes, training", "“Professional chemistry with technical advice”", "3 (consumables)"],
      ],
    } },

    { h1: "5. Buyers: who decides and what we tell them" },
    { table: {
      cols: ["Profile", "Cares about", "We show", "Typical objection → answer"],
      widths: [1700, 2400, 2560, 2700],
      rows: [
        ["Owner / CEO", "Return, risk, cash flow", "ROI calculator with their numbers; phased investment; financing", "“Too much money” → digital station on their current carousel first"],
        ["Plant / production manager", "Pieces per hour, downtime, labor", "Demo at 400+ pieces/hour; fewer screens and changeovers", "“My operators don’t know how” → training included and local technician"],
        ["Engineering / process", "Stability, curing, washfastness, maintenance", "Data sheets, wash tests, maintenance plan", "“Chinese heads fail” → spare parts in Mexico and service contract"],
        ["Purchasing", "Price, credit, delivery, reliable supplier", "Local stock (CEB), peso pricing, 30–60 day credit", "“ScreenTec is cheaper” → cost per piece and effects they don’t have"],
        ["Design", "Creative freedom, new effects", "Physical swatch book, effect recipes, test with their artwork", "“Not sure how it looks on fabric” → sample with their art in 72 hours"],
      ],
    } },

    { h1: "6. Positioning and brand" },
    { h2: "Positioning statement" },
    { p: "For printers and contractors who need to stand out without losing volume, CLT by TID is the only turnkey hybrid solution in Mexico: machine, chemistry and local service that combine screen printing cost with unlimited digital color and special effects DTF cannot achieve." },
    { h2: "Proposed taglines (to test with customers)" },
    { bullets: [
      "“Screen + digital. One pass.” (main)",
      "“Print what used to be impossible.” (special effects)",
      "“Unlimited color at screen printing cost.” (ROI)",
    ] },
    { h2: "Three message pillars and their proof" },
    { table: {
      cols: ["Pillar", "Promise", "Proof"],
      widths: [2000, 3400, 3960],
      rows: [
        ["Productivity", "More pieces per hour, lower cost per piece", "400–450 pieces/hour; 40–70% less ink than DTG; profitable from 500 pieces"],
        ["Differentiation", "Effects that sell at a premium", "Glass-like silicone, embroidery effect, 3D, foil, discharge; physical swatch book"],
        ["Local backing", "A partner, not an importer", "Demo room in Querétaro, TID/VSP technicians, CEB stock, training and warranty"],
      ],
    } },
    { h2: "Brand architecture" },
    { bullets: [
      "Product brand: CLT (following its identity and brand guidelines).",
      "Endorsement: “Official distributor in Mexico: TID México · VSP · CEB”. In local communication: “CLT by TID”.",
      "Training program name: “CLT Hybrid Academy” (operator certification; builds loyalty and chemistry consumption).",
    ] },

    { h1: "7. Marketing mix" },
    { table: {
      cols: ["Element", "Decision"],
      widths: [1900, 7460],
      rows: [
        ["Product", "Three packages: Starter (chemistry + digital station on the customer’s carousel), Pro (carousel + hybrid station + chemistry + service contract) and Full (line with DTG). Always with installation, training and service."],
        ["Price", "Value-based pricing (cost per piece), in pesos and dollars. “Founding customers” program: special terms for the first 5 buyers in exchange for a case study and plant visits. Third-party financing or leasing and consignment chemistry for key accounts."],
        ["Place", "Direct sales to 80/20 accounts (salesperson + management). Demo room in Querétaro; border served with VSP; consumables by direct order, a B2B online store and, from year 2, 2–3 chemistry dealers in Guadalajara, Puebla and León."],
        ["Promotion", "ABM, demos, trade shows, visual content, LinkedIn, WhatsApp, PR and referrals (details in sections 9–12)."],
      ],
    } },

    { h1: "8. Phased plan in Mexico" },
    { table: {
      cols: ["Phase", "Months", "Goal", "Key actions"],
      widths: [1700, 1100, 2400, 4160],
      rows: [
        ["0. Prepare", "0–3", "Be ready to sell", "Spanish brand kit, /clt web page, catalog and data sheets, effect videos, physical swatch book, CRM and WhatsApp Business, ROI calculator, list of 82 accounts with contacts"],
        ["1. Launch", "3–9", "Let the market know we exist", "Demo room opening, FESPA México, ABM on the 17 accounts, first 2 “founding customers”, silicone and paste launch to shops"],
        ["2. Prove and scale", "9–18", "Turn tests into sales", "Video case studies, “Hybrid Days” in Guadalajara, León, Puebla, Monterrey, Tijuana and Mérida, monthly webinars, referral program, Hybrid Academy"],
        ["3. Lead", "18–36", "Own the category", "Talks at trade shows and chambers, design school partnerships, chemistry dealers, customer community, move into Latin America"],
      ],
    } },

    { h1: "9. Account-based marketing (ABM) for the 17 80/20 accounts" },
    { bullets: [
      "Step 1 — Research: map each account (decision makers, brands supplied, installed equipment, outsourced processes).",
      "Step 2 — Personalized sample: print their own design (or one from a brand they supply) with hybrid effects and deliver it in a box with an ROI calculation at their volume. Approx. cost: US$150–250 per account.",
      "Step 3 — Visit and demo: invitation to the demo room or a demo at their plant on their fabric.",
      "Step 4 — Pilot: short run in real production with a CLT/TID technician; measure cost per piece and quality.",
      "Step 5 — Proposal: tailored package with financing; special terms for “founding customers”.",
      "Weekly follow-up in the CRM; target: 10 of 17 accounts with a demo or test in year 1.",
    ] },

    { h1: "10. Channels and tactics" },
    { table: {
      cols: ["Channel", "Purpose", "Tactic", "Metric"],
      widths: [1700, 2200, 3660, 1800],
      rows: [
        ["Demo room", "Close sales", "Scheduled demos, tests on the customer’s fabric, effect workshops", "Demos/month; % to proposal"],
        ["LinkedIn", "Reach OEM decision makers", "Company and director profiles, case studies, short videos; ads to plant and purchasing roles", "OEM leads; meetings"],
        ["Instagram, TikTok and YouTube", "Show the effects", "Before/after reels, “how it was made”, close-ups of glass and embroidery effects", "Reach; inbound messages"],
        ["WhatsApp Business", "Service and reorders", "Catalog, broadcast lists for promotions, consumable orders", "Response time; orders"],
        ["Website and search", "Capture searches", "/clt page with calculator; content for “hybrid textile printing”, “screen printing silicone”, “embroidery effect”, “water-based paste” (in Spanish)", "Visits; forms"],
        ["Email", "Nurture prospects", "6-email sequence per profile; monthly newsletter with cases", "Opens; clicks; demos"],
        ["Trade shows and Hybrid Days", "Contact volume", "Live demo, samples printed with the visitor’s logo", "Leads per event; cost per lead"],
        ["Public relations", "Credibility", "Printing and textile trade press; CANAINTEX and CANAIVE chambers", "Mentions; invitations"],
        ["Referrals", "Organic growth", "Chemistry discount for each referred customer who buys", "Referred sales"],
      ],
    } },

    { h1: "11. Content" },
    { table: {
      cols: ["Content pillar", "Formats", "Frequency"],
      widths: [2600, 4960, 1800],
      rows: [
        ["Effects that sell", "15–30 s reels, macro photos, swatch book", "3 per week"],
        ["Numbers that convince", "ROI calculator, cost-per-piece comparisons vs. DTF and DTG", "1 per month"],
        ["Customer cases", "2-minute plant video, case sheet", "1 per quarter (from month 9)"],
        ["Hybrid Academy", "Webinars, technical guides, effect recipes, certification", "1 webinar per month"],
        ["Behind the brand", "CLT plant, technical team, demo room, trade shows", "2 per month"],
      ],
    } },
    { note: "All content in Spanish; English versions for VSP and OEM accounts headquartered in the U.S." },

    { h1: "12. Events and trade shows" },
    { table: {
      cols: ["Event", "Where", "Purpose", "Year"],
      widths: [2800, 1900, 3360, 1300],
      rows: [
        ["FESPA México", "Mexico City", "Launch with a hybrid line running", "1, 2, 3"],
        ["Demo room opening", "Querétaro", "Event with the 17 accounts, chambers and press", "1"],
        ["Hybrid Days (roadshow)", "Guadalajara, León, Puebla, Monterrey, Tijuana, Mérida", "Demos at a customer’s or local partner’s plant", "1–2"],
        ["Intermoda", "Guadalajara", "Fashion brands and designers", "2"],
        ["PRINTING United", "U.S.", "OEM accounts headquartered in the U.S., with VSP and CLT", "1, 2, 3"],
        ["Apparel Sourcing Show", "Guatemala", "Entry into Central America", "2–3"],
        ["Colombiatex de las Américas", "Medellín", "Entry into Colombia and the Andean region", "3"],
        ["Perú Moda", "Lima", "Entry into Peru", "3"],
      ],
    } },
    { note: "Dates to be confirmed in each year’s calendar." },

    { h1: "13. Year-1 sales funnel" },
    { table: {
      bold: true,
      cols: ["Stage", "Year-1 target", "Conversion", "Owner"],
      widths: [3160, 1800, 1800, 2600],
      rows: [
        ["Contacts generated (shows, digital, ABM)", "900", "—", "Marketing"],
        ["Marketing-qualified leads (MQL)", "300", "33%", "Marketing + customer service"],
        ["Demos or tests", "40", "13%", "Salesperson + technician"],
        ["Formal proposals", "12", "30%", "Salesperson"],
        ["Hybrid lines sold", "2", "17%", "Management + salesperson"],
        ["Shops buying consumables", "30", "10% of MQLs", "Customer service"],
      ],
    } },

    { h1: "14. Marketing budget (estimate)" },
    { table: {
      bold: true,
      cols: ["Item", "Year 1", "Year 2", "Year 3"],
      widths: [4560, 1600, 1600, 1600],
      rows: [
        ["Identity, website, catalog and data sheets", "US$6k", "US$3k", "US$4k"],
        ["Video and photography (effects, demos, cases)", "US$5k", "US$6k", "US$6k"],
        ["ABM sample kits and swatch book", "US$6k", "US$7k", "US$8k"],
        ["Trade shows (booth, machine transport, travel)", "US$18k", "US$25k", "US$32k"],
        ["Demo room opening and Hybrid Days", "US$6k", "US$8k", "US$8k"],
        ["Digital advertising (LinkedIn, Meta, YouTube, Google)", "US$5k", "US$9k", "US$12k"],
        ["Tools (CRM, WhatsApp, email)", "US$1.5k", "US$2k", "US$3k"],
        ["Contingency", "US$2.5k", "US$5k", "US$7k"],
        ["Total", "US$50k", "US$65k", "US$80k"],
      ],
    } },
    { p: "Of year 1, US$20k is already in the initial investment (“Launch” line) and part of the trade shows in the proposal’s operating expenses. Year 3 includes the Latin America entry. We propose asking CLT for a co-op marketing fund equal to 3–5% of the distributor’s purchases." },

    { h1: "15. Metrics and tracking" },
    { bullets: [
      "Monthly dashboard: leads by channel, cost per lead, demos, proposals, sales, consumables sales and repurchase.",
      "Business metrics: acquisition cost per line, consumables revenue per installed line, customer satisfaction (NPS survey) at 90 days.",
      "Brand metrics: followers and reach, press mentions, searches for “CLT” and “hybrid printing” in Mexico.",
      "Quarterly review with CLT: results, message and budget adjustments, use of the co-op fund.",
    ] },

    { h1: "16. Expansion into Latin America" },
    { table: {
      cols: ["Wave", "When", "Countries", "Why", "How we enter"],
      widths: [1000, 1300, 2100, 2760, 2200],
      rows: [
        ["1", "Years 2–3", "El Salvador, Honduras, Guatemala", "Export contractors with screen printing for U.S. brands (Hanes, Gildan, Tegra); close to Mexico", "Direct sales from Mexico + traveling technician; Apparel Sourcing Show"],
        ["2", "Year 3", "Peru and Colombia", "Export cotton and knitwear (Topy Top, Textiles Camones); strong trade shows", "Local agent or dealer with TID technical support; Colombiatex and Perú Moda"],
        ["3", "Years 3–4", "Dominican Republic, Haiti and rest of South America", "Free zones with screen printing (Gildan, Hansae)", "From Central America and VSP; chemistry dealers"],
      ],
    } },
    { bullets: [
      "Entry condition: Mexico with at least 5 installed lines and documented success cases.",
      "All Spanish material is reused; local adjustments per country (pricing, credit, logistics).",
      "Prospects already identified: 122 companies in Central America, the Caribbean and South America (27 priority A).",
    ] },

    { h1: "17. What we ask CLT for marketing" },
    { bullets: [
      "Brand use, identity guidelines and original material (photos, videos, data sheets) to adapt into Spanish.",
      "Co-op marketing fund of 3–5% of the distributor’s purchases.",
      "Demo machine on consignment or at a discount for the demo room and trade shows.",
      "A CLT engineer at the launch and at FESPA México.",
      "Chemical certificates for OEMs (e.g., OEKO-TEX ECO PASSPORT or ZDHC) and wash tests, if available.",
      "Routing to TID / CEB of all Mexico and Latin America prospects that reach CLT.",
    ] },

    { h1: "18. Plan risks" },
    { table: {
      cols: ["Risk", "Mitigation"],
      widths: [3900, 5460],
      rows: [
        ["Distrust of Chinese machinery", "Tests on the customer’s fabric, local cases, warranty and spare parts in Mexico"],
        ["Long OEM sales cycle (brand approvals)", "Start with consumables and digital stations; use one customer’s approval to open others supplying the same brand"],
        ["Limited budget", "Focus 80% of spend on the 17 accounts and the demo room; CLT co-op fund"],
        ["Price war in consumables", "Sell cost per piece and technical advice, not price per kilo"],
        ["Dependence on a single salesperson", "Up-to-date CRM, standard materials and cross-training with TID"],
      ],
    } },

    { h1: "19. First 12 months calendar" },
    { table: {
      cols: ["Quarter", "Marketing", "Sales"],
      widths: [1500, 4260, 3600],
      rows: [
        ["Q1 (months 1–3)", "Brand kit, /clt website, videos, swatch book, CRM, ROI calculator", "Contacts for the 82 accounts; first samples sent to the 17 accounts"],
        ["Q2 (months 4–6)", "Demo room opening, LinkedIn and Instagram campaign, first webinar", "10 demos; consumables launch to shops"],
        ["Q3 (months 7–9)", "FESPA México, Hybrid Days in Guadalajara and León", "First “founding customer”; 20 shops on consumables"],
        ["Q4 (months 10–12)", "First video case study, Hybrid Days in Puebla and Tijuana, year-2 plan", "Second line; 30 shops on consumables; Latam plan"],
      ],
    } },
  ],
};

module.exports = { es, en };
