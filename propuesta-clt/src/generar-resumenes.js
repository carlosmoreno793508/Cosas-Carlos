// Resúmenes ejecutivos para inversionistas: México y LATAM/Caribe. Uso: node generar-resumenes.js <carpeta_salida>
const fs = require("fs");
const path = require("path");
const { Packer } = require("docx");
const { buildDoc } = require("./generar-doc");

const MAPAS = path.join(__dirname, "..", "mapas");
const latam = fs.readdirSync(__dirname).filter((f) => /^latam_.*\.json$/.test(f)).flatMap((f) => require(`./${f}`).prospects);
const mx = require("./prospectos.json").prospects;

// Conteos calculados de los datos (no fijos)
const nA = latam.filter((x) => x.priority === "A").length;
const nOEM = latam.filter((x) => x.segment === "OEM").length;
const nPaises = new Set(latam.map((x) => x.country)).size;
const byC = {};
latam.forEach((x) => { byC[x.country] = byC[x.country] || [0, 0]; byC[x.country][0]++; if (x.priority === "A") byC[x.country][1]++; });
const ranking = Object.entries(byC).sort((a, b) => b[1][0] - a[1][0]);
const top = ranking.slice(0, 8), rest = ranking.slice(8);
const restN = rest.reduce((s, [, v]) => s + v[0], 0), restA = rest.reduce((s, [, v]) => s + v[1], 0);
const region = (c) => latam.find((x) => x.country === c).region;
const mxOEM = mx.filter((x) => x.segment === "OEM").length;
const mxA = mx.filter((x) => x.priority === "A").length;

const metaBase = {
  preparedBy: "Preparado por: TID México · VSP Printing, Inc. · CEB",
  preparedFor: "Para: inversionistas y socios del grupo",
  date: "Octubre 2026",
  conf: "Documento confidencial",
  contact: "Contacto: Carlos Moreno — TID México · carlos.moreno@tidmexico.com.mx · +52 446 479 4420",
  estimateNote: "Las cifras marcadas como «estimación» son cálculos propios con fuentes públicas; se confirmarán con la cotización formal de CLT.",
};

