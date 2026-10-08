// Presentación del estudio de mercado (ES y EN) con transiciones. Uso: node generar-ppt-estudio.js <carpeta_salida>
// Reutiliza textos de la propuesta (generar-ppt.js) y los datos de prospectos, 80/20 y FODA.
const path = require("path");
const { THEME, HEX, DOTS, IMG, makeDeck, addTransitions } = require("./ppt-base");
const { T } = require("./generar-ppt");
const top8020 = require("./top8020");
const foda = require("./foda");
const prospects = require("./prospectos.json").prospects;
const fs = require("fs");
const latam = fs.readdirSync(__dirname).filter((f) => /^latam_.*\.json$/.test(f)).sort().flatMap((f) => require(`./${f}`).prospects);

const S = {
  es: {
    file: "Estudio_Mercado_CLT_Mexico_Latam_ES",
    footer: "Estudio de mercado CLT — TID · VSP · CEB — Confidencial",
    title: "Estudio de Mercado: Impresión Híbrida Textil",
    subtitle: "Oportunidad para CLT en México, Latinoamérica y EE. UU.",
    by: "TID México · VSP Printing, Inc. · CEB  |  Octubre 2026",
    s_exec: "El estudio en una página",
    exec: [["~1,900", "empresas alcanzables en México"], ["82", "prospectos en México (35 OEM)"], ["122", "prospectos en Latinoamérica"], ["0", "distribuidores formales de híbridos chinos"]],
    execMsg: "Hay un mercado sin dueño: la industria necesita diferenciarse y nadie ofrece en México una solución híbrida con química y servicio local.",
    s_agenda: "Contenido",
    agenda: ["Alcance y metodología", "El fabricante: CLT", "Mercado mexicano", "Clientes prioritarios (80/20)", "Competencia", "Comercio exterior", "Latinoamérica y EE. UU.", "Conclusiones"],
    secs: ["Alcance y metodología", "El fabricante: CLT", "Mercado mexicano", "Clientes prioritarios", "Competencia", "Comercio exterior", "Latinoamérica y EE. UU.", "Conclusiones"],
    s_params: "Parámetros del estudio",
    paramCols: ["Parámetro", "Qué se analizó"],
    params: [
      ["Mercado", "Equipos híbridos, consumibles (siliconas, pastas, tintas) y servicio; sustitutos: serigrafía, DTG, DTF, sublimación"],
      ["Segmentos", "Maquila de exportación, estampadores industriales, uniformes y deportivo, marcas, talleres"],
      ["Tamaño", "Mercado total, alcanzable y capturable (TAM / SAM / SOM)"],
      ["Geografía", "9 zonas en México + Centroamérica, Caribe y Sudamérica"],
      ["Competencia", "DTG, pulpos automáticos, híbridos chinos, tintas y siliconas"],
      ["Comercio", "Aranceles 2026, importación vía CEB, T-MEC"],
    ],
    paramNote: "Fuentes: CLT (sitio y reporte anual 2025), INEGI, CANAINTEX, FESPA México, DOF, Open Supply Hub, sitios de cada empresa y tiendas en línea.",
    s_portfolio: "Portafolio de CLT relevante para México",
    portfolio: [
      ["Híbridas", "CLT-012R/015R/018R (Ricoh, 450 pzs/h) y CLT-014B/016B/018B (Brother, 400 pzs/h)"],
      ["Pulpos ovalados", "SM45-85, SM60-85, SM70-95: hasta 800 pzs/h, ±0.02 mm"],
      ["DTG y DTF", "DTG de 6 estaciones con pretratamiento en línea; DTF industrial CLT-6900"],
      ["Química", "Siliconas 3D, vidrio y especiales (S-1701, S-1703, S-1704-1, S-1714-1); pastas base agua"],
    ],
    portfolioNote: "Certificaciones declaradas por CLT: OEKO-TEX, GOTS, ISO 9001 e ISO 14001.",
    s_struct: "Estructura de la industria",
    sizeTitle: "Empresas por tamaño (%)",
    sizeLabels: ["Micro", "Pequeña", "Mediana", "Grande"],
    tradeStats: [["US$9,300 M", "exportaciones (89% a EE. UU.)"], ["US$13,300 M", "importaciones (35% de China)"], ["1,130", "empresas medianas y grandes: el núcleo del mercado"]],
    s_pros: "82 prospectos en 13 zonas de México",
    prosChart: "Prospectos por zona",
    prosSeries: ["Estampadores y fabricantes", "OEM"],
    prosSide: [["16", "prioridad A"], ["35", "prioridad B"], ["35", "OEM de exportación"]],
    prosNote: "Fuente: sitios de cada empresa, Open Supply Hub y directorios; detalle en el Excel de prospectos.",
    s_top1: "80/20: estampadores y fabricantes (9 de 47)",
    s_top2: "80/20: OEM de exportación (8 de 35)",
    topCols: ["Empresa", "Ciudad", "A qué se dedica"],
    topCols2: ["Empresa", "Ciudad", "Marcas y clientes"],
    topNote: "17 de 82 cuentas (20%) concentran el esfuerzo comercial del año 1",
    s_latam: "Latinoamérica: 122 prospectos en 16 países",
    latamChart: "Prospectos por región y prioridad",
    latamSide: [["27", "prioridad A"], ["45", "Centroamérica: maquila para marcas de EE. UU."], ["19 + 19", "Perú y República Dominicana"]],
    s_latamTop: "Latinoamérica: cuentas prioridad A",
    latamCols: ["Empresa", "País", "Tipo"],
    s_waves: "Ruta de expansión",
    waves: [
      ["Ola 1 · años 2–3", "El Salvador, Honduras, Guatemala", "Maquila con serigrafía para Hanes, Gildan, Tegra; venta desde México"],
      ["Ola 2 · año 3", "Perú y Colombia", "Algodón y punto de exportación; agente local con soporte de TID"],
      ["Ola 3 · años 3–4", "Rep. Dominicana, Haití y resto", "Zonas francas con serigrafía (Gildan, Hansae)"],
    ],
    usa: "EE. UU.: VSP Printing (California) da servicio local y atiende a las matrices de las OEM; CLT ya participa en PRINTING United.",
    s_concl: "Conclusiones",
    concl: [
      "La industria mexicana necesita diferenciarse frente a la importación: la impresión híbrida responde a esa necesidad.",
      "El mercado alcanzable es concentrado (~1,900 empresas): se gana con venta consultiva a pocas cuentas grandes.",
      "Nadie es dueño de la categoría: no hay distribuidor formal de híbridos chinos ni oferta llave en mano con servicio local.",
      "La competencia en tintas es premium (Avient, Matsui) o barata (ScreenTec, marcas nacionales): CLT compite con paquete y servicio.",
      "Los aranceles 2026 y el T-MEC favorecen producir en México; Centroamérica y Perú son la siguiente ola.",
    ],
    s_next: "Recomendaciones y próximos pasos",
    next: ["Cotización formal de CLT para sustituir estimaciones", "Validar consumos y precios con 10–15 talleres", "Abrir la sala demo y trabajar las 17 cuentas 80/20", "Confirmar aranceles y fracciones con agente aduanal", "Preparar la entrada a Centroamérica (año 2)"],
    thanks: "Gracias",
    contact: "Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
  },
  en: {
    file: "CLT_Market_Study_Mexico_Latam_EN",
    footer: "CLT market study — TID · VSP · CEB — Confidential",
    title: "Market Study: Hybrid Textile Printing",
    subtitle: "Opportunity for CLT in Mexico, Latin America and the U.S.",
    by: "TID México · VSP Printing, Inc. · CEB  |  October 2026",
    s_exec: "The study on one page",
    exec: [["~1,900", "reachable companies in Mexico"], ["82", "prospects in Mexico (35 OEMs)"], ["122", "prospects in Latin America"], ["0", "formal distributors of Chinese hybrids"]],
    execMsg: "A market without an owner: the industry needs to stand out, and nobody in Mexico offers a hybrid solution with local chemistry and service.",
    s_agenda: "Contents",
    agenda: ["Scope and methodology", "The manufacturer: CLT", "Mexican market", "Priority accounts (80/20)", "Competition", "Trade", "Latin America and the U.S.", "Conclusions"],
    secs: ["Scope and methodology", "The manufacturer: CLT", "Mexican market", "Priority accounts", "Competition", "Trade", "Latin America and the U.S.", "Conclusions"],
    s_params: "Study parameters",
    paramCols: ["Parameter", "What we analyzed"],
    params: [
      ["Market", "Hybrid equipment, consumables (silicones, pastes, inks) and service; substitutes: screen, DTG, DTF, sublimation"],
      ["Segments", "Export contractors, industrial printers, uniforms and sportswear, brands, shops"],
      ["Size", "Total, reachable and capturable market (TAM / SAM / SOM)"],
      ["Geography", "9 regions in Mexico + Central America, the Caribbean and South America"],
      ["Competition", "DTG, automatic carousels, Chinese hybrids, inks and silicones"],
      ["Trade", "2026 tariffs, import through CEB, USMCA"],
    ],
    paramNote: "Sources: CLT (website and 2025 annual report), INEGI, CANAINTEX, FESPA México, DOF, Open Supply Hub, company websites and online stores.",
    s_portfolio: "CLT portfolio relevant to Mexico",
    portfolio: [
      ["Hybrids", "CLT-012R/015R/018R (Ricoh, 450 pcs/h) and CLT-014B/016B/018B (Brother, 400 pcs/h)"],
      ["Oval carousels", "SM45-85, SM60-85, SM70-95: up to 800 pcs/h, ±0.02 mm"],
      ["DTG and DTF", "6-station DTG with inline pretreatment; industrial DTF CLT-6900"],
      ["Chemistry", "3D, glass and special silicones (S-1701, S-1703, S-1704-1, S-1714-1); water-based pastes"],
    ],
    portfolioNote: "Certifications stated by CLT: OEKO-TEX, GOTS, ISO 9001 and ISO 14001.",
    s_struct: "Industry structure",
    sizeTitle: "Companies by size (%)",
    sizeLabels: ["Micro", "Small", "Medium", "Large"],
    tradeStats: [["US$9.3 B", "exports (89% to the U.S.)"], ["US$13.3 B", "imports (35% from China)"], ["1,130", "medium and large firms: the core of the market"]],
    s_pros: "82 prospects in 13 regions of Mexico",
    prosChart: "Prospects by region",
    prosSeries: ["Printers and manufacturers", "OEMs"],
    prosSide: [["16", "priority A"], ["35", "priority B"], ["35", "export OEMs"]],
    prosNote: "Source: company websites, Open Supply Hub and directories; details in the prospects workbook.",
    s_top1: "80/20: printers and manufacturers (9 of 47)",
    s_top2: "80/20: export OEMs (8 of 35)",
    topCols: ["Company", "City", "What they do"],
    topCols2: ["Company", "City", "Brands and customers"],
    topNote: "17 of 82 accounts (20%) receive the year-1 sales focus",
    s_latam: "Latin America: 122 prospects in 16 countries",
    latamChart: "Prospects by region and priority",
    latamSide: [["27", "priority A"], ["45", "Central America: contractors for U.S. brands"], ["19 + 19", "Peru and Dominican Republic"]],
    s_latamTop: "Latin America: priority A accounts",
    latamCols: ["Company", "Country", "Type"],
    s_waves: "Expansion path",
    waves: [
      ["Wave 1 · years 2–3", "El Salvador, Honduras, Guatemala", "Contractors printing for Hanes, Gildan, Tegra; sold from Mexico"],
      ["Wave 2 · year 3", "Peru and Colombia", "Export cotton and knitwear; local agent with TID support"],
      ["Wave 3 · years 3–4", "Dominican Rep., Haiti and others", "Free zones with screen printing (Gildan, Hansae)"],
    ],
    usa: "U.S.: VSP Printing (California) provides local service and covers OEM headquarters; CLT already exhibits at PRINTING United.",
    s_concl: "Conclusions",
    concl: [
      "Mexico’s industry must stand out against imports: hybrid printing answers that need.",
      "The reachable market is concentrated (~1,900 firms): it is won with consultative selling to a few large accounts.",
      "Nobody owns the category: no formal distributor of Chinese hybrids and no turnkey offer with local service.",
      "Ink competition is premium (Avient, Matsui) or cheap (ScreenTec, local brands): CLT competes with package and service.",
      "2026 tariffs and USMCA favor producing in Mexico; Central America and Peru are the next wave.",
    ],
    s_next: "Recommendations and next steps",
    next: ["Formal CLT quotation to replace estimates", "Validate consumption and prices with 10–15 shops", "Open the demo room and work the 17 80/20 accounts", "Confirm tariffs and HS codes with a customs broker", "Prepare the Central America entry (year 2)"],
    thanks: "Thank you",
    contact: "Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
  },
};

