// FODA de la competencia en tintas y consumibles textiles (sección 8). Precios públicos de referencia, octubre 2026.
const es = {
  inksTitle: "Competidores en tintas, pastas y siliconas",
  inksCols: ["Marca (origen)", "Presencia en México", "Precio de referencia", "Amenaza"],
  inks: [
    ["Avient: Wilflex, Rutland, Union Ink, Printop (EE. UU.)", "Casa Díaz y distribuidores; estándar en maquila de exportación", "Alto: ~US$40–60/galón en colores de mezcla; especialidades US$90–310/galón (tiendas de EE. UU.)", "Alta en OEM"],
    ["Grupo Sánchez / ScreenTec: Seritex, Aquatex, Siltex (México)", "Fabricante nacional con red de distribuidores", "Bajo: MXN 159–217/kg al menudeo (Seritex)", "Alta en talleres"],
    ["Matsui (Japón)", "Casa Díaz; referencia en base agua y descarga", "Medio-alto; bases desde ~US$8–9/kg en Centroamérica", "Media-alta"],
    ["International Coatings (EE. UU.)", "Importación vía distribuidores de EE. UU.", "Medio", "Media"],
    ["Marabu (Alemania)", "Graficolor y otros; fuerte en gráfica, tampografía y digital", "Alto", "Baja: textil limitado (nylon, sintéticos)"],
    ["RUCO / RUCOINX (Alemania)", "Tampomex (distribuidor)", "Alto", "Baja: tintas industriales para plástico, vidrio y metal"],
    ["Tampoprint (Alemania)", "Filial en México; máquinas y tintas de tampografía", "Alto", "Baja: solo etiquetas sin costura (tagless)"],
    ["Marcas nacionales económicas: Dyssa, Celi Colors, Quitexa, De la Rana", "Menudeo, Mercado Libre, tiendas de serigrafía", "Muy bajo: galón de blanco plastisol ~MXN 790", "Media en talleres chicos"],
    ["Proveedores chinos directos (Alibaba)", "Venta en línea sin servicio local", "Muy bajo: silicona ~€3.5–5.2/kg", "Media: mismo origen que CLT"],
  ],
  inksNote: "Comex no fabrica tintas para serigrafía textil: es una marca de pinturas arquitectónicas. Precios públicos de octubre de 2026, solo como referencia; el precio de CLT para México está por confirmar.",
  swotTitle: "FODA por competidor",
  swotCols: ["Competidor", "Fortalezas", "Debilidades", "Oportunidad para CLT", "Amenaza para CLT"],
  swot: [
    ["Avient (Wilflex, Rutland)", "Marca global; tintas certificadas y aprobadas por marcas; gama completa", "Precio alto; importado; especialidades muy caras", "Siliconas y efectos especiales a menor precio; base agua", "Las marcas de exportación ya tienen tintas aprobadas: cambiar es lento"],
    ["Grupo Sánchez / ScreenTec", "Fabricante nacional; precio bajo; red de distribución; siliconas Siltex", "No vende máquinas ni línea híbrida; enfoque en mercado nacional", "Paquete llave en mano: máquina + química + servicio", "Guerra de precios en consumibles"],
    ["Matsui", "Referencia en base agua, descarga y especialidades", "Importado; precio medio-alto", "Las pastas base agua son el 54% de las ventas de CLT", "Ya está dentro de maquilas y talleres grandes"],
    ["Marabu, RUCO, Tampoprint", "Calidad alemana; fuertes en gráfica, tampografía e industria", "Poca oferta para estampado de prenda", "No compiten de frente en ropa", "Nicho de etiquetas sin costura y sintéticos"],
    ["Marcas económicas nacionales", "Precio muy bajo; disponibles en cualquier tienda", "Calidad variable; sin certificaciones ni soporte técnico", "Talleres que crecen y necesitan calidad constante", "Guerra de precios en talleres chicos"],
    ["Proveedores chinos directos", "Precio más bajo", "Sin servicio, sin inventario local, sin garantía", "Servicio local, inventario y técnicos en español", "Mismo origen: el cliente compara precio contra CLT"],
  ],
  ourTitle: "FODA de nuestra posición frente a la competencia (CLT + TID · VSP · CEB)",
  our: {
    F: ["Única oferta llave en mano: máquina híbrida + química + servicio", "Química CLT de menor precio que las marcas premium", "Servicio en México y EE. UU.; importación propia (CEB)"],
    D: ["Marca CLT poco conocida en México", "Sin aprobaciones de marcas de exportación todavía", "Equipo textil por formar"],
    O: ["Aranceles 2026 a China en prendas: más producción local", "OEM de exportación buscan efectos de alto valor", "Siliconas y efectos especiales con poca oferta local"],
    A: ["Avient atado a las listas de tintas aprobadas de las marcas", "Precio bajo de ScreenTec y de marcas económicas nacionales", "DTF en tirajes cortos", "Aranceles a insumos chinos"],
  },
  ourLabels: { F: "Fortalezas", D: "Debilidades", O: "Oportunidades", A: "Amenazas" },
  answer: "¿Son muy caras para competir? Las marcas premium (Avient, Matsui, Marabu, RUCO) cuestan más que la química china: ahí CLT compite por precio, pero debe ganar las aprobaciones de las marcas para entrar a la maquila. La competencia de precio real está en Grupo Sánchez / ScreenTec, las marcas económicas nacionales y los proveedores chinos directos; contra ellos el argumento es el paquete con máquina, servicio y soporte técnico.",
};