const mexico = {
  meta: { ...metaBase, file: "Resumen_Ejecutivo_Mexico_ES", title: "Resumen Ejecutivo: México", subtitle: "Distribución de la impresión híbrida textil de CLT (serigrafía + digital)", footer: "Resumen ejecutivo México — Confidencial" },
  body: [
    { h1: "La oportunidad en una página" },
    { p: "TID México, VSP Printing y su importadora CEB proponen ser el distribuidor exclusivo en México de CLT (Dongguan Changlian New Material Technology, Bolsa de Shenzhen 301618). CLT fabrica impresoras híbridas que combinan serigrafía y digital en una sola pasada, y la química que consumen: siliconas, pastas base agua y tintas. Hoy no tiene distribuidor formal en México." },
    {
      bullets: [
        "Mercado en crecimiento: la impresión textil digital en México vale US$116.5 millones (2024) y llegará a US$217.6 millones en 2030, con 11.5% de crecimiento anual. El segmento que más crece es la impresión directa sobre prenda, donde compite la híbrida (Grand View Research).",
        "Sin competencia directa: no encontramos un distribuidor de impresión híbrida china con inventario, refacciones, técnicos y química en México. Epson domina el digital puro (~60%, según Epson), pero no vende serigrafía ni química.",
        "Momento favorable: los aranceles de 2026 (hasta 35% a prendas de países sin tratado) y el nearshoring empujan producción a México, que necesita diferenciarse con efectos de alto valor y entrega rápida.",
        `Clientes identificados: ${mx.length} prospectos en 13 zonas (${mxOEM} maquilas de exportación OEM), con 17 cuentas prioritarias que fabrican para Nike, Disney, Fanatics, adidas, Puma y Columbia.`,
        "Negocio recurrente: cada línea instalada consume ~US$36 mil al año en química (estimación). Además se vende química a talleres que no compran máquina.",
        "Inversión acotada: ~US$262 mil en el escenario base, con recuperación durante el año 3 (estimación).",
      ],
    },

    { h1: "El fabricante: CLT" },
    {
      table: {
        cols: ["Indicador", "Dato"],
        widths: [3600, 5760],
        rows: [
          ["Empresa", "Fundada en 2009 en Dongguan, China; cotiza en la Bolsa de Shenzhen (ChiNext) desde 2024"],
          ["Ventas 2025", "¥568 millones (~US$80 M); utilidad neta ~US$6 M"],
          ["Mezcla de ventas", "Pastas base agua 54%, siliconas 21%, resinas 8%, equipos 6.5%; exportación 18%"],
          ["Tecnología híbrida", "Base blanca con serigrafía y color digital en una pasada; 40–70% menos tinta que DTG puro; rentable de 500 a 5,000 piezas"],
          ["Certificaciones", "OEKO-TEX, GOTS, ISO 9001 e ISO 14001 (requisito de las marcas de exportación)"],
        ],
      },
    },
    { note: "Fuente: reporte anual 2025 de CLT. Tipo de cambio de referencia ¥7.1 por US$." },

    { h1: "El mercado mexicano" },
    {
      table: {
        cols: ["Indicador", "Dato", "Fuente"],
        widths: [3000, 4160, 2200],
        rows: [
          ["Impresión textil digital", "US$116.5 M (2024) → US$217.6 M (2030), +11.5% anual", "Grand View Research"],
          ["Empresas textiles y de confección", "102,492 unidades económicas", "INEGI 2023"],
          ["Núcleo del mercado", "~1,130 empresas medianas y grandes", "INEGI"],
          ["Clientes alcanzables", "1,400–1,900 (medianas/grandes y talleres con pulpo automático)", "Estimación propia"],
          ["Exportaciones", "US$9,300 millones; 89% a EE. UU.", "INEGI 2023"],
          ["Zonas prioritarias", "Edomex/CDMX, Jalisco y Baja California; después Puebla/Tlaxcala y Guanajuato", "Estudio propio"],
        ],
      },
    },
    { h2: "Evidencia de demanda" },
    {
      bullets: [
        "Fortune Fashions Baja (Mad Engine, Ensenada) importó US$8.3 millones en tintas de serigrafía entre 2022 y 2025: ~US$2.2 millones al año, una sola planta (registros de comercio exterior).",
        "Las maquilas de Baja California y Yucatán estampan para Disney, Fanatics, Nike y Columbia, y ya trabajan con pulpos automáticos: son clientes naturales para agregar estaciones digitales.",
        "Los talleres nacionales compiten contra importación barata y DTF; la híbrida les da color fotográfico con el costo de la serigrafía.",
      ],
    },
    { img: path.join(MAPAS, "Mapa_Prospectos_OEM.png"), w: 600, h: 383, alt: "Mapa de prospectos OEM", caption: "Prospectos OEM en México, Centroamérica y Caribe. Estrella dorada: cuenta 80/20 o prioridad A." },

    { h1: "Cuentas prioritarias (80/20)" },
    {
      table: {
        cols: ["Maquilas de exportación (OEM)", "Clientes que atienden"],
        widths: [4400, 4960],
        rows: [
          ["Vertical Knits (Yucatán)", "Nike, Fanatics, Tommy Hilfiger, Patagonia"],
          ["Ink Throwers de México (Tijuana)", "Disney, Levi's, Marvel"],
          ["MD International, Fortune Fashions, SOIR y Factory 1 (Ensenada)", "Fanatics, Mad Engine, Disney, Columbia, REI"],
          ["Codipsa (Puebla)", "Puma, Gap, Hot Topic, Macy's, Disney"],
          ["Industrias Manufactureras MYR (Irapuato)", "adidas, Puma (jerseys Selección Mexicana y Liga MX)"],
        ],
      },
    },
    { p: "Estampadores y marcas nacionales: ADN Serigrafía, Grupo Martex, GOCA'S, SerigrafiarteSP (CDMX y Edomex), Serigrafía Textil Automatizada (Puebla), Reitex (Nuevo León), Diermi y Uniformes Carmen (Jalisco), Charly (León)." },

    { h1: "Modelo de negocio y números" },
    {
      table: {
        bold: true,
        cols: ["Escenario base (estimación)", "Año 1", "Año 2", "Año 3"],
        widths: [3960, 1800, 1800, 1800],
        rows: [
          ["Líneas híbridas vendidas", "2", "5", "8"],
          ["Ventas (equipos + consumibles)", "~US$0.4 M", "~US$1.0 M", "~US$1.8 M"],
          ["Margen por equipos (20%)", "US$60k", "US$150k", "US$240k"],
          ["Margen por consumibles (35%)", "US$34k", "US$99k", "US$209k"],
          ["Gastos de operación", "-US$131k", "-US$160k", "-US$180k"],
          ["Resultado del año", "-US$37k", "+US$89k", "+US$269k"],
          ["Resultado acumulado", "-US$37k", "+US$52k", "+US$321k"],
        ],
      },
    },
    {
      bullets: [
        "Inversión inicial: ~US$262 mil en el escenario base: equipo de demostración, importación, sala de demostración, inventario, refacciones, capacitación y lanzamiento. Hay un escenario ligero de ~US$53 mil, con equipo en consignación de CLT, y uno completo de ~US$450 mil.",
        "Meta conservadora: las ventas del año 3 equivalen a ~1% del mercado digital y ~3–4% de la impresión sobre prenda. Con 30–90 líneas en 5 años, la venta anual llegaría a US$2–8 millones (1–3.5% del mercado de 2030).",
        "El margen crece con la base instalada: la química pasa de ~1/3 del margen en el año 1 a casi la mitad en el año 3.",
      ],
    },

    { h1: "Por qué este grupo" },
    {
      bullets: [
        "Mismo modelo: TID ya vende proyectos llave en mano con máquina, consumibles, capacitación y servicio.",
        "Cobertura de Norteamérica con un solo socio: TID en Querétaro, VSP en Los Ángeles y CEB como importadora propia en México.",
        "Servicio técnico local en español: lo que CLT no puede dar desde China y lo que el cliente industrial exige.",
      ],
    },

    { h1: "Riesgos principales" },
    {
      table: {
        cols: ["Riesgo", "Mitigación"],
        widths: [3600, 5760],
        rows: [
          ["Industria textil en contracción", "Inversión por etapas; estaciones digitales sobre pulpos existentes; financiamiento al cliente"],
          ["DTF en tirajes cortos", "Enfoque en volumen (500–5,000 piezas) y efectos que el DTF no logra"],
          ["Aprobaciones de tintas de las marcas", "Certificaciones OEKO-TEX/GOTS de CLT; pruebas con las maquilas ancla"],
          ["Curva de aprendizaje textil", "Certificación en la planta de CLT y contratación de personal del sector"],
          ["Aranceles y tipo de cambio", "Importación directa vía CEB, PROSEC y precios en dólares"],
        ],
      },
    },

    { h1: "Lo que se decide y próximos pasos" },
    {
      bullets: [
        "Aprobar el escenario base de inversión (~US$262 mil) o el ligero (~US$53 mil) mientras se negocia con CLT.",
        "Negociar con CLT: exclusividad en México, margen de 20% en equipos y 35% en consumibles, equipo de demostración en consignación o con 30–50% de descuento, y capacitación sin costo.",
        "Recibir la cotización formal de CLT para sustituir las estimaciones, y validar consumos con 10–15 clientes.",
        "Firmar carta de intención y arrancar el plan de 6 meses: sala de demostración, FESPA México y visitas a las 17 cuentas prioritarias.",
      ],
    },
  ],
};