// Cifras de Latinoamérica calculadas de los datos (cambian al agregar países o dar de baja empresas)
{
  const n = latam.length, a = latam.filter((x) => x.priority === "A").length;
  const nc = new Set(latam.map((x) => x.country)).size;
  const byC = (c) => latam.filter((x) => x.country === c).length;
  const ca = latam.filter((x) => x.region === "Centroamérica").length;
  S.es.exec[2][0] = String(n); S.en.exec[2][0] = String(n);
  S.es.s_latam = `Latinoamérica: ${n} prospectos en ${nc} países`;
  S.en.s_latam = `Latin America: ${n} prospects in ${nc} countries`;
  const top = [...new Set(latam.filter((x) => x.region === "Sudamérica").map((x) => x.country))].sort((x, y) => byC(y) - byC(x)).slice(0, 2);
  S.es.latamSide = [[String(a), "prioridad A"], [String(ca), "Centroamérica: maquila para marcas de EE. UU."], [`${byC(top[0])} + ${byC(top[1])}`, `${top[0]} y ${top[1]}`]];
  const en = { "Perú": "Peru", "Brasil": "Brazil", "Colombia": "Colombia" };
  S.en.latamSide = [[String(a), "priority A"], [String(ca), "Central America: contractors for U.S. brands"], [`${byC(top[0])} + ${byC(top[1])}`, `${en[top[0]] || top[0]} and ${en[top[1]] || top[1]}`]];
}

