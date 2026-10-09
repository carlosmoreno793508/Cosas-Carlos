// Contenido del documento (Word/PDF) en español e inglés.
// Bloques: { h1 }, { h2 }, { p }, { bullets: [] }, { table: { cols, rows, widths, bold? } }, { note }, { pagebreak: true }
// Las cifras marcadas como estimación deben reemplazarse con la cotización y condiciones reales de CLT.

const top8020 = require("./top8020");

// Cuentas prioritarias (regla 80/20), sección 7
function top8020Blocks(lang) {
  const es = lang === "es";
  const rows = (list) => list.map((r) => [r[0], r[1], es ? r[2] : r[3], es ? r[4] : r[5]]);
  const widths = [2200, 1500, 3860, 1800];
  return [
    { h2: es ? "Cuentas prioritarias: regla 80/20" : "Priority accounts: the 80/20 rule" },
    { p: es
      ? "De los 82 prospectos identificados en México (47 estampadores y fabricantes, y 35 OEM y maquiladoras), seleccionamos el 20% con mayor potencial: volumen de producción, decoración propia, exportación y encaje con la línea híbrida. Estas 17 cuentas recibirán el 80% del esfuerzo comercial del primer año (visitas, demostraciones y pruebas con su tela)."
      : "Out of the 82 prospects identified in Mexico (47 printers and manufacturers, and 35 OEMs and contract manufacturers), we selected the top 20% by potential: production volume, in-house decoration, exports and fit with the hybrid line. These 17 accounts will receive 80% of the first-year sales effort (visits, demos and tests on their own fabric)." },
    { h2: es ? "Prospectos prioritarios: estampadores y fabricantes (9 de 47)" : "Priority prospects: printers and manufacturers (9 of 47)" },
    { table: { cols: es ? ["Empresa", "Ciudad", "A qué se dedica", "Subsector"] : ["Company", "City", "What they do", "Subsector"], widths, rows: rows(top8020.prospects) } },
    { h2: es ? "OEM prioritarios: maquila de exportación (8 de 35)" : "Priority OEMs: export contract manufacturing (8 of 35)" },
    { table: { cols: es ? ["Empresa", "Ciudad", "A qué se dedica", "Marcas y clientes"] : ["Company", "City", "What they do", "Brands and customers"], widths, rows: rows(top8020.oems) } },
    { p: top8020.next[lang] },
    { note: es
      ? "Fuentes: sitios web de cada empresa, Open Supply Hub y directorios industriales. Marcas y clientes según fuentes públicas; confirmar en la primera visita."
      : "Sources: company websites, Open Supply Hub and industry directories. Brands and customers per public sources; to be confirmed at the first visit." },
  ];
}

const foda = require("./foda");

// FODA de la competencia (sección 8)
function fodaBlocks(lang) {
  const f = foda[lang];
  const L = f.ourLabels;
  return [
    { h2: f.inksTitle },
    { table: { cols: f.inksCols, widths: [2500, 2500, 2700, 1660], rows: f.inks } },
    { note: f.inksNote },
    { h2: f.swotTitle },
    { table: { cols: f.swotCols, widths: [1560, 1950, 1950, 1950, 1950], rows: f.swot } },
    { h2: f.ourTitle },
    { table: { cols: [L.F, L.D], widths: [4680, 4680], rows: [[f.our.F.join("\n"), f.our.D.join("\n")]] } },
    { table: { cols: [L.O, L.A], widths: [4680, 4680], rows: [[f.our.O.join("\n"), f.our.A.join("\n")]] } },
    { p: f.answer },
  ];
}

// Resumen del plan de marketing (sección 11); el plan completo está en Plan_Marketing_CLT_Mexico_Latam.xlsx
function marketingBlocks(lang) {
  const es = lang === "es";
  return [
    { h2: es ? "Plan de marketing (resumen)" : "Marketing plan (summary)" },
    { p: es
      ? "Objetivo: que en 24 meses CLT sea la marca de referencia en impresión híbrida textil en México y replicar el modelo en Latinoamérica en el año 3. Posicionamiento: «Serigrafía + digital en un solo paso, con química y servicio en México». No vendemos una máquina: vendemos color ilimitado al costo de la serigrafía, efectos que el DTF no logra y un socio técnico local."
      : "Goal: within 24 months, make CLT the reference brand for hybrid textile printing in Mexico and replicate the model in Latin America in year 3. Positioning: “Screen + digital in one pass, with chemistry and service in Mexico.” We do not sell a machine: we sell unlimited color at screen printing cost, effects DTF cannot achieve and a local technical partner." },
    { table: {
      cols: es ? ["Palanca", "Qué haremos"] : ["Lever", "What we will do"],
      widths: [2300, 7060],
      rows: es ? [
        ["Marketing por cuentas", "Muestra con el diseño de cada una de las 17 cuentas 80/20, calculadora de retorno, demo y prueba piloto en su tela"],
        ["Sala de demostración", "Querétaro como motor de ventas: demos, talleres de efectos y Academia Híbrida CLT (certificación de operadores)"],
        ["Contenido y digital", "Reels de efectos (vidrio, bordado, 3D), casos de clientes, LinkedIn para OEM, WhatsApp para consumibles"],
        ["Eventos", "FESPA México, inauguración de la sala demo, «Días Híbridos» en 6 ciudades y PRINTING United con VSP"],
        ["Oferta", "Paquetes Inicio, Pro y Completo; programa «Clientes fundadores» para los primeros 5 compradores; consumibles como puerta de entrada"],
      ] : [
        ["Account-based marketing", "Sample with each of the 17 80/20 accounts’ own design, ROI calculator, demo and pilot on their fabric"],
        ["Demo room", "Querétaro as the sales engine: demos, effect workshops and the CLT Hybrid Academy (operator certification)"],
        ["Content and digital", "Effect reels (glass, embroidery, 3D), customer cases, LinkedIn for OEMs, WhatsApp for consumables"],
        ["Events", "FESPA México, demo room opening, “Hybrid Days” in 6 cities and PRINTING United with VSP"],
        ["Offer", "Starter, Pro and Full packages; “founding customers” program for the first 5 buyers; consumables as the entry point"],
      ],
    } },
    { table: {
      bold: true,
      cols: es ? ["Meta y presupuesto", "Año 1", "Año 2", "Año 3"] : ["Targets and budget", "Year 1", "Year 2", "Year 3"],
      widths: [3960, 1800, 1800, 1800],
      rows: es ? [
        ["Leads calificados", "300", "600", "900"],
        ["Demostraciones", "40", "80", "120"],
        ["Talleres con consumibles CLT", "30", "70", "120"],
        ["Presupuesto de marketing", "US$50k", "US$65k", "US$80k"],
      ] : [
        ["Qualified leads", "300", "600", "900"],
        ["Demos", "40", "80", "120"],
        ["Shops buying CLT consumables", "30", "70", "120"],
        ["Marketing budget", "US$50k", "US$65k", "US$80k"],
      ],
    } },
    { p: es
      ? "Latinoamérica: ola 1 en El Salvador, Honduras y Guatemala (años 2–3), ola 2 en Perú y Colombia (año 3), con México como condición (5 líneas y casos documentados). Pedimos a CLT un fondo cooperativo de marketing del 3–5% de las compras, material de marca en español y apoyo de un ingeniero en el lanzamiento. Plan completo con calendario, presupuesto y tablero de indicadores en el Excel adjunto."
      : "Latin America: wave 1 in El Salvador, Honduras and Guatemala (years 2–3), wave 2 in Peru and Colombia (year 3), conditional on Mexico (5 lines and documented cases). We ask CLT for a co-op marketing fund of 3–5% of purchases, Spanish brand material and an engineer at the launch. Full plan with calendar, budget and KPI dashboard in the attached Excel workbook." },
    { note: es ? "Metas y presupuesto: estimación a validar con CLT." : "Targets and budget: estimate to be validated with CLT." },
  ];
}

