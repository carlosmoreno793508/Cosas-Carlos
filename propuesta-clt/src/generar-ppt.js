// Genera la presentación (ES y EN) con transiciones. Uso: node generar-ppt.js <carpeta_salida>
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const JSZip = require("jszip");

const THEME = {
  name: "CLT Propuesta",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B1F3B", lt1: "FFFFFF", dk2: "3A4060", lt2: "EEF2F7",
    accent1: "C2185B", accent2: "0089C2", accent3: "F2B705", accent4: "1B1F3B",
    accent5: "7A8299", accent6: "2E7D32", hlink: "0089C2", folHlink: "6D2E46",
  },
};
const HEX = THEME.colors;

// ---------- Textos ----------
const T = {
  es: {
    file: "Presentacion_Propuesta_CLT_ES",
    footer: "Propuesta TID · VSP · CEB para CLT — Confidencial",
    estimate: "Estimación — confirmar con cotización CLT",
    title: "Propuesta de Distribución CLT",
    subtitle: "Impresión híbrida textil (serigrafía + digital) en México y Latinoamérica",
    by: "TID México · VSP Printing, Inc. · CEB  |  Octubre 2026",
    s_exec: "La oportunidad en una página",
    exec: [
      ["0", "distribuidores formales de híbridos chinos en México"],
      ["~1,900", "clientes alcanzables (empresas medianas/grandes y talleres con pulpo)"],
      ["30–90", "líneas híbridas potenciales en 5 años"],
      ["Año 3", "recuperación de la inversión (escenario base)"],
    ],
    execMsg: "Proponemos a TID / VSP / CEB como distribuidor de CLT en México, con expansión a EE. UU. y Latinoamérica.",
    sec1: "El fabricante", sec1n: "01",
    s_clt: "CLT: una empresa química que vende máquinas",
    cltStats: [["2009", "fundación, Dongguan"], ["¥568 M", "ingresos 2025 (~US$80 M)"], ["301618", "Bolsa de Shenzhen (ChiNext)"], ["18%", "ventas de exportación"]],
    mixTitle: "Ingresos 2025 por línea",
    mixLabels: ["Pastas base agua", "Siliconas", "Resinas", "Equipos", "Otros"],
    s_tech: "La tecnología híbrida: lo mejor de dos procesos",
    steps: [
      ["Base serigráfica", "Blanco y efectos con pasta económica: relieve, foil, glitter, descarga"],
      ["Color digital", "Cabezales Ricoh o Brother: degradados fotográficos, colores ilimitados"],
      ["Efectos especiales", "Silicona tipo vidrio, bordado o 3D sobre la impresión"],
    ],
    techStats: [["400–450", "piezas por hora"], ["40–70%", "ahorro de tinta vs DTG"], ["500–5,000", "piezas: tiraje rentable"]],
    s_model: "Cómo vende CLT hoy",
    model: [
      ["Ferias con demo en vivo", "Prueba con la tela del cliente y cotización el mismo día"],
      ["Paquete llave en mano", "Máquina, química, instalación, capacitación y logística"],
      ["Inversión por etapas", "Pulpo primero, estaciones digitales después"],
      ["Venta por ROI", "Ahorro de tinta, operadores y espacio"],
      ["Consumibles vinculados", "Garantía con química y refacciones originales"],
      ["Captación digital", "Sitio multilingüe y WhatsApp"],
    ],
    modelGap: "Lo que falta en México: servicio técnico local, inventario en el país, atención en español y sala de demostración",
    sec2: "El mercado mexicano", sec2n: "02",
    s_mkt: "Una industria que necesita diferenciarse",
    mkt: [["$91,165 M", "PIB textil-confección (MXN, 2025)"], ["102,492", "unidades económicas"], ["519 mil", "puestos de trabajo"], ["89%", "exportaciones a EE. UU."]],
    mktMsg: [
      "La importación de bajo costo presiona al fabricante nacional (PIB -8.4% en 2023)",
      "Aranceles 2026: hasta 35% a prendas de países sin tratado, incluida China",
      "La salida: personalización, tirajes cortos y efectos de alto valor, justo lo que hace el híbrido",
    ],
    s_size: "Tamaño del mercado",
    funnel: [["~102,500", "Mercado total: todas las empresas textiles"], ["~1,400–1,900", "Alcanzable: medianas/grandes y talleres con pulpo"], ["30–90 líneas", "Capturable a 5 años (2–5% de adopción)"]],
    sizeSide: [["US$3.6–22 M", "en equipos a 5 años"], ["US$0.9–3 M", "al año en consumibles (50 líneas)"]],
    s_geo: "Zonas prioritarias",
    geo: [
      ["1", "Edomex y CDMX", "Estampadores, marcas, promocionales"],
      ["1", "Jalisco", "Moda, deportivo, marcas nacionales"],
      ["2", "Puebla y Tlaxcala", "Maquila de exportación, punto"],
      ["2", "Guanajuato", "Punto y mayoreo; a 1–2 h de TID"],
      ["3", "Laguna, Ags., N.L., Yucatán", "Mezclilla, IMMEX, uniformes"],
    ],
    s_comp: "Competencia: el hueco está en el servicio local",
    compCols: ["Tipo", "Jugadores", "Lectura"],
    comp: [
      ["DTG alta gama", "Kornit (Sun Digital México)", "Inversión alta"],
      ["Pulpos automáticos", "M&R, ROQ, MHM, Anatol", "Clientes para estaciones digitales"],
      ["Híbridos chinos", "Textalk, Hanglory", "Sin estructura local visible"],
      ["Siliconas y pastas", "ScreenTec (Siltex)", "Competencia en consumibles"],
      ["Sustitutos", "DTF, sublimación", "DTF crece en tirajes cortos"],
    ],
    s_trade: "Importación y regulación",
    trade: [
      ["CEB importa", "Empresa del grupo constituida en México; envío directo China → México"],
      ["Aranceles 2026", "5–50% a países sin tratado; confirmar fracciones 8443, 3215 y 3910"],
      ["IVA 16%", "Acreditable: afecta flujo, no costo"],
      ["T-MEC", "Maquiladoras exigen OEKO-TEX y respuesta rápida"],
    ],
    sec3: "Por qué TID · VSP · CEB", sec3n: "03",
    s_group: "Un grupo con presencia en México y EE. UU.",
    group: [
      ["TID México", "Querétaro", "12 años en decorado industrial. Venta, instalación y servicio en México. 2 técnicos."],
      ["VSP Printing", "Los Ángeles, CA", "20+ años en impresión industrial. Servicio en EE. UU. y respaldo técnico. 1 técnico."],
      ["CEB", "México", "Subsidiaria de VSP. Importación de equipos e insumos CLT."],
    ],
    s_fit: "Fortalezas y cómo cerramos las brechas",
    fitL: "Lo que aportamos",
    fitLItems: ["Mismo modelo llave en mano", "Negocio basado en consumibles", "Servicio técnico en español", "Cobertura México + EE. UU.", "Importadora propia (CEB)"],
    fitR: "Brecha → acción",
    fitRItems: ["Experiencia textil → división textil dedicada", "Química textil → certificación en CLT", "3 técnicos → +2 técnicos textiles", "Eventos textiles → FESPA México", "Demostración → sala con línea híbrida"],
    s_team: "Equipo dedicado y capacitación",
    team: [
      ["Vendedor textil", "Prospección, demos, cotizaciones llave en mano y cierre"],
      ["Atención al cliente", "Pedidos de consumibles, posventa, garantías y agenda de servicio"],
      ["Técnico textil", "Instalación, mantenimiento y soporte; +1 técnico en año 2"],
    ],
    trainT: "Programa de capacitación",
    train: ["Inicial en planta CLT: máquinas, química y certificación", "Clientes – máquinas: operación, calibración y mantenimiento", "Clientes – productos: siliconas, pastas, curado y efectos", "Actualización continua con ingenieros de CLT"],
    teamNote: "Apoyo existente: 2 técnicos TID, 1 técnico VSP, importación y logística CEB",
    sec4: "Plan e inversión", sec4n: "04",
    s_plan: "Plan comercial en cuatro fases",
    plan: [["0–6 meses", "Arranque", "Acuerdo, contrataciones, capacitación, consumibles, FESPA"], ["6–18 meses", "Demostración", "Sala demo, primeras 2–5 líneas"], ["18–36 meses", "Escala", "Clústeres prioritarios, EE. UU. vía VSP"], ["Año 3+", "Latinoamérica", "Centroamérica, Colombia, Perú, R. Dominicana"]],
    s_inv: "Inversión inicial",
    inv: [["Ligero", "~US$53k", "Demo en consignación o en taller ancla; consumibles primero"], ["Base", "~US$262k", "Pulpo + estación híbrida, inventario, sala demo, lanzamiento"], ["Completo", "~US$450k", "Línea completa con DTG de 6 estaciones"]],
    invRec: "Recomendado",
    invNote: "Gasto operativo año 1: ~US$131k (vendedor, atención al cliente, técnico, capacitación, ferias)",
    s_fin: "Proyección: el ingreso recurrente crece cada año",
    finSeries: ["Margen equipos", "Margen consumibles"],
    finYears: ["Año 1", "Año 2", "Año 3"],
    finChartTitle: "Margen bruto (miles de US$)",
    finRes: [["Año 1", "-US$37k"], ["Año 2", "+US$89k"], ["Año 3", "+US$269k"]],
    finResTitle: "Resultado anual",
    finNote: "Supuestos: línea US$150k, margen 20% equipos / 35% consumibles, ~US$36k de consumo por línea al año",
    sec5: "La propuesta", sec5n: "05",
    s_terms: "Lo que pedimos y lo que nos comprometemos",
    askT: "Solicitamos a CLT",
    ask: ["Exclusividad en México; Latam según metas", "Margen ~20% equipos / ~35% consumibles", "Demo en consignación o 30–50% desc.", "Inventario inicial a consignación o 90 días", "Capacitación y certificación sin costo", "Prospectos de México canalizados a TID / CEB"],
    giveT: "Nos comprometemos a",
    give: ["Importación e inventario local (CEB)", "Sala demo y servicio en español", "Vendedor, atención al cliente y técnico textil", "Capacitación en máquinas y productos", "Metas: 2 · 5 · 8 líneas en años 1–3", "Reportes trimestrales"],
    s_risk: "Riesgos y mitigación",
    risk: [["Industria descapitalizada", "Inversión por etapas y financiamiento"], ["DTF en tirajes cortos", "Enfoque en volumen y efectos"], ["Aranceles", "Fracciones confirmadas; PROSEC; CEB"], ["Curva textil", "Certificación CLT y personal del sector"]],
    s_next: "Próximos pasos",
    next: ["Cotización formal de CLT (CLT-016B, CLT-012R, SM60-85, consumibles)", "Reunión con los dueños de CLT para revisar términos", "Confirmar aranceles con agente aduanal", "Validar consumos con 10–15 talleres", "Carta de intención y plan de arranque de 6 meses"],
    contact: "Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
    thanks: "Gracias",
  },
  en: {
    file: "CLT_Proposal_Presentation_EN",
    footer: "TID · VSP · CEB proposal to CLT — Confidential",
    estimate: "Estimate — to be confirmed with CLT’s quotation",
    title: "CLT Distribution Proposal",
    subtitle: "Hybrid textile printing (screen + digital) in Mexico and Latin America",
    by: "TID México · VSP Printing, Inc. · CEB  |  October 2026",
    s_exec: "The opportunity on one page",
    exec: [
      ["0", "formal distributors of Chinese hybrids in Mexico"],
      ["~1,900", "reachable customers (medium/large firms and shops with carousels)"],
      ["30–90", "potential hybrid lines in 5 years"],
      ["Year 3", "investment payback (base case)"],
    ],
    execMsg: "We propose TID / VSP / CEB as CLT’s distributor in Mexico, expanding into the U.S. and Latin America.",
    sec1: "The manufacturer", sec1n: "01",
    s_clt: "CLT: a chemistry company that sells machines",
    cltStats: [["2009", "founded, Dongguan"], ["¥568M", "2025 revenue (~US$80M)"], ["301618", "Shenzhen Stock Exchange (ChiNext)"], ["18%", "export sales"]],
    mixTitle: "2025 revenue by line",
    mixLabels: ["Water-based pastes", "Silicones", "Resins", "Equipment", "Other"],
    s_tech: "Hybrid technology: the best of two processes",
    steps: [
      ["Screen base", "White and effects with low-cost paste: puff, foil, glitter, discharge"],
      ["Digital color", "Ricoh or Brother heads: photographic gradients, unlimited colors"],
      ["Special effects", "Glass-like, embroidery-like or 3D silicone over the print"],
    ],
    techStats: [["400–450", "pieces per hour"], ["40–70%", "ink savings vs DTG"], ["500–5,000", "pieces: profitable run"]],
    s_model: "How CLT sells today",
    model: [
      ["Live-demo trade shows", "Tests on the customer’s fabric and same-day quote"],
      ["Turnkey package", "Machine, chemistry, installation, training and logistics"],
      ["Phased investment", "Press first, digital stations later"],
      ["ROI-based selling", "Savings in ink, operators and floor space"],
      ["Linked consumables", "Warranty with genuine chemistry and parts"],
      ["Digital lead capture", "Multilingual site and WhatsApp"],
    ],
    modelGap: "Missing in Mexico: local technical service, in-country inventory, Spanish-language support and a demo showroom",
    sec2: "The Mexican market", sec2n: "02",
    s_mkt: "An industry that needs to differentiate",
    mkt: [["MXN 91.2 B", "textile & apparel GDP (2025)"], ["102,492", "businesses"], ["519k", "jobs"], ["89%", "of exports go to the U.S."]],
    mktMsg: [
      "Low-cost imports pressure domestic makers (GDP -8.4% in 2023)",
      "2026 tariffs: up to 35% on garments from non-FTA countries, including China",
      "The answer: customization, short runs and high-value effects, exactly what hybrid printing does",
    ],
    s_size: "Market size",
    funnel: [["~102,500", "Total market: all textile businesses"], ["~1,400–1,900", "Serviceable: medium/large firms and shops with carousels"], ["30–90 lines", "Obtainable in 5 years (2–5% adoption)"]],
    sizeSide: [["US$3.6–22M", "in equipment over 5 years"], ["US$0.9–3M", "per year in consumables (50 lines)"]],
    s_geo: "Priority regions",
    geo: [
      ["1", "State of Mexico & CDMX", "Printers, brands, promotional"],
      ["1", "Jalisco", "Fashion, sportswear, domestic brands"],
      ["2", "Puebla & Tlaxcala", "Export maquila, knitwear"],
      ["2", "Guanajuato", "Knitwear, wholesale; 1–2 h from TID"],
      ["3", "Laguna, Ags., N.L., Yucatán", "Denim, IMMEX, uniforms"],
    ],
    s_comp: "Competition: the gap is local service",
    compCols: ["Type", "Players", "Reading"],
    comp: [
      ["High-end DTG", "Kornit (Sun Digital México)", "High investment"],
      ["Automatic presses", "M&R, ROQ, MHM, Anatol", "Customers for digital stations"],
      ["Chinese hybrids", "Textalk, Hanglory", "No visible local structure"],
      ["Silicones & pastes", "ScreenTec (Siltex)", "Consumables competition"],
      ["Substitutes", "DTF, sublimation", "DTF growing in short runs"],
    ],
    s_trade: "Import and regulation",
    trade: [
      ["CEB imports", "Group company incorporated in Mexico; direct China → Mexico shipping"],
      ["2026 tariffs", "5–50% on non-FTA countries; confirm lines 8443, 3215 and 3910"],
      ["16% VAT", "Creditable: affects cash flow, not cost"],
      ["USMCA", "Maquiladoras require OEKO-TEX and fast response"],
    ],
    sec3: "Why TID · VSP · CEB", sec3n: "03",
    s_group: "A group present in Mexico and the U.S.",
    group: [
      ["TID México", "Querétaro", "12 years in industrial decoration. Sales, installation and service in Mexico. 2 technicians."],
      ["VSP Printing", "Los Angeles, CA", "20+ years in industrial printing. U.S. service and technical backup. 1 technician."],
      ["CEB", "Mexico", "VSP subsidiary. Imports CLT equipment and supplies."],
    ],
    s_fit: "Strengths and how we close the gaps",
    fitL: "What we bring",
    fitLItems: ["Same turnkey model", "Consumables-driven business", "Technical service in Spanish", "Mexico + U.S. coverage", "In-house importer (CEB)"],
    fitR: "Gap → action",
    fitRItems: ["Textile experience → dedicated textile division", "Textile chemistry → CLT certification", "3 technicians → +2 textile technicians", "Textile events → FESPA México", "Demonstration → showroom with hybrid line"],
    s_team: "Dedicated team and training",
    team: [
      ["Textile sales", "Prospecting, demos, turnkey quotes and closing"],
      ["Customer service", "Consumables orders, after-sales, warranties and service scheduling"],
      ["Textile technician", "Installation, maintenance and support; +1 technician in year 2"],
    ],
    trainT: "Training program",
    train: ["Initial at CLT’s plant: machines, chemistry and certification", "Customers – machines: operation, calibration and maintenance", "Customers – products: silicones, pastes, curing and effects", "Ongoing updates with CLT engineers"],
    teamNote: "Existing support: 2 TID technicians, 1 VSP technician, CEB import and logistics",
    sec4: "Plan and investment", sec4n: "04",
    s_plan: "A four-phase commercial plan",
    plan: [["Months 0–6", "Launch", "Agreement, hiring, training, consumables, FESPA"], ["Months 6–18", "Demonstration", "Demo showroom, first 2–5 lines"], ["Months 18–36", "Scale", "Priority clusters, U.S. via VSP"], ["Year 3+", "Latin America", "Central America, Colombia, Peru, D.R."]],
    s_inv: "Initial investment",
    inv: [["Light", "~US$53k", "Demo on consignment or at an anchor shop; consumables first"], ["Base", "~US$262k", "Press + hybrid station, inventory, showroom, launch"], ["Full", "~US$450k", "Complete line incl. 6-station DTG"]],
    invRec: "Recommended",
    invNote: "Year-1 operating expense: ~US$131k (sales, customer service, technician, training, shows)",
    s_fin: "Projection: recurring revenue grows every year",
    finSeries: ["Equipment margin", "Consumables margin"],
    finYears: ["Year 1", "Year 2", "Year 3"],
    finChartTitle: "Gross margin (US$ thousands)",
    finRes: [["Year 1", "-US$37k"], ["Year 2", "+US$89k"], ["Year 3", "+US$269k"]],
    finResTitle: "Annual result",
    finNote: "Assumptions: US$150k line, 20% equipment / 35% consumables margin, ~US$36k consumption per line per year",
    sec5: "The proposal", sec5n: "05",
    s_terms: "What we request and what we commit",
    askT: "We request from CLT",
    ask: ["Exclusivity in Mexico; LatAm subject to targets", "~20% equipment / ~35% consumables margin", "Demo on consignment or 30–50% off", "Initial inventory on consignment or 90 days", "Free training and certification", "Mexican leads referred to TID / CEB"],
    giveT: "We commit to",
    give: ["Import and local inventory (CEB)", "Demo showroom and Spanish service", "Sales, customer service and textile technician", "Machine and product training", "Targets: 2 · 5 · 8 lines in years 1–3", "Quarterly reports"],
    s_risk: "Risks and mitigation",
    risk: [["Cash-strapped industry", "Phased investment and financing"], ["DTF in short runs", "Focus on volume and effects"], ["Tariffs", "Confirmed lines; PROSEC; CEB"], ["Textile learning curve", "CLT certification and industry hires"]],
    s_next: "Next steps",
    next: ["CLT formal quotation (CLT-016B, CLT-012R, SM60-85, consumables)", "Meeting with CLT’s owners to review terms", "Confirm duties with a customs broker", "Validate consumption with 10–15 shops", "Letter of intent and 6-month launch plan"],
    contact: "Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
    thanks: "Thank you",
  },
};