const en = {
  inksTitle: "Competitors in inks, pastes and silicones",
  inksCols: ["Brand (origin)", "Presence in Mexico", "Reference price", "Threat"],
  inks: [
    ["Avient: Wilflex, Rutland, Union Ink, Printop (U.S.)", "Casa Díaz and dealers; standard in export contract manufacturing", "High: ~US$40–60/gallon for mixing colors; specialties US$90–310/gallon (U.S. stores)", "High with OEMs"],
    ["Grupo Sánchez / ScreenTec: Seritex, Aquatex, Siltex (Mexico)", "Domestic manufacturer with a dealer network", "Low: MXN 159–217/kg retail (Seritex)", "High with shops"],
    ["Matsui (Japan)", "Casa Díaz; benchmark for water-based and discharge", "Mid-high; bases from ~US$8–9/kg in Central America", "Mid-high"],
    ["International Coatings (U.S.)", "Imported through U.S. dealers", "Mid", "Mid"],
    ["Marabu (Germany)", "Graficolor and others; strong in graphics, pad and digital printing", "High", "Low: limited textile range (nylon, synthetics)"],
    ["RUCO / RUCOINX (Germany)", "Tampomex (dealer)", "High", "Low: industrial inks for plastic, glass and metal"],
    ["Tampoprint (Germany)", "Mexican subsidiary; pad printing machines and inks", "High", "Low: tagless labels only"],
    ["Low-cost Mexican brands: Dyssa, Celi Colors, Quitexa, De la Rana", "Retail, Mercado Libre, screen printing stores", "Very low: plastisol white ~MXN 790/gallon", "Mid with small shops"],
    ["Direct Chinese suppliers (Alibaba)", "Online sales with no local service", "Very low: silicone ~€3.5–5.2/kg", "Mid: same origin as CLT"],
  ],
  inksNote: "Comex does not make textile screen printing inks: it is an architectural paint brand. Public prices as of October 2026, for reference only; CLT’s price for Mexico is to be confirmed.",
  swotTitle: "SWOT by competitor",
  swotCols: ["Competitor", "Strengths", "Weaknesses", "Opportunity for CLT", "Threat to CLT"],
  swot: [
    ["Avient (Wilflex, Rutland)", "Global brand; certified inks approved by brands; full range", "High price; imported; very expensive specialties", "Silicones and special effects at a lower price; water-based", "Export brands already have approved inks: switching is slow"],
    ["Grupo Sánchez / ScreenTec", "Domestic maker; low price; dealer network; Siltex silicones", "No machines or hybrid line; focus on the domestic market", "Turnkey package: machine + chemistry + service", "Price war in consumables"],
    ["Matsui", "Benchmark in water-based, discharge and specialties", "Imported; mid-high price", "Water-based pastes are 54% of CLT’s sales", "Already inside large contractors and shops"],
    ["Marabu, RUCO, Tampoprint", "German quality; strong in graphics, pad printing and industry", "Little offer for garment printing", "Not head-on competitors in apparel", "Tagless label and synthetics niche"],
    ["Low-cost Mexican brands", "Very low price; sold in every store", "Uneven quality; no certifications or technical support", "Growing shops that need consistent quality", "Price war in small shops"],
    ["Direct Chinese suppliers", "Lowest price", "No service, no local stock, no warranty", "Local service, stock and Spanish-speaking technicians", "Same origin: customers compare price against CLT"],
  ],
  ourTitle: "SWOT of our position against the competition (CLT + TID · VSP · CEB)",
  our: {
    F: ["Only turnkey offer: hybrid machine + chemistry + service", "CLT chemistry priced below premium brands", "Service in Mexico and the U.S.; own importer (CEB)"],
    D: ["CLT brand little known in Mexico", "No export-brand ink approvals yet", "Textile team still to be built"],
    O: ["2026 tariffs on Chinese apparel: more local production", "Export OEMs want high-value effects", "Few local suppliers of silicones and special effects"],
    A: ["Avient tied to brands’ approved-ink lists", "Low prices from ScreenTec and Mexican budget brands", "DTF in short runs", "Tariffs on Chinese inputs"],
  },
  ourLabels: { F: "Strengths", D: "Weaknesses", O: "Opportunities", A: "Threats" },
  answer: "Are they too expensive to compete? Premium brands (Avient, Matsui, Marabu, RUCO) cost more than Chinese chemistry: there CLT competes on price, but it must win brand approvals to get into contract manufacturing. The real price competition is Grupo Sánchez / ScreenTec, Mexican budget brands and direct Chinese suppliers; against them the argument is the package of machine, service and technical support.",
};

module.exports = { es, en };