const es = {
  meta: {
    file: "Propuesta_Distribucion_CLT_Mexico_ES",
    title: "Propuesta de Distribución CLT",
    subtitle: "Impresión híbrida textil (serigrafía + digital) — México y Latinoamérica",
    preparedBy: "Preparado por: TID México · VSP Printing, Inc. · CEB",
    preparedFor: "Para: Dongguan Changlian New Material Technology Co., Ltd. (CLT)",
    date: "Octubre 2026",
    conf: "Documento confidencial",
    contact: "Contacto: Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
    footer: "Propuesta TID / VSP / CEB para CLT — Confidencial",
    estimateNote:
      "Nota: las cifras marcadas como «estimación» son cálculos propios basados en fuentes públicas y deben confirmarse con la cotización y las condiciones comerciales de CLT.",
  },
  body: [
    { h1: "1. Resumen ejecutivo" },
    {
      p: "TID México, VSP Printing, Inc. y su subsidiaria CEB proponen a CLT (Dongguan Changlian New Material Technology Co., Ltd., SZSE 301618) convertirse en su distribuidor en México, con expansión a Estados Unidos y Latinoamérica. El objetivo es introducir y dar soporte local a las impresoras híbridas de CLT (serigrafía + digital) y a sus consumibles: siliconas, pastas base agua y tintas.",
    },
    {
      bullets: [
        "Oportunidad: no identificamos un distribuidor de impresión híbrida china con presencia formal en México (inventario, refacciones, técnicos y químicos locales).",
        "Mercado: ~102,500 unidades económicas textiles; ~1,400–1,900 clientes alcanzables (empresas medianas/grandes y talleres con pulpo automático); 30–90 líneas híbridas potenciales en 5 años (estimación).",
        "Momento: los aranceles de 2026 (hasta 35% a prendas de países sin tratado) favorecen al fabricante mexicano, que necesita diferenciarse con valor agregado y respuesta rápida.",
        "Socio: más de 30 años de experiencia combinada en impresión industrial, modelo de negocio basado en consumibles y servicio técnico, presencia en México (Querétaro) y EE. UU. (Los Ángeles), e importadora propia constituida en México (CEB).",
        "Inversión inicial propuesta (escenario base): ~US$262 mil, con recuperación estimada durante el año 3.",
      ],
    },
    { h1: "2. Alcance y metodología" },
    {
      p: "El estudio se centra en México como primera etapa; Estados Unidos y Latinoamérica se presentan como etapas de expansión. Se analizaron: el sitio internacional de CLT (garmentprintingpro.com), su reporte anual 2025, estadísticas de INEGI y CANAINTEX, información arancelaria pública y fuentes del sector (FESPA México, fabricantes y distribuidores).",
    },
    {
      table: {
        cols: ["Parámetro", "Contenido"],
        widths: [2600, 6760],
        rows: [
          ["Definición del mercado", "Equipos híbridos, consumibles (siliconas, pastas, tintas) y servicio técnico; tecnologías sustitutas: serigrafía tradicional, DTG, DTF, sublimación"],
          ["Segmentos", "Maquiladoras de exportación (IMMEX), marcas nacionales, talleres de serigrafía medianos/grandes, promocionales, uniformes y deportivos"],
          ["Dimensionamiento", "Mercado total, alcanzable y capturable (TAM / SAM / SOM) con escenarios conservador, base y optimista"],
          ["Geografía", "Clústeres: Edomex/CDMX, Jalisco, Puebla/Tlaxcala, Guanajuato, Baja California, La Laguna, Aguascalientes, Nuevo León, Yucatán"],
          ["Competencia", "Fabricantes y distribuidores de DTG, pulpos automáticos, híbridos chinos y consumibles"],
          ["Economía", "Inversión del distribuidor, márgenes, punto de equilibrio y retorno"],
          ["Regulación", "Aranceles 2026, importación vía CEB, T-MEC, NOM eléctricas"],
        ],
      },
    },
    { note: "Las cifras marcadas como «estimación» son cálculos propios y deben confirmarse con la cotización y condiciones de CLT." },

    { h1: "3. CLT: perfil del fabricante" },
    {
      p: "Dongguan Changlian New Material Technology Co., Ltd. (CLT) fue fundada en 2009 en Liaobu, Dongguan (Guangdong). Cotiza en el mercado ChiNext de la Bolsa de Shenzhen desde septiembre de 2024 (clave 301618). Es reconocida en China como líder en pastas de estampado base agua y ofrece una solución integral de materiales y equipos para el estampado textil.",
    },
    {
      table: {
        cols: ["Indicador 2025", "Valor", "Aprox. USD"],
        widths: [4360, 2600, 2400],
        rows: [
          ["Ingresos totales", "¥568.1 millones", "~US$80 M"],
          ["Pastas de estampado base agua", "¥304.4 M (53.6%)", "~US$43 M"],
          ["Materiales de silicona", "¥117.7 M (20.7%)", "~US$17 M"],
          ["Resinas base agua", "¥45.9 M (8.1%)", "~US$6 M"],
          ["Equipos de impresión", "¥37.0 M (6.5%)", "~US$5 M"],
          ["Ventas de exportación", "¥103.5 M (18.2%)", "~US$15 M"],
          ["Utilidad neta atribuible", "¥40.6 millones", "~US$6 M"],
          ["Canal: comercializadores / fabricantes", "49.5% / 50.5%", ""],
        ],
      },
    },
    { note: "Fuente: Reporte anual 2025 de CLT (Bolsa de Shenzhen). Tipo de cambio de referencia: ¥7.1 por US$." },
    { h2: "Portafolio relevante para esta propuesta" },
    {
      bullets: [
        "Impresoras híbridas: CLT-012R/015R/018R (cabezales Ricoh, hasta 1800 dpi, 450 pzs/h), CLT-014B/016B/018B (Brother 680, 400 pzs/h), CLT-005S (blanco Star Light).",
        "Pulpos ovalados automáticos: SM45-85, SM60-85, SM70-95 (hasta 800 pzs/h, ±0.02 mm).",
        "DTG de 6 estaciones con pretratamiento en línea y DTF industrial serie CLT-6900.",
        "Siliconas para efectos: alta densidad / 3D (S-1701), borde redondeado (S-1703), brillante tipo vidrio (S-1704-1), especial (S-1714-1); pastas base agua, espumantes y tintas DTG/DTF.",
        "Certificaciones: OEKO-TEX, GOTS, ISO 9001 e ISO 14001.",
      ],
    },
    { h2: "La tecnología híbrida" },
    {
      p: "Las estaciones digitales se montan sobre un pulpo ovalado de serigrafía. La base blanca se imprime con pasta de serigrafía (económica) y el color con cabezales digitales, lo que permite combinar en una sola pasada efectos de serigrafía (relieve, foil, glitter, descarga, silicona tipo vidrio o bordado) con degradados fotográficos. CLT indica ahorros de tinta de 40–70% frente a DTG puro y rentabilidad en tirajes de 500 a 5,000 piezas.",
    },

    { h1: "4. Modelo comercial de CLT" },
    {
      p: "CLT utiliza el equipo como puerta de entrada al consumo recurrente de químicos, que representa la mayor parte de sus ingresos. Su plan 2026 contempla reforzar el sudeste asiático y expandirse en Europa, América, Medio Oriente y África, completando su red de agentes en el extranjero.",
    },
    {
      table: {
        cols: ["Elemento", "Cómo lo aplica CLT"],
        widths: [2800, 6560],
        rows: [
          ["Ferias con demostración en vivo", "Línea funcionando, pruebas con la tela y el diseño del cliente, cotización escrita el mismo día, paquetes con precio de feria (PRINTING United, Stitch & Tex Egipto)"],
          ["Paquete llave en mano", "Máquina + química compatible + instalación + capacitación + flete y documentación de importación, a un solo precio"],
          ["Inversión por etapas", "Empezar con el pulpo y agregar estaciones digitales; planes de 2–3 temporadas"],
          ["Venta por retorno de inversión", "Ahorro de tinta, menos operadores y menos espacio; cálculo de ROI a la medida"],
          ["Consumibles vinculados", "La garantía requiere refacciones y químicos originales de CLT"],
          ["Laboratorio de aplicación", "Simula la producción del cliente y recomienda el proceso completo"],
          ["Captación digital", "Sitio multilingüe, formularios y WhatsApp con respuesta en menos de 2 horas"],
        ],
      },
    },
    {
      p: "Lo que hoy falta en México: servicio técnico local, inventario de refacciones y químicos en el país, atención en español y una sala de demostración. Estos son exactamente los elementos que aporta el grupo distribuidor.",
    },

    { pagebreak: true },
    { h1: "5. Mercado mexicano: panorama" },
    {
      table: {
        cols: ["Indicador", "Dato", "Fuente"],
        widths: [3000, 4160, 2200],
        rows: [
          ["PIB textil-confección", "$91,165 millones de pesos; 1.75% del PIB manufacturero", "CANAINTEX, cierre 2025"],
          ["Composición del PIB", "Prendas 56%, insumos y acabado textil 27%, productos textiles 17%", "CANAINTEX"],
          ["Unidades económicas", "102,492", "INEGI 2023"],
          ["Puestos de trabajo", "519,313 (225 mil formales)", "INEGI 2022 / CANAINTEX"],
          ["Tamaño de empresas", "Micro 95.6%, pequeñas 3.3%, medianas 0.8%, grandes 0.3%", "INEGI, Censo 2019"],
          ["Exportaciones", "US$9,300 millones; 89% a EE. UU.", "INEGI 2023"],
          ["Importaciones", "US$13,300 millones; 35% de China", "INEGI 2023"],
          ["Tendencia", "PIB -8.4% en 2023; ~20 mil empleos perdidos en 2024", "INEGI / FESPA"],
        ],
      },
    },
    {
      p: "La industria enfrenta presión por importaciones de bajo costo e informalidad. La respuesta del fabricante nacional es diferenciarse: personalización, tirajes cortos con entrega rápida y efectos de alto valor. La impresión híbrida responde directamente a esa necesidad. Los aranceles vigentes desde enero de 2026 refuerzan la posición de quien produce en México.",
    },

    { h1: "6. Tamaño del mercado (estimación)" },
    {
      table: {
        cols: ["Nivel", "Definición", "Tamaño estimado"],
        widths: [2000, 4760, 2600],
        rows: [
          ["Mercado total (TAM)", "Todas las unidades económicas textiles y de confección", "~102,500"],
          ["Mercado alcanzable (SAM)", "Empresas medianas y grandes (~1,130) más talleres de serigrafía con pulpo automático (300–800)", "~1,400–1,900 clientes"],
          ["Mercado capturable (SOM, 5 años)", "Adopción de 2–5% del mercado alcanzable", "~30–90 líneas híbridas"],
        ],
      },
    },
    {
      bullets: [
        "Equipos: 30–90 líneas × US$120–250 mil puestas en México = US$3.6–22 millones en 5 años (estimación; confirmar con cotización CLT).",
        "Consumibles: US$1,500–5,000 por línea al mes (hipótesis a validar con talleres). Con 50 líneas: US$0.9–3 millones anuales, más la venta de siliconas y pastas a talleres sin equipo híbrido.",
        "Referencia de precio de la competencia: pulpo automático M&R Cobra 10 estaciones / 8 colores, ~US$88 mil en EE. UU.",
      ],
    },

    { h1: "7. Zonas geográficas prioritarias" },
    {
      table: {
        cols: ["Prioridad", "Zona", "Motivo"],
        widths: [1300, 3000, 5060],
        rows: [
          ["1", "Estado de México y CDMX", "Mayor concentración de estampadores, marcas, promocionales y corporativo"],
          ["1", "Jalisco (Guadalajara, Zapotlanejo)", "Moda, ropa deportiva y marcas nacionales"],
          ["1", "Baja California (Tijuana, Ensenada, Tecate)", "Serigrafía de exportación para marcas de EE. UU. (Disney, Fanatics, Columbia); cobertura conjunta TID + VSP desde la frontera"],
          ["2", "Puebla y Tlaxcala", "Maquila de exportación y tejido de punto"],
          ["2", "Guanajuato (Moroleón, Uriangato, León)", "Tejido de punto y mayoreo; a 1–2 horas de TID en Querétaro"],
          ["3", "La Laguna, Aguascalientes, Nuevo León, Yucatán", "Mezclilla, maquila IMMEX y uniformes"],
        ],
      },
    },
    { note: "Priorización preliminar por concentración de industria mediana y grande; se validará con el directorio DENUE de INEGI." },
    ...top8020Blocks("es"),

    { h1: "8. Competencia" },
    {
      table: {
        cols: ["Tipo", "Participantes", "Observación"],
        widths: [2400, 3400, 3560],
        rows: [
          ["DTG / digital de alta gama", "Kornit (vía Sun Digital México)", "Líder en DTG; inversión alta; servicio establecido"],
          ["Pulpos automáticos", "M&R, ROQ, MHM, Anatol, Workhorse", "Base instalada en México: clientes naturales para agregar estaciones digitales"],
          ["Híbridos chinos", "Textalk, Hanglory y otros", "Venta principalmente por redes sociales y WhatsApp, sin estructura local visible"],
          ["Siliconas y pastas", "ScreenTec (Siltex), Avient (Wilflex, Rutland), Matsui y marcas económicas", "Competencia directa en consumibles"],
          ["Sustitutos", "DTF, sublimación, serigrafía tradicional", "El DTF crece rápido en tirajes cortos"],
        ],
      },
    },

    ...fodaBlocks("es"),

    { h1: "9. Comercio exterior y regulación" },
    {
      bullets: [
        "Importador: CEB, constituida en México, actuará como importador de registro de equipos y consumibles CLT. El envío será directo China → México para evitar los aranceles de EE. UU. (Sección 301) sobre productos chinos.",
        "Aranceles 2026: México aplica de 5% a 50% a 1,463 fracciones de países sin tratado (China incluida); prendas 35%, telas e hilos 15–35%. Pendiente confirmar con agente aduanal la tasa para maquinaria de impresión (8443) y químicos (3215, 3910), y la posible aplicación de PROSEC.",
        "IVA de importación (16%): acreditable; impacta el flujo de efectivo, no el costo.",
        "Requisitos: padrón de importadores vigente, NOM eléctricas aplicables (equipos a 220 V) y hojas de seguridad de químicos.",
        "T-MEC: 89% de las exportaciones textiles van a EE. UU.; las maquiladoras demandan certificaciones (OEKO-TEX) y respuesta rápida, que CLT puede ofrecer.",
      ],
    },

    { pagebreak: true },
    { h1: "10. El grupo distribuidor: TID México · VSP Printing · CEB" },
    {
      table: {
        cols: ["Empresa", "Papel en el proyecto", "Experiencia", "Técnicos"],
        widths: [1900, 2700, 3660, 1100],
        rows: [
          ["TID México (Querétaro)", "Venta, instalación y servicio en México", "12 años en decorado industrial: tampografía, hot stamping y serigrafía industrial; proyectos llave en mano", "2"],
          ["VSP Printing, Inc. (Sylmar, California)", "Venta y servicio en EE. UU.; respaldo técnico del grupo", "Más de 20 años en tampografía, hot stamping, impresión digital y serigrafía; igualación de color y desarrollo de procesos", "1"],
          ["CEB (México, subsidiaria de VSP)", "Importación de equipos e insumos CLT", "Importadora del grupo constituida en México", "—"],
        ],
      },
    },
    { h2: "Por qué somos el socio indicado" },
    {
      bullets: [
        "Mismo modelo de negocio: TID ya vende proyectos llave en mano con maquinaria, consumibles, capacitación y servicio.",
        "Negocio basado en consumibles: la venta recurrente de tintas, foils y mallas es el centro de nuestra operación.",
        "Servicio técnico local en español y mantenimiento preventivo: lo que hoy CLT no puede ofrecer desde China.",
        "Cobertura de Norteamérica con un solo socio: México (TID) y Los Ángeles (VSP), uno de los mayores centros de estampado de ropa de EE. UU.",
        "Ubicación estratégica: Querétaro, a 1–2 horas de Guanajuato y a 2–3 horas de CDMX, Estado de México y Puebla.",
        "Importadora propia en México (CEB) para controlar logística, aduanas e inventario.",
      ],
    },
    { h2: "Brechas y cómo las cerramos" },
    {
      table: {
        cols: ["Brecha", "Acción"],
        widths: [3400, 5960],
        rows: [
          ["Experiencia en el sector textil", "Crear una división textil con 1–2 vendedores provenientes del estampado de ropa"],
          ["Química textil (base agua, plastisol, silicona)", "Certificación de técnicos en la planta de CLT y soporte de su laboratorio de aplicación"],
          ["Capacidad técnica (3 técnicos)", "Contratar 1 técnico textil en el año 1 y otro en el año 2"],
          ["Presencia en eventos textiles", "Stand en FESPA México / Expo Producción y vinculación con CANAIVE"],
          ["Demostración", "Sala de demostración en Querétaro o CDMX con línea híbrida funcionando"],
        ],
      },
    },

    { h1: "11. Estrategia comercial" },
    {
      table: {
        cols: ["Fase", "Periodo", "Actividades clave"],
        widths: [2000, 1600, 5760],
        rows: [
          ["1. Arranque", "Meses 0–6", "Firma de acuerdo, contratación de vendedor, atención al cliente y técnico, capacitación en China, inventario inicial, venta de siliconas y pastas a talleres, lanzamiento en FESPA México"],
          ["2. Demostración", "Meses 6–18", "Sala de demostración, pruebas con clientes, primeras 2–5 líneas híbridas, contratos de servicio"],
          ["3. Escala", "Meses 18–36", "Cobertura de clústeres prioritarios, segundo técnico, programa de refacciones, inicio de expansión EE. UU. (VSP)"],
          ["4. Latinoamérica", "Año 3 en adelante", "Centroamérica, Colombia, Perú y Rep. Dominicana según metas cumplidas"],
        ],
      },
    },
    {
      bullets: [
        "Clientes de entrada: talleres que ya tienen pulpo automático (estaciones digitales sobre su equipo) y fabricantes de uniformes y ropa deportiva (nombres y números sobre prenda oscura).",
        "Oferta: paquete llave en mano (equipo + química + instalación + capacitación + servicio) con cálculo de retorno por cliente.",
        "Ingreso recurrente: consumibles, refacciones y contratos de mantenimiento preventivo.",
      ],
    },
    ...marketingBlocks("es"),

    { h1: "12. Estructura del equipo y capacitación" },
    { p: "La división textil operará con un equipo dedicado, apoyado por la estructura actual de TID (2 técnicos), VSP (1 técnico) y CEB (importación y logística)." },
    {
      table: {
        cols: ["Puesto", "Funciones", "Cuándo", "Costo mensual aprox."],
        widths: [2000, 4260, 1300, 1800],
        rows: [
          ["Vendedor especializado textil", "Prospección por zonas, visitas y demostraciones, cotizaciones llave en mano, cálculo de retorno por cliente y cierre de ventas", "Año 1", "~$40,000 MXN + comisión"],
          ["Atención al cliente", "Pedidos y reabasto de consumibles, seguimiento posventa, garantías, agenda de servicio técnico y de capacitaciones, encuestas de satisfacción", "Año 1", "~$20,000 MXN"],
          ["Técnico textil", "Instalación, puesta en marcha, mantenimiento preventivo y correctivo, soporte en pruebas de producción", "Año 1 (+1 en año 2)", "~$30,000 MXN"],
          ["Soporte del grupo", "Técnicos de TID (2) y VSP (1), importación y logística (CEB), administración", "Existente", "—"],
        ],
      },
    },
    { h2: "Programa de capacitación en máquinas y productos" },
    {
      table: {
        cols: ["Capacitación", "Dirigida a", "Contenido"],
        widths: [2200, 2300, 4860],
        rows: [
          ["Inicial en planta CLT", "Vendedor, técnicos y atención al cliente", "Operación y mantenimiento de híbridas, pulpos y DTG; química textil (siliconas, pastas, tintas); efectos especiales; certificación técnica"],
          ["En máquinas para clientes", "Operadores y supervisores del cliente", "Instalación, operación, calibración, limpieza de cabezales, mantenimiento preventivo y solución de fallas; incluida en el paquete llave en mano"],
          ["En productos (consumibles)", "Clientes y prospectos", "Uso de siliconas (3D, vidrio, bordado), pastas base agua, curado, pruebas de lavado y recetas de efectos; talleres en la sala de demostración"],
          ["Actualización continua", "Equipo interno y clientes", "Nuevos productos y modelos de CLT, sesiones remotas con ingenieros de CLT, actualización anual"],
        ],
      },
    },
    { note: "Sueldos mensuales antes de prestaciones (~35%). La capacitación puede ofrecerse con costo a clientes cuyas máquinas no se adquirieron con el grupo." },

    { pagebreak: true },
    { h1: "13. Inversión inicial (estimación)" },
    {
      table: {
        bold: true,
        cols: ["Concepto", "Ligero", "Base (recomendado)", "Completo"],
        widths: [3360, 1800, 2400, 1800],
        rows: [
          ["Equipo de demostración", "US$0 (consignación CLT o taller ancla)", "US$130k (pulpo + estación híbrida, 30–40% desc.)", "US$230k (pulpo + híbrida + DTG 6 estaciones)"],
          ["Importación (flete, seguro, agente, arancel)", "—", "US$20k", "US$40k"],
          ["Sala de demostración (220 V, compresor, curado, ventilación)", "US$5k", "US$25k", "US$40k"],
          ["Inventario inicial de consumibles", "US$20k", "US$35k", "US$60k"],
          ["Refacciones (cabezales, tarjetas)", "US$10k", "US$20k", "US$35k"],
          ["Capacitación en planta CLT (2–3 personas)", "US$8k", "US$12k", "US$15k"],
          ["Lanzamiento (FESPA, web, muestras)", "US$10k", "US$20k", "US$30k"],
          ["Total inversión inicial", "~US$53k", "~US$262k", "~US$450k"],
        ],
      },
    },
    {
      p: "Gastos de operación año 1 (escenario base): ~US$131 mil, que incluyen vendedor especializado textil (~$40,000 MXN/mes más comisión), atención al cliente (~$20,000 MXN/mes), técnico textil (~$30,000 MXN/mes), prestaciones, capacitación continua, ferias, espacio y viáticos. El IVA de importación es acreditable pero afecta el flujo de efectivo.",
    },

    { h1: "14. Proyección financiera (escenario base, estimación)" },
    {
      table: {
        bold: true,
        cols: ["Concepto", "Año 1", "Año 2", "Año 3"],
        widths: [3960, 1800, 1800, 1800],
        rows: [
          ["Líneas híbridas vendidas", "2", "5", "8"],
          ["Margen por equipos (20% sobre US$150k)", "US$60k", "US$150k", "US$240k"],
          ["Margen por consumibles (35%)", "US$34k", "US$99k", "US$209k"],
          ["Gastos de operación", "-US$131k", "-US$160k", "-US$180k"],
          ["Resultado del año", "-US$37k", "+US$89k", "+US$269k"],
          ["Resultado acumulado", "-US$37k", "+US$52k", "+US$321k"],
        ],
      },
    },
    {
      bullets: [
        "Supuestos: precio de línea US$150 mil; margen de distribuidor 20% en equipos y 35% en consumibles; consumo de ~US$36 mil anuales por línea instalada; venta adicional de siliconas y pastas a talleres sin línea híbrida.",
        "Escenario base: la inversión de ~US$262 mil se recupera durante el año 3.",
        "Escenario conservador (50% de la venta base): resultado positivo a partir del año 3 y recuperación de la inversión en 5 años o más. Por ello, el apoyo de CLT en equipo de demostración e inventario es determinante.",
      ],
    },

    { h1: "15. Propuesta de términos con CLT" },
    { h2: "Lo que solicitamos a CLT" },
    {
      bullets: [
        "Distribución exclusiva en México; extensión a Latinoamérica (y coordinación en EE. UU. vía VSP) sujeta a metas.",
        "Precio de distribuidor que permita un margen de ~20% en equipos y ~35% en consumibles.",
        "Equipo de demostración en consignación o con descuento de 30–50%.",
        "Inventario inicial de consumibles en consignación o con crédito a 90 días.",
        "Capacitación y certificación de técnicos sin costo; acceso a su laboratorio de aplicación.",
        "Apoyo compartido para ferias (FESPA México) y muestras.",
        "Canalización a TID / CEB de todos los prospectos de México (y Latinoamérica) generados por su sitio web y ferias.",
      ],
    },
    { h2: "Lo que el grupo se compromete a aportar" },
    {
      bullets: [
        "Importación, inventario local y logística a través de CEB.",
        "Sala de demostración, servicio técnico en español y mantenimiento preventivo.",
        "Equipo textil dedicado: vendedor especializado, atención al cliente y técnico.",
        "Programa de capacitación en máquinas y productos para clientes.",
        "Metas mínimas de venta propuestas: 2 líneas en el año 1, 5 en el año 2 y 8 en el año 3, más volumen de consumibles por acordar.",
        "Reportes trimestrales de mercado, pipeline y satisfacción de clientes.",
      ],
    },

    { h1: "16. Riesgos y mitigación" },
    {
      table: {
        cols: ["Riesgo", "Mitigación"],
        widths: [3600, 5760],
        rows: [
          ["Industria textil en contracción y clientes descapitalizados", "Inversión por etapas, estaciones digitales sobre pulpos existentes y financiamiento"],
          ["Competencia de DTF en tirajes cortos", "Enfocarse en volumen (500–5,000 piezas) y efectos que el DTF no logra"],
          ["Aranceles y cambios regulatorios", "Confirmar fracciones con agente aduanal; evaluar PROSEC; importación directa vía CEB"],
          ["Curva de aprendizaje textil del grupo", "Certificación en CLT, contratación de personal del sector y soporte remoto de CLT"],
          ["Tiempo de entrega de equipos (~1 mes)", "Inventario de refacciones y consumibles en México"],
          ["Tipo de cambio", "Precios en dólares y coberturas cuando aplique"],
        ],
      },
    },

    { h1: "17. Expansión: Estados Unidos y Latinoamérica" },
    {
      bullets: [
        "Estados Unidos (VSP Printing, Los Ángeles): CLT ya participa en PRINTING United; VSP puede ofrecer servicio local y seguimiento a prospectos. Se debe evaluar el impacto de los aranceles estadounidenses sobre productos chinos.",
        "Latinoamérica (año 3 en adelante): priorización preliminar de Centroamérica (maquila de exportación), Colombia, Perú y República Dominicana; el análisis detallado se entregará en la siguiente etapa del estudio.",
      ],
    },

    { h1: "18. Próximos pasos" },
    {
      bullets: [
        "Recibir cotización formal de CLT (CLT-016B, CLT-012R, pulpo SM60-85 y consumibles) para sustituir las estimaciones.",
        "Reunión con los dueños de CLT para revisar términos de distribución.",
        "Confirmar con agente aduanal las fracciones y aranceles aplicables a la importación vía CEB.",
        "Validar consumos y precios con 10–15 talleres y fabricantes mexicanos.",
        "Firmar carta de intención y definir el plan de arranque de 6 meses.",
      ],
    },

    { pagebreak: true },
    { h1: "Anexo: muestras de CLT" },
    { p: "Fotografías del stand de CLT en PRINTING United 2026 (Las Vegas), tomadas por VSP Printing durante su reunión con CLT, y de muestras de producción de CLT." },
    { images: [
      ["06-stand-printing-united.jpg", "Stand C3397: pulpo automático con estación digital en operación"],
      ["08-folleto-clt.jpg", "Folleto corporativo de CLT (clave 301618)"],
      ["01-vineyard.jpg", "Acuarela digital sobre base blanca en prenda de color"],
      ["02-perro.jpg", "Fotorrealismo digital sobre prenda oscura"],
      ["03-living.jpg", "Collage fotográfico a todo color"],
      ["10-aguila.jpg", "Impresión digital transpirable sobre prenda oscura"],
      ["04-clt-pastas.jpg", "Pastas CLT: alto relieve 511-1, espumante MP399, foil en frío 105-3"],
      ["05-escudo.jpg", "Escudo deportivo con relieve y brillo en poliéster"],
      ["07-tigre.jpg", "Serigrafía de tintas planas en prenda de color"],
      ["09-huskies.jpg", "Relieve, foil dorado y destellos metálicos combinados"],
    ] },
    { note: "Las técnicas indicadas se identificaron visualmente y deben confirmarse con CLT." },

    { h1: "Anexo: fuentes" },
    {
      bullets: [
        "CLT — garmentprintingpro.com (sitio internacional) y dgclt.com (corporativo).",
        "CLT — Reporte anual 2025, Bolsa de Shenzhen (clave 301618).",
        "INEGI — Conociendo la industria textil y de la confección 2024.",
        "CANAINTEX — Información estadística, mayo 2026 (cierre 2025).",
        "FESPA México — Panorama y desafíos de la industria textil mexicana 2025.",
        "Decreto de aranceles a países sin tratado (vigente desde el 1 de enero de 2026); El País, El Economista, Expansión.",
        "Precios de referencia de equipos: distribuidores públicos en EE. UU. (Texsource / M&R).",
        "Tintas: avientspecialtyinks.com, screentec.com.mx, sanchez.com.mx, casadiaz.com.mx (Matsui), marabu-tintas.es, ruco-druckfarben.de (distribuidores), tampoprint.com; precios en screenprinting.com, spsi.com, graficosleo.com.mx, Mercado Libre y Alibaba (octubre 2026).",
      ],
    },
  ],
};