// Zona corta para la gráfica de prospectos
const ZONE = {
  "Puebla y Tlaxcala": "Puebla/Tlax.", "Estado de México y CDMX": "Edomex/CDMX", Jalisco: "Jalisco", Guanajuato: "Guanajuato",
  "Baja California (Tijuana / Ensenada / Tecate)": "Baja California", "Nuevo León (Monterrey)": "Nuevo León", "Yucatán (Mérida)": "Yucatán",
  "La Laguna (Torreón/Gómez Palacio)": "La Laguna", Querétaro: "Querétaro", Aguascalientes: "Aguascalientes",
  "Veracruz (Xalapa)": "Veracruz", "Tamaulipas (Reynosa)": "Tamaulipas", Hidalgo: "Hidalgo",
};

function build(lang) {
  const t = S[lang], p = T[lang];
  const es = lang === "es";
  const { pres, C, content, section, stat, card, badge, note, dots } = makeDeck(lang, t);
  const tbl = (s, rows, cols, colW, fs, rowH, y = 1.05) => {
    const hd = cols.map((c) => ({ text: c, options: { bold: true, color: "FFFFFF", fill: { color: HEX.dk1 } } }));
    const rw = rows.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, fill: { color: i % 2 ? HEX.lt1 : HEX.lt2 }, color: HEX.dk1 } })));
    s.addTable([hd, ...rw], { x: 0.5, y, w: 9, colW, fontSize: fs, rowH, border: { type: "solid", pt: 0.5, color: "C9D1DC" }, valign: "middle", margin: 0.05 });
  };
  const chartText = { titleFontSize: 13, titleColor: HEX.dk1, titleFontFace: "+mn-lt", legendFontSize: 10, legendFontFace: "+mn-lt",
    catAxisLabelColor: HEX.dk2, valAxisLabelColor: HEX.dk2, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    dataLabelFontFace: "+mn-lt", valGridLine: { color: "E3E7EE", size: 0.5 }, catGridLine: { style: "none" } };
  const opening = es ? "Inicio" : "Opening";

  // Portada
  pres.addSection({ title: opening });
  let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: opening });
  dots(s, 0.65, 1.2, 0.26, 0.1);
  s.addText(t.title, { placeholder: "title" });
  s.addText(t.subtitle, { placeholder: "body" });
  s.addText(t.by, { x: 0.6, y: 4.5, w: 8.8, h: 0.4, fontSize: 13, color: "CFD6E4", isTextBox: true, margin: 0 });

  // Resumen
  s = content(t.s_exec, opening);
  t.exec.forEach(([b, l], i) => {
    const x = 0.5 + i * 2.3;
    card(s, x, 1.25, 2.1, 2.2);
    s.addText(b, { x: x + 0.15, y: 1.45, w: 1.8, h: 0.8, fontSize: 30, bold: true, color: DOTS[i] === "F2B705" ? "B38600" : DOTS[i], isTextBox: true, margin: 0 });
    s.addText(l, { x: x + 0.15, y: 2.25, w: 1.8, h: 1.1, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addText(t.execMsg, { x: 0.5, y: 3.75, w: 9, h: 0.8, fontSize: 16, bold: true, color: C.text1, isTextBox: true, margin: 0 });

  // Agenda
  s = content(t.s_agenda, opening);
  t.agenda.forEach((a, i) => {
    const x = 0.5 + (i % 2) * 4.6, y = 1.15 + Math.floor(i / 2) * 0.9;
    card(s, x, y, 4.4, 0.75);
    s.addText(String(i + 1).padStart(2, "0"), { x: x + 0.2, y, w: 0.7, h: 0.75, fontSize: 20, bold: true, color: DOTS[i % 4] === "F2B705" ? "B38600" : DOTS[i % 4], valign: "middle", isTextBox: true, margin: 0 });
    s.addText(a, { x: x + 0.95, y, w: 3.3, h: 0.75, fontSize: 15, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  });

  // 01 Alcance
  section(t.secs[0], "01");
  s = content(t.s_params);
  tbl(s, t.params, t.paramCols, [2.0, 7.0], 12, 0.52);
  note(s, t.paramNote);

  // 02 CLT
  section(t.secs[1], "02");
  s = content(p.s_clt);
  p.cltStats.forEach(([b, l], i) => stat(s, 0.5 + (i % 2) * 2.3, 1.3 + Math.floor(i / 2) * 1.6, 2.1, b, l, i % 2 ? C.accent2 : C.accent1));
  s.addChart(pres.charts.DOUGHNUT, [{ name: p.mixTitle, labels: p.mixLabels, values: [53.6, 20.7, 8.1, 6.5, 11.1] }], {
    x: 5.1, y: 1.1, w: 4.4, h: 3.8, holeSize: 55, showTitle: true, title: p.mixTitle, ...chartText,
    chartColors: ["C2185B", "0089C2", "7A8299", "F2B705", "CFD6E4"], showPercent: true, showValue: false, showLegend: true, legendPos: "r",
    dataLabelColor: "FFFFFF", dataLabelFontSize: 10,
  });
  note(s, es ? "Fuente: reporte anual 2025 de CLT" : "Source: CLT 2025 annual report");

  s = content(t.s_portfolio);
  t.portfolio.forEach(([h, d], i) => {
    const x = 0.5 + (i % 2) * 4.6, y = 1.2 + Math.floor(i / 2) * 1.7;
    card(s, x, y, 4.4, 1.5);
    badge(s, x + 0.2, y + 0.2, String(i + 1), DOTS[i]);
    s.addText(h, { x: x + 0.8, y: y + 0.2, w: 3.4, h: 0.42, fontSize: 16, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: y + 0.75, w: 4.0, h: 0.7, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });
  note(s, t.portfolioNote);

  s = content(p.s_tech);
  p.steps.forEach(([h, d], i) => {
    const x = 0.5 + i * 3.1;
    card(s, x, 1.2, 2.8, 2.0);
    badge(s, x + 0.2, 1.38, String(i + 1), DOTS[i]);
    s.addText(h, { x: x + 0.75, y: 1.38, w: 1.95, h: 0.42, fontSize: 15, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: 1.95, w: 2.45, h: 1.15, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
    if (i < 2) s.addShape(pres.shapes.CHEVRON, { x: x + 2.86, y: 2.05, w: 0.18, h: 0.3, fill: { color: HEX.accent5 }, line: { color: HEX.accent5 } });
  });
  p.techStats.forEach(([b, l], i) => stat(s, 0.5 + i * 3.1, 3.55, 2.8, b, l, i === 1 ? C.accent2 : C.accent1));

  s = content(p.s_model);
  p.model.forEach(([h, d], i) => {
    const x = 0.5 + (i % 3) * 3.05, y = 1.2 + Math.floor(i / 3) * 1.35;
    card(s, x, y, 2.85, 1.2);
    badge(s, x + 0.15, y + 0.15, String(i + 1), DOTS[i % 4], 0.36);
    s.addText(h, { x: x + 0.6, y: y + 0.12, w: 2.15, h: 0.42, fontSize: 13, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.15, y: y + 0.6, w: 2.6, h: 0.55, fontSize: 11, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 4.0, w: 9, h: 0.8, rectRadius: 0.08, fill: { color: HEX.dk1 }, line: { color: HEX.dk1 } });
  s.addText(p.modelGap, { x: 0.7, y: 4.0, w: 8.6, h: 0.8, fontSize: 14, bold: true, color: "FFFFFF", valign: "middle", isTextBox: true, margin: 0 });

  [[p.s_gal1, p.gal1], [p.s_gal2, p.gal2]].forEach(([title, items]) => {
    s = content(title);
    items.forEach(([f, cap], i) => {
      const x = 0.5 + i * 2.3;
      s.addImage({ path: IMG(f), x, y: 1.15, w: 2.1, h: 2.85, sizing: { type: "cover", w: 2.1, h: 2.85 }, altText: cap });
      s.addText(cap, { x, y: 4.1, w: 2.1, h: 0.6, fontSize: 11, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
    });
  });
  s = content(p.s_booth);
  s.addImage({ path: IMG("06-stand-printing-united.jpg"), x: 0.5, y: 1.1, w: 5.6, h: 3.6, sizing: { type: "cover", w: 5.6, h: 3.6 }, altText: p.s_booth });
  p.boothSide.forEach(([b, l], i) => stat(s, 6.4, 1.15 + i * 1.3, 3.1, b, l, i ? C.accent2 : C.accent1));
  s.addText(p.booth, { x: 6.4, y: 3.75, w: 3.1, h: 1.0, fontSize: 12, bold: true, color: C.text1, isTextBox: true, margin: 0, valign: "top" });

  // 03 Mercado mexicano
  section(t.secs[2], "03");
  s = content(p.s_mkt);
  p.mkt.forEach(([b, l], i) => stat(s, 0.5 + i * 2.3, 1.25, 2.1, b, l, i % 2 ? C.accent2 : C.accent1));
  p.mktMsg.forEach((m, i) => {
    badge(s, 0.5, 2.95 + i * 0.62, String(i + 1), DOTS[i], 0.36);
    s.addText(m, { x: 1.0, y: 2.95 + i * 0.62, w: 8.5, h: 0.36, fontSize: 14, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  });
  note(s, "INEGI 2023–2024 · CANAINTEX 2026 · DOF 2026");

  s = content(t.s_struct);
  s.addChart(pres.charts.BAR, [{ name: t.sizeTitle, labels: t.sizeLabels, values: [95.6, 3.3, 0.8, 0.3] }], {
    x: 0.5, y: 1.1, w: 5.4, h: 3.7, barDir: "bar", chartColors: ["0089C2"], showTitle: true, title: t.sizeTitle, ...chartText,
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: HEX.dk1, dataLabelFontSize: 11, dataLabelFormatCode: "0.0",
    showLegend: false, valAxisHidden: true, valGridLine: { style: "none" },
  });
  t.tradeStats.forEach(([b, l], i) => stat(s, 6.3, 1.2 + i * 1.2, 3.2, b, l, [C.accent1, C.accent2, C.accent1][i]));
  note(s, "INEGI (Censo 2019 y 2023)");

  s = content(p.s_size);
  const fw = [5.6, 4.4, 3.2], fc = [HEX.lt2, "CFE6F2", "F8D3E1"];
  p.funnel.forEach(([b, l], i) => {
    const w = fw[i], x = 0.5 + (5.6 - w) / 2, y = 1.2 + i * 1.15;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.0, rectRadius: 0.08, fill: { color: fc[i] }, line: { color: fc[i] } });
    s.addText([{ text: b, options: { bold: true, fontSize: 20, color: i === 2 ? HEX.accent1 : HEX.dk1, breakLine: true } }, { text: l, options: { fontSize: 11, color: HEX.dk2 } }],
      { x: x + 0.1, y, w: w - 0.2, h: 1.0, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  });
  p.sizeSide.forEach(([b, l], i) => stat(s, 6.6, 1.3 + i * 1.5, 2.9, b, l, i ? C.accent2 : C.accent1));
  note(s, p.estimate);

  s = content(p.s_geo);
  p.geo.forEach(([pr, z, w], i) => {
    const y = 1.1 + i * 0.63;
    card(s, 0.5, y, 9, 0.55);
    badge(s, 0.65, y + 0.065, pr, pr === "1" ? HEX.accent1 : pr === "2" ? HEX.accent2 : HEX.accent3, 0.42);
    s.addText(z, { x: 1.25, y, w: 3.4, h: 0.55, fontSize: 15, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(w, { x: 4.7, y, w: 4.6, h: 0.55, fontSize: 13, color: C.text2, valign: "middle", isTextBox: true, margin: 0 });
  });

  // Prospectos por zona (datos reales del estudio)
  s = content(t.s_pros);
  const zones = [...new Set(prospects.map((x) => x.zone))]
    .map((z) => ({ z, oem: prospects.filter((x) => x.zone === z && x.segment === "OEM").length, pr: prospects.filter((x) => x.zone === z && x.segment !== "OEM").length }))
    .sort((a, b) => b.oem + b.pr - (a.oem + a.pr));
  s.addChart(pres.charts.BAR, [
    { name: t.prosSeries[0], labels: zones.map((x) => ZONE[x.z] || x.z), values: zones.map((x) => x.pr) },
    { name: t.prosSeries[1], labels: zones.map((x) => ZONE[x.z] || x.z), values: zones.map((x) => x.oem) },
  ], {
    x: 0.5, y: 1.05, w: 6.0, h: 3.8, barDir: "bar", barGrouping: "stacked", chartColors: ["0089C2", "C2185B"], showTitle: true, title: t.prosChart, ...chartText,
    showLegend: true, legendPos: "b", catAxisOrientation: "maxMin", catAxisLabelFontSize: 10, valAxisLabelFontSize: 9,
  });
  const cnt = (k, v) => prospects.filter((x) => x[k] === v).length;
  [[String(cnt("priority", "A")), t.prosSide[0][1]], [String(cnt("priority", "B")), t.prosSide[1][1]], [String(cnt("segment", "OEM")), t.prosSide[2][1]]]
    .forEach(([b, l], i) => stat(s, 6.9, 1.2 + i * 1.2, 2.6, b, l, [C.accent1, C.accent2, C.accent1][i]));
  note(s, t.prosNote);

  // 04 Clientes prioritarios
  section(t.secs[3], "04");
  [[t.s_top1, top8020.prospects, t.topCols, 2], [t.s_top2, top8020.oems, t.topCols2, 4]].forEach(([title, list, cols, k]) => {
    s = content(title);
    tbl(s, list.map((r) => [r[0], r[1], r[es ? k : k + 1]]), cols, [2.3, 1.5, 5.2], 9, 0.34);
    note(s, t.topNote);
  });

  // 05 Competencia
  section(t.secs[4], "05");
  s = content(p.s_comp);
  tbl(s, p.comp, p.compCols, [2.4, 3.3, 3.3], 13, 0.52, 1.2);
  const f = foda[lang];
  s = content(f.inksTitle);
  tbl(s, f.inks.map((r) => [r[0], r[2], r[3]]), [f.inksCols[0], f.inksCols[2], f.inksCols[3]], [3.3, 3.9, 1.8], 9, 0.36);
  note(s, f.inksNote);
  s = content(f.swotTitle);
  tbl(s, f.swot, f.swotCols, [1.6, 1.85, 1.85, 1.85, 1.85], 9, 0.58);
  s = content(es ? "FODA: posición de CLT + TID frente a la competencia" : "SWOT: CLT + TID position against the competition");
  [["F", HEX.accent2], ["D", HEX.accent5], ["O", "2E7D32"], ["A", HEX.accent1]].forEach(([key, col], i) => {
    const x = 0.5 + (i % 2) * 4.6, y = 1.1 + Math.floor(i / 2) * 1.9;
    card(s, x, y, 4.4, 1.75);
    s.addText(f.ourLabels[key], { x: x + 0.2, y: y + 0.1, w: 4.0, h: 0.4, fontSize: 15, bold: true, color: col, isTextBox: true, margin: 0 });
    s.addText(f.our[key].map((it, n) => ({ text: it, options: { bullet: true, breakLine: n < f.our[key].length - 1 } })),
      { x: x + 0.2, y: y + 0.5, w: 4.0, h: 1.2, fontSize: 11, color: HEX.dk1, paraSpaceAfter: 3, valign: "top", isTextBox: true, margin: 0 });
  });

  // 06 Comercio exterior
  section(t.secs[5], "06");
  s = content(p.s_trade);
  p.trade.forEach(([h, d], i) => {
    const x = 0.5 + (i % 2) * 4.6, y = 1.2 + Math.floor(i / 2) * 1.75;
    card(s, x, y, 4.4, 1.55);
    badge(s, x + 0.2, y + 0.2, String(i + 1), DOTS[i]);
    s.addText(h, { x: x + 0.8, y: y + 0.2, w: 3.4, h: 0.42, fontSize: 16, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: y + 0.75, w: 4.0, h: 0.75, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });

  // 07 Latinoamérica y EE. UU.
  section(t.secs[6], "07");
  s = content(t.s_latam);
  const regions = es ? ["Centroamérica", "Caribe", "Sudamérica"] : ["Central America", "Caribbean", "South America"];
  const regKey = ["Centroamérica", "Caribe", "Sudamérica"];
  s.addChart(pres.charts.BAR, ["A", "B", "C"].map((pr) => ({
    name: (es ? "Prioridad " : "Priority ") + pr, labels: regions, values: regKey.map((r) => latam.filter((x) => x.region === r && x.priority === pr).length),
  })), {
    x: 0.5, y: 1.05, w: 5.8, h: 3.8, barDir: "col", barGrouping: "stacked", chartColors: ["C2185B", "0089C2", "CFD6E4"], showTitle: true, title: t.latamChart, ...chartText,
    showValue: true, dataLabelColor: "FFFFFF", dataLabelFontSize: 10, showLegend: true, legendPos: "b",
  });
  t.latamSide.forEach(([b, l], i) => stat(s, 6.7, 1.2 + i * 1.2, 2.8, b, l, [C.accent1, C.accent2, C.accent1][i]));

  s = content(t.s_latamTop);
  const typeEn = { "OEM / maquila de paquete completo": "OEM / full-package contractor", "Estampador por contrato": "Contract printer", "Fabricante de ropa deportiva/uniformes": "Sportswear / uniform maker" };
  const latA = latam.filter((x) => x.priority === "A").sort((x, y) => (y.foco ? 1 : 0) - (x.foco ? 1 : 0)).slice(0, 12)
    .map((x) => [x.company.replace(/\s*\(.*\)$/, "").replace(/,? S\.A\.( de C\.V\.)?|,? S\.A\.C\.|,? Ltda\. de C\.V\./g, ""), x.country, es ? x.type : typeEn[x.type] || x.type]);
  tbl(s, latA, t.latamCols, [4.2, 1.8, 3.0], 9, 0.29);
  note(s, es ? "Primero las 8 cuentas foco (estampado en volumen o equipo M&R / híbrido); el resto de prioridad A está en el Excel." : "Focus accounts first (volume printing or M&R / hybrid equipment); the rest of priority A is in the workbook.");

  s = content(t.s_waves);
  t.waves.forEach(([h, c, d], i) => {
    const x = 0.5 + i * 3.05;
    card(s, x, 1.2, 2.85, 2.6);
    badge(s, x + 0.2, 1.38, String(i + 1), DOTS[i]);
    s.addText(h, { x: x + 0.75, y: 1.38, w: 2.0, h: 0.42, fontSize: 13, bold: true, color: C.accent1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(c, { x: x + 0.2, y: 1.95, w: 2.5, h: 0.6, fontSize: 15, bold: true, color: C.text1, isTextBox: true, margin: 0, valign: "top" });
    s.addText(d, { x: x + 0.2, y: 2.6, w: 2.5, h: 1.1, fontSize: 12, color: C.text2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 4.0, w: 9, h: 0.8, rectRadius: 0.08, fill: { color: HEX.dk1 }, line: { color: HEX.dk1 } });
  s.addText(t.usa, { x: 0.7, y: 4.0, w: 8.6, h: 0.8, fontSize: 13, bold: true, color: "FFFFFF", valign: "middle", isTextBox: true, margin: 0 });

  // 08 Conclusiones
  section(t.secs[7], "08");
  s = content(t.s_concl);
  t.concl.forEach((n, i) => {
    const y = 1.1 + i * 0.75;
    badge(s, 0.5, y + 0.07, String(i + 1), DOTS[i % 4], 0.45);
    s.addText(n, { x: 1.15, y, w: 8.3, h: 0.6, fontSize: 14, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  });
  s = content(t.s_next);
  t.next.forEach((n, i) => {
    const y = 1.15 + i * 0.7;
    badge(s, 0.5, y + 0.05, String(i + 1), DOTS[i % 4], 0.45);
    s.addText(n, { x: 1.15, y, w: 8.3, h: 0.55, fontSize: 15, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  });

  s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: t.secs[7] });
  dots(s, 0.65, 1.2, 0.26, 0.1);
  s.addText(t.thanks, { placeholder: "title" });
  s.addText([{ text: t.contact, options: { fontSize: 14 } }], { placeholder: "body" });
  return pres;
}

(async () => {
  const out = process.argv[2] || ".";
  const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");
  for (const lang of ["es", "en"]) {
    const f = path.join(out, S[lang].file + ".pptx");
    await build(lang).writeFile({ fileName: f });
    await applyTheme(f, THEME);
    await addTransitions(f);
    console.log("ok", f);
  }
})();