// CMYK: motivo visual (círculos de tinta)
const DOTS = ["0089C2", "C2185B", "F2B705", "1B1F3B"];

function build(lang) {
  const t = T[lang];
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9"; // 10 x 5.625
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = t.title;
  pres.author = "TID México";
  const C = pres.SchemeColor;

  pres.defineSlideMaster({
    title: "TITLE_DARK",
    background: { color: HEX.dk1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.6, w: 8.4, h: 1.2, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left" }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 2.9, w: 8.4, h: 0.8, fontSize: 18, color: C.accent3, align: "left" }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "SECTION_DARK",
    background: { color: HEX.dk1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 2.3, w: 8.8, h: 1.0, fontSize: 36, bold: true, color: C.background1, align: "left" }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "CONTENT",
    background: { color: HEX.lt1 },
    margin: [0.5, 0.5, 0.5, 0.5],
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.3, w: 9.0, h: 0.7, fontSize: 26, bold: true, color: C.text1, valign: "middle" }, text: "" } },
      { text: { text: t.footer, options: { x: 0.5, y: 5.25, w: 7.5, h: 0.25, fontSize: 9, color: HEX.accent5 } } },
    ],
    slideNumber: { x: 9.0, y: 5.25, w: 0.5, h: 0.25, fontSize: 9, color: HEX.accent5, align: "right" },
  });

  const dots = (s, x, y, d = 0.18, gap = 0.08) =>
    ["0089C2", "C2185B", "F2B705", "FFFFFF"].forEach((c, i) => s.addShape(pres.shapes.OVAL, { x: x + i * (d + gap), y, w: d, h: d, fill: { color: c }, line: { color: c }, objectName: "cmyk-dot" }));

  let sec = "";
  const content = (title, section) => {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section || sec });
    s.addText(title, { placeholder: "title" });
    return s;
  };
  const section = (title, num) => {
    sec = title;
    pres.addSection({ title });
    const s = pres.addSlide({ masterName: "SECTION_DARK", sectionTitle: title });
    s.addText(num, { x: 0.6, y: 1.2, w: 3, h: 1.0, fontSize: 60, bold: true, color: C.accent3, isTextBox: true, margin: 0 });
    s.addText(title, { placeholder: "title" });
    dots(s, 0.65, 3.55);
    return s;
  };
  const stat = (s, x, y, w, big, small, color) => {
    s.addText(big, { x, y, w, h: 0.7, fontSize: 30, bold: true, color: color || C.accent1, isTextBox: true, margin: 0 });
    s.addText(small, { x, y: y + 0.7, w, h: 0.6, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  };
  const card = (s, x, y, w, h, fill) =>
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill || HEX.lt2 }, line: { color: fill || HEX.lt2 } });
  const badge = (s, x, y, label, color, d = 0.42) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color } });
    s.addText(label, { x, y, w: d, h: d, fontSize: 13, bold: true, color: color === "F2B705" ? HEX.dk1 : "FFFFFF", align: "center", valign: "middle", isTextBox: true, margin: 0 });
  };
  const note = (s, text) => s.addText(text, { x: 0.5, y: 4.9, w: 9, h: 0.3, fontSize: 10, italic: true, color: C.accent5, isTextBox: true, margin: 0 });

  // 1. Portada
  pres.addSection({ title: lang === "es" ? "Inicio" : "Opening" });
  let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: lang === "es" ? "Inicio" : "Opening" });
  dots(s, 0.65, 1.2, 0.26, 0.1);
  s.addText(t.title, { placeholder: "title" });
  s.addText(t.subtitle, { placeholder: "body" });
  s.addText(t.by, { x: 0.6, y: 4.5, w: 8.8, h: 0.4, fontSize: 13, color: "CFD6E4", isTextBox: true, margin: 0 });

  // 2. Resumen ejecutivo
  s = content(t.s_exec, lang === "es" ? "Inicio" : "Opening");
  t.exec.forEach(([b, l], i) => {
    const x = 0.5 + i * 2.3;
    card(s, x, 1.25, 2.1, 2.2);
    s.addText(b, { x: x + 0.15, y: 1.45, w: 1.8, h: 0.8, fontSize: 30, bold: true, color: DOTS[i] === "F2B705" ? "B38600" : DOTS[i], isTextBox: true, margin: 0 });
    s.addText(l, { x: x + 0.15, y: 2.25, w: 1.8, h: 1.1, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addText(t.execMsg, { x: 0.5, y: 3.75, w: 9, h: 0.8, fontSize: 16, bold: true, color: C.text1, isTextBox: true, margin: 0 });

  // Sección 1
  section(t.sec1, t.sec1n);
  s = content(t.s_clt);
  t.cltStats.forEach(([b, l], i) => stat(s, 0.5 + (i % 2) * 2.3, 1.3 + Math.floor(i / 2) * 1.6, 2.1, b, l, i % 2 ? C.accent2 : C.accent1));
  s.addChart(pres.charts.DOUGHNUT, [{ name: t.mixTitle, labels: t.mixLabels, values: [53.6, 20.7, 8.1, 6.5, 11.1] }], {
    x: 5.1, y: 1.1, w: 4.4, h: 3.8, holeSize: 55, showTitle: true, title: t.mixTitle, titleFontSize: 13, titleColor: HEX.dk1, titleFontFace: "+mn-lt",
    chartColors: ["C2185B", "0089C2", "7A8299", "F2B705", "CFD6E4"], showPercent: true, showValue: false, showLegend: true, legendPos: "r",
    legendFontSize: 10, legendFontFace: "+mn-lt", dataLabelColor: "FFFFFF", dataLabelFontSize: 10, dataLabelFontFace: "+mn-lt",
  });
  note(s, "Fuente / Source: CLT 2025 annual report");

  s = content(t.s_tech);
  t.steps.forEach(([h, d], i) => {
    const x = 0.5 + i * 3.1;
    card(s, x, 1.2, 2.8, 2.0);
    badge(s, x + 0.2, 1.38, String(i + 1), DOTS[i]);
    s.addText(h, { x: x + 0.75, y: 1.38, w: 1.95, h: 0.42, fontSize: 15, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: 1.95, w: 2.45, h: 1.15, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
    if (i < 2) s.addShape(pres.shapes.CHEVRON, { x: x + 2.86, y: 2.05, w: 0.18, h: 0.3, fill: { color: HEX.accent5 }, line: { color: HEX.accent5 } });
  });
  t.techStats.forEach(([b, l], i) => stat(s, 0.5 + i * 3.1, 3.55, 2.8, b, l, i === 1 ? C.accent2 : C.accent1));

  s = content(t.s_model);
  t.model.forEach(([h, d], i) => {
    const x = 0.5 + (i % 3) * 3.05, y = 1.2 + Math.floor(i / 3) * 1.35;
    card(s, x, y, 2.85, 1.2);
    badge(s, x + 0.15, y + 0.15, String(i + 1), DOTS[i % 4], 0.36);
    s.addText(h, { x: x + 0.6, y: y + 0.12, w: 2.15, h: 0.42, fontSize: 13, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.15, y: y + 0.6, w: 2.6, h: 0.55, fontSize: 11, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 4.0, w: 9, h: 0.8, rectRadius: 0.08, fill: { color: HEX.dk1 }, line: { color: HEX.dk1 } });
  s.addText(t.modelGap, { x: 0.7, y: 4.0, w: 8.6, h: 0.8, fontSize: 14, bold: true, color: "FFFFFF", valign: "middle", isTextBox: true, margin: 0 });

  // Sección 2
  section(t.sec2, t.sec2n);
  s = content(t.s_mkt);
  t.mkt.forEach(([b, l], i) => stat(s, 0.5 + i * 2.3, 1.25, 2.1, b, l, i % 2 ? C.accent2 : C.accent1));
  t.mktMsg.forEach((m, i) => {
    badge(s, 0.5, 2.95 + i * 0.62, String(i + 1), DOTS[i], 0.36);
    s.addText(m, { x: 1.0, y: 2.95 + i * 0.62, w: 8.5, h: 0.36, fontSize: 14, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  });
  note(s, "INEGI 2023–2024 · CANAINTEX 2026 · DOF 2026");

  s = content(t.s_size);
  const fw = [5.6, 4.4, 3.2], fc = [HEX.lt2, "CFE6F2", "F8D3E1"];
  t.funnel.forEach(([b, l], i) => {
    const w = fw[i], x = 0.5 + (5.6 - w) / 2, y = 1.2 + i * 1.15;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.0, rectRadius: 0.08, fill: { color: fc[i] }, line: { color: fc[i] } });
    s.addText([{ text: b, options: { bold: true, fontSize: 20, color: i === 2 ? HEX.accent1 : HEX.dk1, breakLine: true } }, { text: l, options: { fontSize: 11, color: HEX.dk2 } }],
      { x: x + 0.1, y, w: w - 0.2, h: 1.0, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  });
  t.sizeSide.forEach(([b, l], i) => stat(s, 6.6, 1.3 + i * 1.5, 2.9, b, l, i ? C.accent2 : C.accent1));
  note(s, t.estimate);

  s = content(t.s_geo);
  t.geo.forEach(([p, z, w], i) => {
    const y = 1.15 + i * 0.72;
    card(s, 0.5, y, 9, 0.62);
    badge(s, 0.65, y + 0.1, p, p === "1" ? HEX.accent1 : p === "2" ? HEX.accent2 : HEX.accent3, 0.42);
    s.addText(z, { x: 1.25, y, w: 3.4, h: 0.62, fontSize: 15, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(w, { x: 4.7, y, w: 4.6, h: 0.62, fontSize: 13, color: C.text2, valign: "middle", isTextBox: true, margin: 0 });
  });

  s = content(t.s_comp);
  const head = t.compCols.map((c) => ({ text: c, options: { bold: true, color: "FFFFFF", fill: { color: HEX.dk1 } } }));
  const rows = t.comp.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, fill: { color: i % 2 ? HEX.lt1 : HEX.lt2 }, color: HEX.dk1 } })));
  s.addTable([head, ...rows], { x: 0.5, y: 1.2, w: 9, colW: [2.4, 3.3, 3.3], fontSize: 13, rowH: 0.52, border: { type: "solid", pt: 0.5, color: "C9D1DC" }, valign: "middle" });

  s = content(t.s_trade);
  t.trade.forEach(([h, d], i) => {
    const x = 0.5 + (i % 2) * 4.6, y = 1.2 + Math.floor(i / 2) * 1.75;
    card(s, x, y, 4.4, 1.55);
    badge(s, x + 0.2, y + 0.2, String(i + 1), DOTS[i]);
    s.addText(h, { x: x + 0.8, y: y + 0.2, w: 3.4, h: 0.42, fontSize: 16, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: y + 0.75, w: 4.0, h: 0.75, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });

  // Sección 3
  section(t.sec3, t.sec3n);
  s = content(t.s_group);
  t.group.forEach(([n, loc, d], i) => {
    const x = 0.5 + i * 3.05;
    card(s, x, 1.2, 2.85, 3.0);
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: 1.4, w: 0.5, h: 0.5, fill: { color: DOTS[i] }, line: { color: DOTS[i] } });
    s.addText(n, { x: x + 0.2, y: 2.05, w: 2.5, h: 0.45, fontSize: 18, bold: true, color: C.text1, isTextBox: true, margin: 0 });
    s.addText(loc, { x: x + 0.2, y: 2.5, w: 2.5, h: 0.35, fontSize: 12, bold: true, color: C.accent1, isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: 2.95, w: 2.5, h: 1.5, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });

  s = content(t.s_fit);
  [[t.fitL, t.fitLItems, HEX.accent2, 0.5], [t.fitR, t.fitRItems, HEX.accent1, 5.1]].forEach(([h, items, col, x]) => {
    card(s, x, 1.15, 4.4, 3.65);
    s.addText(h, { x: x + 0.25, y: 1.3, w: 3.9, h: 0.45, fontSize: 17, bold: true, color: col, isTextBox: true, margin: 0 });
    s.addText(items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < items.length - 1 } })),
      { x: x + 0.25, y: 1.85, w: 3.95, h: 2.8, fontSize: 14, color: HEX.dk1, paraSpaceAfter: 6, valign: "top", isTextBox: true, margin: 0 });
  });

  s = content(t.s_team);
  t.team.forEach(([h, d], i) => {
    const y = 1.15 + i * 1.2;
    card(s, 0.5, y, 4.6, 1.05);
    badge(s, 0.68, y + 0.3, String(i + 1), DOTS[i], 0.45);
    s.addText(h, { x: 1.3, y: y + 0.1, w: 3.65, h: 0.4, fontSize: 16, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: 1.3, y: y + 0.5, w: 3.65, h: 0.5, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.4, y: 1.15, w: 4.1, h: 3.45, rectRadius: 0.08, fill: { color: HEX.dk1 }, line: { color: HEX.dk1 } });
  s.addText(t.trainT, { x: 5.65, y: 1.3, w: 3.6, h: 0.45, fontSize: 17, bold: true, color: HEX.accent3, isTextBox: true, margin: 0 });
  s.addText(t.train.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < t.train.length - 1 } })),
    { x: 5.65, y: 1.85, w: 3.65, h: 2.6, fontSize: 14, color: "FFFFFF", paraSpaceAfter: 8, valign: "top", isTextBox: true, margin: 0 });
  note(s, t.teamNote);

  // Sección 4
  section(t.sec4, t.sec4n);
  s = content(t.s_plan);
  s.addShape(pres.shapes.LINE, { x: 0.8, y: 1.85, w: 8.4, h: 0, line: { color: HEX.accent5, width: 2 } });
  t.plan.forEach(([p, h, d], i) => {
    const x = 0.5 + i * 2.3;
    badge(s, x + 0.1, 1.6, String(i + 1), DOTS[i], 0.5);
    s.addText(p, { x, y: 2.25, w: 2.1, h: 0.35, fontSize: 12, bold: true, color: C.accent1, isTextBox: true, margin: 0 });
    s.addText(h, { x, y: 2.6, w: 2.1, h: 0.45, fontSize: 17, bold: true, color: C.text1, isTextBox: true, margin: 0 });
    s.addText(d, { x, y: 3.1, w: 2.1, h: 1.3, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });

  s = content(t.s_inv);
  t.inv.forEach(([n, v, d], i) => {
    const x = 0.5 + i * 3.05, rec = i === 1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.2, w: 2.85, h: 3.1, rectRadius: 0.08, fill: { color: rec ? HEX.dk1 : HEX.lt2 }, line: { color: rec ? HEX.dk1 : HEX.lt2 } });
    if (rec) s.addText(t.invRec, { x: x + 0.2, y: 1.35, w: 2.45, h: 0.3, fontSize: 11, bold: true, color: HEX.accent3, isTextBox: true, margin: 0 });
    s.addText(n, { x: x + 0.2, y: 1.7, w: 2.45, h: 0.4, fontSize: 17, bold: true, color: rec ? "FFFFFF" : HEX.dk1, isTextBox: true, margin: 0 });
    s.addText(v, { x: x + 0.2, y: 2.15, w: 2.45, h: 0.75, fontSize: 32, bold: true, color: rec ? HEX.accent3 : HEX.accent1, isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: 3.0, w: 2.45, h: 1.2, fontSize: 12, color: rec ? "DDE3EE" : HEX.dk2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addText(t.invNote, { x: 0.5, y: 4.45, w: 9, h: 0.35, fontSize: 13, bold: true, color: C.text1, isTextBox: true, margin: 0 });
  note(s, t.estimate);

  s = content(t.s_fin);
  s.addChart(pres.charts.BAR, [
    { name: t.finSeries[0], labels: t.finYears, values: [60, 150, 240] },
    { name: t.finSeries[1], labels: t.finYears, values: [34, 99, 209] },
  ], {
    x: 0.5, y: 1.1, w: 5.6, h: 3.7, barDir: "col", barGrouping: "stacked", chartColors: ["0089C2", "C2185B"],
    showTitle: true, title: t.finChartTitle, titleFontSize: 13, titleColor: HEX.dk1, titleFontFace: "+mn-lt",
    showValue: true, dataLabelPosition: "ctr", dataLabelColor: "FFFFFF", dataLabelFontSize: 11, dataLabelFontFace: "+mn-lt",
    showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt",
    catAxisLabelColor: HEX.dk2, valAxisLabelColor: HEX.dk2, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    valGridLine: { color: "E3E7EE", size: 0.5 }, catGridLine: { style: "none" },
  });
  s.addText(t.finResTitle, { x: 6.5, y: 1.15, w: 3, h: 0.4, fontSize: 15, bold: true, color: C.text1, isTextBox: true, margin: 0 });
  t.finRes.forEach(([y, v], i) => {
    const yy = 1.65 + i * 0.95;
    card(s, 6.5, yy, 3.0, 0.8);
    s.addText(y, { x: 6.65, y: yy, w: 1.1, h: 0.8, fontSize: 13, color: HEX.dk2, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(v, { x: 7.7, y: yy, w: 1.7, h: 0.8, fontSize: 22, bold: true, color: v.startsWith("-") ? HEX.accent1 : "2E7D32", align: "right", valign: "middle", isTextBox: true, margin: 0 });
  });
  note(s, t.finNote);

  // Sección 5
  section(t.sec5, t.sec5n);
  s = content(t.s_terms);
  [[t.askT, t.ask, HEX.accent1, 0.5], [t.giveT, t.give, HEX.accent2, 5.1]].forEach(([h, items, col, x]) => {
    card(s, x, 1.15, 4.4, 3.65);
    s.addText(h, { x: x + 0.25, y: 1.3, w: 3.9, h: 0.45, fontSize: 17, bold: true, color: col, isTextBox: true, margin: 0 });
    s.addText(items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < items.length - 1 } })),
      { x: x + 0.25, y: 1.85, w: 3.95, h: 2.85, fontSize: 14, color: HEX.dk1, paraSpaceAfter: 5, valign: "top", isTextBox: true, margin: 0 });
  });

  s = content(t.s_risk);
  t.risk.forEach(([r, m], i) => {
    const x = 0.5 + (i % 2) * 4.6, y = 1.2 + Math.floor(i / 2) * 1.75;
    card(s, x, y, 4.4, 1.55);
    badge(s, x + 0.2, y + 0.2, "!", DOTS[i]);
    s.addText(r, { x: x + 0.8, y: y + 0.2, w: 3.4, h: 0.42, fontSize: 16, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(m, { x: x + 0.2, y: y + 0.8, w: 4.0, h: 0.6, fontSize: 13, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });

  s = content(t.s_next);
  t.next.forEach((n, i) => {
    const y = 1.15 + i * 0.7;
    badge(s, 0.5, y + 0.05, String(i + 1), DOTS[i % 4], 0.45);
    s.addText(n, { x: 1.15, y, w: 8.3, h: 0.55, fontSize: 15, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  });

  // Cierre
  s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: t.sec5 });
  dots(s, 0.65, 1.2, 0.26, 0.1);
  s.addText(t.thanks, { placeholder: "title" });
  s.addText([{ text: t.contact, options: { fontSize: 14 } }], { placeholder: "body" });

  return pres;
}

// Agrega transiciones "fade" a cada diapositiva (presentación dinámica)
async function addTransitions(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    let xml = await zip.file(name).async("string");
    if (!xml.includes("<p:transition")) {
      xml = xml.replace("</p:clrMapOvr>", '</p:clrMapOvr><p:transition spd="med"><p:fade/></p:transition>');
      zip.file(name, xml);
    }
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

(async () => {
  const out = process.argv[2] || ".";
  const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");
  for (const lang of ["es", "en"]) {
    const f = path.join(out, T[lang].file + ".pptx");
    await build(lang).writeFile({ fileName: f });
    await applyTheme(f, THEME);
    await addTransitions(f);
    console.log("ok", f);
  }
})();