const en = {
  meta: {
    file: "CLT_Distribution_Proposal_Mexico_EN",
    title: "CLT Distribution Proposal",
    subtitle: "Hybrid textile printing (screen + digital) — Mexico and Latin America",
    preparedBy: "Prepared by: TID México · VSP Printing, Inc. · CEB",
    preparedFor: "For: Dongguan Changlian New Material Technology Co., Ltd. (CLT)",
    date: "October 2026",
    conf: "Confidential document",
    contact: "Contact: Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
    footer: "TID / VSP / CEB proposal to CLT — Confidential",
    estimateNote:
      "Note: figures marked as “estimate” are our own calculations based on public sources and must be confirmed with CLT’s quotation and commercial terms.",
  },
  body: [
    { h1: "1. Executive summary" },
    {
      p: "TID México, VSP Printing, Inc. and its subsidiary CEB propose to become the distributor of CLT (Dongguan Changlian New Material Technology Co., Ltd., SZSE 301618) in Mexico, with expansion into the United States and Latin America. The goal is to introduce and locally support CLT’s hybrid printers (screen + digital) and its consumables: silicones, water-based pastes and inks.",
    },
    {
      bullets: [
        "Opportunity: we found no distributor of Chinese hybrid printing with a formal presence in Mexico (local inventory, spare parts, technicians and chemicals).",
        "Market: ~102,500 textile businesses; ~1,400–1,900 reachable customers (medium/large companies and shops with automatic carousels); 30–90 potential hybrid lines in 5 years (estimate).",
        "Timing: Mexico’s 2026 tariffs (up to 35% on garments from non-FTA countries) favor domestic manufacturers, who need to differentiate through added value and fast response.",
        "Partner: 30+ years of combined industrial printing experience, a consumables-and-service business model, presence in Mexico (Querétaro) and the U.S. (Los Angeles), and an in-house importer incorporated in Mexico (CEB).",
        "Proposed initial investment (base case): ~US$262k, with estimated payback during year 3.",
      ],
    },
    { h1: "2. Scope and methodology" },
    {
      p: "This study focuses on Mexico as the first stage; the United States and Latin America are presented as expansion stages. Sources: CLT’s international website (garmentprintingpro.com), its 2025 annual report, INEGI and CANAINTEX statistics, public tariff information and industry sources (FESPA México, manufacturers and distributors).",
    },
    {
      table: {
        cols: ["Parameter", "Content"],
        widths: [2600, 6760],
        rows: [
          ["Market definition", "Hybrid equipment, consumables (silicones, pastes, inks) and technical service; substitutes: traditional screen printing, DTG, DTF, sublimation"],
          ["Segments", "Export maquiladoras (IMMEX), domestic brands, medium/large screen-print shops, promotional, uniforms and sportswear"],
          ["Sizing", "Total, serviceable and obtainable market (TAM / SAM / SOM) with conservative, base and optimistic scenarios"],
          ["Geography", "Clusters: State of Mexico/Mexico City, Jalisco, Puebla/Tlaxcala, Guanajuato, Baja California, La Laguna, Aguascalientes, Nuevo León, Yucatán"],
          ["Competition", "DTG makers and distributors, automatic carousels, Chinese hybrids and consumables"],
          ["Economics", "Distributor investment, margins, break-even and payback"],
          ["Regulation", "2026 tariffs, import through CEB, USMCA, electrical standards (NOM)"],
        ],
      },
    },
    { note: "Figures marked as “estimate” are our own calculations and must be confirmed with CLT’s quotation and terms." },

    { h1: "3. CLT: manufacturer profile" },
    {
      p: "Dongguan Changlian New Material Technology Co., Ltd. (CLT) was founded in 2009 in Liaobu, Dongguan (Guangdong). It has been listed on the ChiNext board of the Shenzhen Stock Exchange since September 2024 (code 301618). It is recognized in China as a leader in water-based printing pastes and offers an integrated materials-and-equipment solution for textile printing.",
    },
    {
      table: {
        cols: ["2025 indicator", "Value", "Approx. USD"],
        widths: [4360, 2600, 2400],
        rows: [
          ["Total revenue", "¥568.1 million", "~US$80M"],
          ["Water-based printing pastes", "¥304.4M (53.6%)", "~US$43M"],
          ["Silicone materials", "¥117.7M (20.7%)", "~US$17M"],
          ["Water-based resins", "¥45.9M (8.1%)", "~US$6M"],
          ["Printing equipment", "¥37.0M (6.5%)", "~US$5M"],
          ["Export sales", "¥103.5M (18.2%)", "~US$15M"],
          ["Net profit attributable", "¥40.6 million", "~US$6M"],
          ["Channel: traders / manufacturers", "49.5% / 50.5%", ""],
        ],
      },
    },
    { note: "Source: CLT 2025 annual report (Shenzhen Stock Exchange). Reference exchange rate: ¥7.1 per US$." },
    { h2: "Portfolio relevant to this proposal" },
    {
      bullets: [
        "Hybrid printers: CLT-012R/015R/018R (Ricoh heads, up to 1800 dpi, 450 pcs/h), CLT-014B/016B/018B (Brother 680, 400 pcs/h), CLT-005S (Star Light white).",
        "Automatic oval presses: SM45-85, SM60-85, SM70-95 (up to 800 pcs/h, ±0.02 mm).",
        "6-station DTG with inline pre-treatment and the CLT-6900 industrial DTF series.",
        "Effect silicones: high-density / 3D (S-1701), rounded-edge (S-1703), glossy glass-like (S-1704-1), special-purpose (S-1714-1); water-based pastes, puff pastes and DTG/DTF inks.",
        "Certifications: OEKO-TEX, GOTS, ISO 9001 and ISO 14001.",
      ],
    },
    { h2: "Hybrid technology" },
    {
      p: "Digital stations are mounted on an oval screen-printing press. The white underbase is printed with (low-cost) screen paste and the color with digital heads, so screen effects (puff, foil, glitter, discharge, glass-like or embroidery-like silicone) can be combined in a single pass with photographic gradients. CLT reports ink savings of 40–70% versus pure DTG and profitability on runs of 500 to 5,000 pieces.",
    },

    { h1: "4. CLT’s commercial model" },
    {
      p: "CLT uses equipment as the gateway to recurring chemical consumption, which makes up most of its revenue. Its 2026 plan is to consolidate Southeast Asia and expand in Europe, the Americas, the Middle East and Africa by building out its overseas agent network.",
    },
    {
      table: {
        cols: ["Element", "How CLT applies it"],
        widths: [2800, 6560],
        rows: [
          ["Trade shows with live demos", "Running production line, tests on the customer’s fabric and artwork, same-day written quote, show-only packages (PRINTING United, Stitch & Tex Egypt)"],
          ["Turnkey package", "Machine + matched chemistry + installation + training + freight and import paperwork, at one price"],
          ["Phased investment", "Start with the press and add digital stations; 2–3 season plans"],
          ["ROI-based selling", "Ink savings, fewer operators, less floor space; customized ROI calculation"],
          ["Linked consumables", "Warranty requires genuine CLT parts and chemistry"],
          ["Application lab", "Simulates the customer’s production and recommends the full process"],
          ["Digital lead capture", "Multilingual site, forms and WhatsApp with a response in under 2 hours"],
        ],
      },
    },
    {
      p: "What is missing in Mexico today: local technical service, in-country spare parts and chemistry inventory, Spanish-language support and a demo showroom. These are exactly what our group brings.",
    },

    { pagebreak: true },
    { h1: "5. Mexican market overview" },
    {
      table: {
        cols: ["Indicator", "Data", "Source"],
        widths: [3000, 4160, 2200],
        rows: [
          ["Textile & apparel GDP", "MXN 91,165 million; 1.75% of manufacturing GDP", "CANAINTEX, 2025"],
          ["GDP composition", "Apparel 56%, textile inputs & finishing 27%, textile products 17%", "CANAINTEX"],
          ["Businesses", "102,492", "INEGI 2023"],
          ["Jobs", "519,313 (225k formal)", "INEGI 2022 / CANAINTEX"],
          ["Company size", "Micro 95.6%, small 3.3%, medium 0.8%, large 0.3%", "INEGI, 2019 Census"],
          ["Exports", "US$9.3 billion; 89% to the U.S.", "INEGI 2023"],
          ["Imports", "US$13.3 billion; 35% from China", "INEGI 2023"],
          ["Trend", "GDP -8.4% in 2023; ~20k jobs lost in 2024", "INEGI / FESPA"],
        ],
      },
    },
    {
      p: "The industry is under pressure from low-cost imports and informality. Domestic manufacturers are responding by differentiating: customization, short runs with fast delivery and high-value effects. Hybrid printing directly addresses this need. The tariffs in force since January 2026 strengthen the position of those producing in Mexico.",
    },

    { h1: "6. Market size (estimate)" },
    {
      table: {
        cols: ["Level", "Definition", "Estimated size"],
        widths: [2000, 4760, 2600],
        rows: [
          ["Total market (TAM)", "All textile and apparel businesses", "~102,500"],
          ["Serviceable market (SAM)", "Medium and large companies (~1,130) plus screen-print shops with automatic carousels (300–800)", "~1,400–1,900 customers"],
          ["Obtainable market (SOM, 5 years)", "2–5% adoption of the serviceable market", "~30–90 hybrid lines"],
        ],
      },
    },
    {
      bullets: [
        "Equipment: 30–90 lines × US$120–250k landed in Mexico = US$3.6–22 million over 5 years (estimate; to be confirmed with CLT’s quotation).",
        "Consumables: US$1,500–5,000 per line per month (hypothesis to validate with shops). With 50 lines: US$0.9–3 million per year, plus silicone and paste sales to shops without hybrid equipment.",
        "Competitor price reference: M&R Cobra automatic press, 10 stations / 8 colors, ~US$88k in the U.S.",
      ],
    },

    { h1: "7. Priority regions" },
    {
      table: {
        cols: ["Priority", "Region", "Rationale"],
        widths: [1300, 3000, 5060],
        rows: [
          ["1", "State of Mexico and Mexico City", "Largest concentration of printers, brands, promotional and corporate buyers"],
          ["1", "Jalisco (Guadalajara, Zapotlanejo)", "Fashion, sportswear and domestic brands"],
          ["1", "Baja California (Tijuana, Ensenada, Tecate)", "Export screen printing for U.S. brands (Disney, Fanatics, Columbia); joint TID + VSP coverage from the border"],
          ["2", "Puebla and Tlaxcala", "Export maquila and knitwear"],
          ["2", "Guanajuato (Moroleón, Uriangato, León)", "Knitwear and wholesale; 1–2 hours from TID in Querétaro"],
          ["3", "La Laguna, Aguascalientes, Nuevo León, Yucatán", "Denim, IMMEX maquila and uniforms"],
        ],
      },
    },
    { note: "Preliminary ranking by concentration of medium and large industry; to be validated with INEGI’s DENUE business directory." },
    ...top8020Blocks("en"),

    { h1: "8. Competition" },
    {
      table: {
        cols: ["Type", "Players", "Observation"],
        widths: [2400, 3400, 3560],
        rows: [
          ["High-end DTG / digital", "Kornit (via Sun Digital México)", "DTG leader; high investment; established service"],
          ["Automatic presses", "M&R, ROQ, MHM, Anatol, Workhorse", "Installed base in Mexico: natural customers for add-on digital stations"],
          ["Chinese hybrids", "Textalk, Hanglory and others", "Sold mainly via social media and WhatsApp, with no visible local structure"],
          ["Silicones and pastes", "ScreenTec (Siltex), Avient (Wilflex, Rutland), Matsui and budget brands", "Direct competition in consumables"],
          ["Substitutes", "DTF, sublimation, traditional screen printing", "DTF is growing fast in short runs"],
        ],
      },
    },

    ...fodaBlocks("en"),

    { h1: "9. Trade and regulation" },
    {
      bullets: [
        "Importer: CEB, incorporated in Mexico, will act as importer of record for CLT equipment and consumables. Shipments will go directly China → Mexico to avoid U.S. tariffs (Section 301) on Chinese goods.",
        "2026 tariffs: Mexico applies 5% to 50% on 1,463 tariff lines from non-FTA countries (including China); garments 35%, fabrics and yarns 15–35%. The rate for printing machinery (8443) and chemicals (3215, 3910), and possible PROSEC treatment, are to be confirmed with a customs broker.",
        "Import VAT (16%): creditable; it affects cash flow, not cost.",
        "Requirements: valid importer registry, applicable electrical standards (220 V equipment) and chemical safety data sheets.",
        "USMCA: 89% of textile exports go to the U.S.; maquiladoras demand certifications (OEKO-TEX) and fast response, which CLT can deliver.",
      ],
    },

    { pagebreak: true },
    { h1: "10. The distributor group: TID México · VSP Printing · CEB" },
    {
      table: {
        cols: ["Company", "Role in the project", "Experience", "Technicians"],
        widths: [1900, 2700, 3660, 1100],
        rows: [
          ["TID México (Querétaro)", "Sales, installation and service in Mexico", "12 years in industrial decoration: pad printing, hot stamping and industrial screen printing; turnkey projects", "2"],
          ["VSP Printing, Inc. (Sylmar, California)", "Sales and service in the U.S.; technical backup for the group", "20+ years in pad printing, hot stamping, digital and screen printing; color matching and process development", "1"],
          ["CEB (Mexico, VSP subsidiary)", "Import of CLT equipment and supplies", "Group importer incorporated in Mexico", "—"],
        ],
      },
    },
    { h2: "Why we are the right partner" },
    {
      bullets: [
        "Same business model: TID already sells turnkey projects combining machinery, consumables, training and service.",
        "Consumables-driven business: recurring sales of inks, foils and meshes are at the core of our operation.",
        "Local technical service in Spanish and preventive maintenance: what CLT cannot provide today from China.",
        "North America coverage with a single partner: Mexico (TID) and Los Angeles (VSP), one of the largest apparel-decoration hubs in the U.S.",
        "Strategic location: Querétaro is 1–2 hours from Guanajuato and 2–3 hours from Mexico City, State of Mexico and Puebla.",
        "In-house importer in Mexico (CEB) to control logistics, customs and inventory.",
      ],
    },
    { h2: "Gaps and how we close them" },
    {
      table: {
        cols: ["Gap", "Action"],
        widths: [3400, 5960],
        rows: [
          ["Textile-sector experience", "Create a textile division with 1–2 salespeople from the apparel-decoration industry"],
          ["Textile chemistry (water-based, plastisol, silicone)", "Technician certification at CLT’s plant and support from its application lab"],
          ["Technical capacity (3 technicians)", "Hire 1 textile technician in year 1 and another in year 2"],
          ["Presence at textile events", "Booth at FESPA México / Expo Producción and ties with CANAIVE"],
          ["Demonstration", "Showroom in Querétaro or Mexico City with a running hybrid line"],
        ],
      },
    },

    { h1: "11. Go-to-market strategy" },
    {
      table: {
        cols: ["Phase", "Period", "Key activities"],
        widths: [2000, 1600, 5760],
        rows: [
          ["1. Launch", "Months 0–6", "Agreement signed, hiring of sales specialist, customer service and technician, training in China, initial inventory, silicone and paste sales to shops, launch at FESPA México"],
          ["2. Demonstration", "Months 6–18", "Showroom, customer trials, first 2–5 hybrid lines, service contracts"],
          ["3. Scale", "Months 18–36", "Coverage of priority clusters, second technician, spare-parts program, start of U.S. expansion (VSP)"],
          ["4. Latin America", "Year 3 onward", "Central America, Colombia, Peru and Dominican Republic, subject to targets met"],
        ],
      },
    },
    {
      bullets: [
        "Entry customers: shops that already own automatic presses (digital stations on their equipment) and uniform and sportswear makers (names and numbers on dark garments).",
        "Offer: turnkey package (equipment + chemistry + installation + training + service) with a customer-specific ROI calculation.",
        "Recurring revenue: consumables, spare parts and preventive-maintenance contracts.",
      ],
    },
    ...marketingBlocks("en"),

    { h1: "12. Team structure and training" },
    { p: "The textile division will run with a dedicated team, backed by the existing structure of TID (2 technicians), VSP (1 technician) and CEB (import and logistics)." },
    {
      table: {
        cols: ["Role", "Responsibilities", "When", "Approx. monthly cost"],
        widths: [2000, 4260, 1300, 1800],
        rows: [
          ["Textile sales specialist", "Prospecting by region, visits and demos, turnkey quotes, customer ROI calculation and closing", "Year 1", "~MXN 40,000 + commission"],
          ["Customer service", "Consumables orders and replenishment, after-sales follow-up, warranties, scheduling of service and training, satisfaction surveys", "Year 1", "~MXN 20,000"],
          ["Textile technician", "Installation, commissioning, preventive and corrective maintenance, production-trial support", "Year 1 (+1 in year 2)", "~MXN 30,000"],
          ["Group support", "TID (2) and VSP (1) technicians, import and logistics (CEB), administration", "Existing", "—"],
        ],
      },
    },
    { h2: "Machine and product training program" },
    {
      table: {
        cols: ["Training", "Audience", "Content"],
        widths: [2200, 2300, 4860],
        rows: [
          ["Initial, at CLT’s plant", "Sales, technicians and customer service", "Operation and maintenance of hybrids, presses and DTG; textile chemistry (silicones, pastes, inks); special effects; technical certification"],
          ["Machine training for customers", "Customer operators and supervisors", "Installation, operation, calibration, head cleaning, preventive maintenance and troubleshooting; included in the turnkey package"],
          ["Product (consumables) training", "Customers and prospects", "Use of silicones (3D, glass-like, embroidery-like), water-based pastes, curing, wash tests and effect recipes; workshops in the demo showroom"],
          ["Ongoing updates", "Internal team and customers", "New CLT products and models, remote sessions with CLT engineers, annual refresher"],
        ],
      },
    },
    { note: "Monthly salaries before benefits (~35%). Training can be offered for a fee to customers whose machines were not purchased through the group." },

    { pagebreak: true },
    { h1: "13. Initial investment (estimate)" },
    {
      table: {
        bold: true,
        cols: ["Item", "Light", "Base (recommended)", "Full"],
        widths: [3360, 1800, 2400, 1800],
        rows: [
          ["Demo equipment", "US$0 (CLT consignment or anchor shop)", "US$130k (press + hybrid station, 30–40% discount)", "US$230k (press + hybrid + 6-station DTG)"],
          ["Import (freight, insurance, broker, duty)", "—", "US$20k", "US$40k"],
          ["Showroom (220 V, compressor, curing, ventilation)", "US$5k", "US$25k", "US$40k"],
          ["Initial consumables inventory", "US$20k", "US$35k", "US$60k"],
          ["Spare parts (heads, boards)", "US$10k", "US$20k", "US$35k"],
          ["Training at CLT’s plant (2–3 people)", "US$8k", "US$12k", "US$15k"],
          ["Launch (FESPA, web, samples)", "US$10k", "US$20k", "US$30k"],
          ["Total initial investment", "~US$53k", "~US$262k", "~US$450k"],
        ],
      },
    },
    {
      p: "Year-1 operating expenses (base case): ~US$131k, including a textile sales specialist (~MXN 40,000/month plus commission), customer service (~MXN 20,000/month), a textile technician (~MXN 30,000/month), benefits, ongoing training, trade shows, space and travel. Import VAT is creditable but affects cash flow.",
    },

    { h1: "14. Financial projection (base case, estimate)" },
    {
      table: {
        bold: true,
        cols: ["Item", "Year 1", "Year 2", "Year 3"],
        widths: [3960, 1800, 1800, 1800],
        rows: [
          ["Hybrid lines sold", "2", "5", "8"],
          ["Equipment margin (20% on US$150k)", "US$60k", "US$150k", "US$240k"],
          ["Consumables margin (35%)", "US$34k", "US$99k", "US$209k"],
          ["Operating expenses", "-US$131k", "-US$160k", "-US$180k"],
          ["Annual result", "-US$37k", "+US$89k", "+US$269k"],
          ["Cumulative result", "-US$37k", "+US$52k", "+US$321k"],
        ],
      },
    },
    {
      bullets: [
        "Assumptions: line price US$150k; distributor margin 20% on equipment and 35% on consumables; ~US$36k annual consumption per installed line; additional silicone and paste sales to shops without hybrid lines.",
        "Base case: the ~US$262k investment is recovered during year 3.",
        "Conservative case (50% of base sales): positive results from year 3 and payback in 5+ years. CLT’s support on demo equipment and inventory is therefore decisive.",
      ],
    },

    { h1: "15. Proposed terms with CLT" },
    { h2: "What we request from CLT" },
    {
      bullets: [
        "Exclusive distribution in Mexico; extension to Latin America (and U.S. coordination through VSP) subject to targets.",
        "Distributor pricing that allows ~20% margin on equipment and ~35% on consumables.",
        "Demo equipment on consignment or at a 30–50% discount.",
        "Initial consumables inventory on consignment or with 90-day credit.",
        "Free technician training and certification; access to CLT’s application lab.",
        "Shared support for trade shows (FESPA México) and samples.",
        "Referral to TID / CEB of all Mexican (and Latin American) leads generated by CLT’s website and trade shows.",
      ],
    },
    { h2: "What the group commits to" },
    {
      bullets: [
        "Import, local inventory and logistics through CEB.",
        "Demo showroom, Spanish-language technical service and preventive maintenance.",
        "A dedicated textile team: sales specialist, customer service and technician.",
        "A machine and product training program for customers.",
        "Proposed minimum sales targets: 2 lines in year 1, 5 in year 2 and 8 in year 3, plus consumables volume to be agreed.",
        "Quarterly reports on market, pipeline and customer satisfaction.",
      ],
    },

    { h1: "16. Risks and mitigation" },
    {
      table: {
        cols: ["Risk", "Mitigation"],
        widths: [3600, 5760],
        rows: [
          ["Contracting textile industry and cash-strapped customers", "Phased investment, digital stations on existing presses and financing"],
          ["DTF competition in short runs", "Focus on volume (500–5,000 pieces) and effects DTF cannot achieve"],
          ["Tariffs and regulatory changes", "Confirm tariff lines with a customs broker; evaluate PROSEC; direct import through CEB"],
          ["Group’s textile learning curve", "Certification at CLT, hiring industry staff and CLT remote support"],
          ["Equipment lead time (~1 month)", "Spare parts and consumables inventory in Mexico"],
          ["Exchange rate", "Pricing in U.S. dollars and hedging where applicable"],
        ],
      },
    },

    { h1: "17. Expansion: United States and Latin America" },
    {
      bullets: [
        "United States (VSP Printing, Los Angeles): CLT already exhibits at PRINTING United; VSP can provide local service and lead follow-up. The impact of U.S. tariffs on Chinese goods must be assessed.",
        "Latin America (year 3 onward): preliminary priority on Central America (export maquila), Colombia, Peru and the Dominican Republic; a detailed analysis will be delivered in the next stage of the study.",
      ],
    },

    { h1: "18. Next steps" },
    {
      bullets: [
        "Receive CLT’s formal quotation (CLT-016B, CLT-012R, SM60-85 press and consumables) to replace the estimates.",
        "Meeting with CLT’s owners to review distribution terms.",
        "Confirm with a customs broker the tariff lines and duties for import through CEB.",
        "Validate consumption and pricing with 10–15 Mexican shops and manufacturers.",
        "Sign a letter of intent and define the 6-month launch plan.",
      ],
    },

    { pagebreak: true },
    { h1: "Appendix: CLT samples" },
    { p: "Photos of CLT’s PRINTING United 2026 booth (Las Vegas), taken by VSP Printing during its meeting with CLT, and of CLT production samples." },
    { images: [
      ["06-stand-printing-united.jpg", "Booth C3397: automatic carousel with a digital station running"],
      ["08-folleto-clt.jpg", "CLT corporate brochure (code 301618)"],
      ["01-vineyard.jpg", "Digital watercolor over white base on a colored garment"],
      ["02-perro.jpg", "Digital photorealism on a dark garment"],
      ["03-living.jpg", "Full-color photographic collage"],
      ["10-aguila.jpg", "Breathable digital print on a dark garment"],
      ["04-clt-pastas.jpg", "CLT pastes: high build 511-1, puff MP399, cold foil 105-3"],
      ["05-escudo.jpg", "Sports crest with relief and shimmer on polyester"],
      ["07-tigre.jpg", "Spot-color screen print on a colored garment"],
      ["09-huskies.jpg", "Relief, gold foil and metallic sparkle combined"],
    ] },
    { note: "Techniques were identified visually and should be confirmed with CLT." },

    { h1: "Appendix: sources" },
    {
      bullets: [
        "CLT — garmentprintingpro.com (international site) and dgclt.com (corporate).",
        "CLT — 2025 annual report, Shenzhen Stock Exchange (code 301618).",
        "INEGI — Conociendo la industria textil y de la confección 2024.",
        "CANAINTEX — Statistical information, May 2026 (2025 close).",
        "FESPA México — Overview and challenges of the Mexican textile industry 2025.",
        "Decree on tariffs for non-FTA countries (in force since January 1, 2026); El País, El Economista, Expansión.",
        "Equipment price references: public U.S. distributors (Texsource / M&R).",
        "Inks: avientspecialtyinks.com, screentec.com.mx, sanchez.com.mx, casadiaz.com.mx (Matsui), marabu-tintas.es, ruco-druckfarben.de (distributors), tampoprint.com; prices from screenprinting.com, spsi.com, graficosleo.com.mx, Mercado Libre and Alibaba (October 2026).",
      ],
    },
  ],
};

module.exports = { es, en };