const filas = top.map(([c, [n, a]]) => [c, region(c), String(n), String(a)]);
filas.push([`Otros ${rest.length} países`, rest.map(([c]) => c).join(", "), String(restN), String(restA)]);
filas.push(["Total", `${nPaises} países`, String(latam.length), String(nA)]);

const latamDoc = {
  meta: { ...metaBase, file: "Resumen_Ejecutivo_LATAM_Caribe_ES", title: "Resumen Ejecutivo: Latinoamérica y Caribe", subtitle: "Expansión de la impresión híbrida textil de CLT después de México", footer: "Resumen ejecutivo LATAM y Caribe — Confidencial" },
  body: [
    { h1: "La oportunidad en una página" },
    { p: "Después de consolidar México, el grupo propone llevar la impresión híbrida y la química de CLT a Latinoamérica y el Caribe desde el año 2. La región combina dos mercados: las maquilas de exportación de Centroamérica y el Caribe, que estampan para marcas de EE. UU., y los mercados de marca propia de Colombia, Perú y Brasil." },
    {
      bullets: [
        "Crecimiento: la impresión textil digital en Latinoamérica crecerá ~11.8% al año hasta 2034; Brasil y México son los mercados líderes (Cannata Report).",
        `Base de clientes identificada: ${latam.length} empresas en ${nPaises} países, ${nA} de prioridad A y ${nOEM} maquilas de exportación (OEM).`,
        "Mismo cliente que en México: las maquilas de Centroamérica y el Caribe fabrican para Hanes, Gildan, Nike y Under Armour, y se pueden atender desde México y desde VSP en EE. UU., donde están sus matrices.",
        "Condición de entrada: México primero. La expansión arranca cuando haya al menos 5 líneas instaladas en México y casos de éxito documentados.",
      ],
    },

    { h1: "Dónde están los clientes" },
    { table: { cols: ["País", "Región", "Empresas", "Prioridad A"], widths: [2400, 3760, 1600, 1600], bold: true, rows: filas } },
    { img: path.join(MAPAS, "diapositivas", "Mapa_LATAM_Estampadores_Fabricantes_ES.png"), w: 600, h: 310, alt: "Mapa LATAM de estampadores y fabricantes", caption: "Estampadores y fabricantes en México, Centroamérica, Caribe y Sudamérica. Estrella dorada: 80/20 en México o prioridad A." },

    { h1: "Cuentas foco" },
    {
      table: {
        cols: ["Empresa", "País", "Por qué"],
        widths: [3200, 1900, 4260],
        rows: [
          ["Cygnus Investments", "El Salvador", "Planta de serigrafía nearshore (2021) que ya ofrece impresión híbrida digital + serigrafía"],
          ["Techno Screen", "El Salvador", "Más de 60 millones de estampados al año en serigrafía, sublimación y digital"],
          ["ACSA Colors Printing", "Guatemala", "Serigrafía de prendas en la zona industrial de Mixco"],
          ["TCPL y The Willbes (mismo grupo)", "Rep. Dominicana y Haití", "Confección y estampado para Gap en zonas francas; una sola negociación cubre tres plantas"],
          ["Topy Top", "Perú", "Primer exportador peruano de prendas de punto; estampado propio y DTG desde 2023"],
          ["Industrias Nettalco", "Perú", "Exportador líder de prendas de punto con estampado digital propio"],
          ["CO&TEX (Coytex)", "Colombia", "~500 mil prendas al mes para Arturo Calle; puede internalizar el estampado"],
          ["Grupo Dass y Grupo Malwee", "Brasil", "Grandes fabricantes con estampado propio: Dass produce para Umbro, Fila y New Balance; Malwee, 35–45 millones de piezas al año"],
        ],
      },
    },

    { h1: "Ruta de expansión" },
    {
      table: {
        cols: ["Etapa", "Países", "Cómo"],
        widths: [1900, 2860, 4600],
        rows: [
          ["Ola 1 · años 2–3", "El Salvador, Guatemala, Honduras", "Maquila para marcas de EE. UU.; venta y servicio desde México, con apoyo de VSP ante las matrices"],
          ["Ola 2 · año 3", "Colombia y Perú", "Mercados con marca propia y exportación de punto; agente local con soporte técnico de TID"],
          ["Ola 3 · años 3–4", "Rep. Dominicana, Haití y Brasil", "Zonas francas del Caribe; en Brasil, socio local por idioma, registro y aranceles de importación"],
        ],
      },
    },
    {
      bullets: [
        "La inversión es por país y se activa por metas: el modelo de México (equipo de demostración, inventario y técnico) se replica con un agente local en lugar de una oficina propia.",
        "Lo que se pide a CLT: extensión de la exclusividad a la región sujeta a metas, fondo cooperativo de marketing de 3–5% de las compras y apoyo de un ingeniero en cada lanzamiento.",
      ],
    },

    { h1: "Riesgos" },
    {
      table: {
        cols: ["Riesgo", "Mitigación"],
        widths: [3600, 5760],
        rows: [
          ["Distancia y costo del servicio técnico", "Agentes locales capacitados por TID; inventario de refacciones en México"],
          ["Inestabilidad política (Haití) y cierres de plantas", "Priorizar grupos con varias plantas (Willbes) y países estables"],
          ["Aranceles y registro en Brasil", "Entrar con socio local; evaluar la cadena de importación antes de invertir"],
          ["Datos de prospectos por verificar", "Parte de las empresas de Brasil y Colombia solo tiene fuentes de prensa o directorio; se validan antes de cada ola"],
        ],
      },
    },

    { h1: "Lo que se decide" },
    {
      bullets: [
        "Aprobar la expansión por olas, condicionada a resultados en México (5 líneas y casos documentados).",
        "Incluir la región en la negociación con CLT desde ahora, para asegurar la exclusividad por metas.",
        "Presupuestar la validación de las cuentas foco en el año 2: visitas a El Salvador y Guatemala, y contacto con los grupos de Perú y República Dominicana.",
      ],
    },
  ],
};

(async () => {
  const out = process.argv[2] || ".";
  for (const d of [mexico, latamDoc]) {
    const f = path.join(out, d.meta.file + ".docx");
    fs.writeFileSync(f, await Packer.toBuffer(buildDoc(d)));
    console.log("ok", f);
  }
})();
