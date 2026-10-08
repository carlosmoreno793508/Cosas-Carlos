// Cuentas prioritarias (regla 80/20) para la propuesta. Fuente: src/prospectos.json (incluye Baja California).
// Cada fila: [empresa, ciudad, giro ES, giro EN, segmento/clientes ES, segmento/clientes EN]
module.exports = {
  prospects: [
    ["ADN Serigrafía", "Naucalpan, Edo. Méx.", "Maquila de serigrafía: 130,000+ piezas/semana, hasta 18 tintas, producción para EE. UU. y Canadá", "Contract screen printing: 130,000+ pcs/week, up to 18 colors, production for the U.S. and Canada", "Estampado y serigrafía", "Printing and screen printing"],
    ["Serigrafía Textil Automatizada (KW)", "Puebla, Pue.", "Serigrafía automatizada por volumen: campañas, deportivo y promocional; 30+ años", "Automated volume screen printing: campaigns, sportswear and promo; 30+ years", "Estampado y serigrafía", "Printing and screen printing"],
    ["Manufacturas Textiles RF (Reitex)", "Guadalupe, N.L.", "Fábrica integrada de hilo a prenda; playeras de campaña y publicitarias de alto volumen", "Integrated yarn-to-garment plant; high-volume campaign and promo T-shirts", "Promocionales", "Promotional"],
    ["Diermi (Playeras Mindy)", "Zapopan, Jal.", "Playeras deportivas y publicitarias en nave automatizada de 5,000 m²; exporta a EE. UU.", "Sports and promo T-shirts in a 5,000 m² automated plant; exports to the U.S.", "Ropa deportiva", "Sportswear"],
    ["GOCA'S", "Ciudad de México", "Playeras y sudaderas a gran escala con serigrafía, sublimación y bordado propios; 25+ años", "Large-scale T-shirts and hoodies with in-house screen, sublimation and embroidery; 25+ years", "Promocionales", "Promotional"],
    ["SerigrafiarteSP", "Ciudad de México", "Maquila de serigrafía (plastisol, base agua, corrosión), DTF y sublimación para fábricas y marcas", "Contract screen printing (plastisol, water-based, discharge), DTF and sublimation for factories and brands", "Estampado y serigrafía", "Printing and screen printing"],
    ["Grupo Martex", "Naucalpan, Edo. Méx.", "Fabricante textil de gran volumen; uniformes (el directorio menciona uniformes FIFA)", "High-volume textile maker; uniforms (directory cites FIFA uniforms)", "Uniformes y deportivo", "Uniforms and sportswear"],
    ["Uniformes Carmen", "Guadalajara, Jal.", "Uniformes con serigrafía, bordado y transfer; maquila de estampado por volumen; 30+ años", "Uniforms with screen, embroidery and transfer; volume print contracting; 30+ years", "Uniformes", "Uniforms"],
    ["Charly (Grupo Charly)", "León, Gto.", "Marca deportiva: jerseys y licencias de clubes de Liga MX (León, Pachuca, Atlas, Santos)", "Sports brand: jerseys and licensed apparel for Liga MX clubs (León, Pachuca, Atlas, Santos)", "Ropa deportiva / licencias", "Sportswear / licensing"],
  ],
  oems: [
    ["Vertical Knits", "Baca, Yuc.", "Tejido de punto con serigrafía y bordado internos; 16–25 millones de prendas al año", "Knitwear with in-house screen printing and embroidery; 16–25 million garments a year", "Nike, Fanatics, Tommy Hilfiger, Patagonia", "Nike, Fanatics, Tommy Hilfiger, Patagonia"],
    ["Ink Throwers de México", "Tijuana, B.C.", "Serigrafía por contrato para retail y licencias: ~50,000 impresiones/día, ~538 trabajadores", "Contract screen printing for retail and licensing: ~50,000 prints/day, ~538 workers", "Disney, Levi's, Marvel", "Disney, Levi's, Marvel"],
    ["MD International Baja", "Ensenada, B.C.", "Estampado masivo y confección; 1,200–1,300 trabajadores", "Mass printing and sewing; 1,200–1,300 workers", "Fanatics, Hurley, REI", "Fanatics, Hurley, REI"],
    ["Fortune Fashions Baja (Mad Engine)", "Ensenada, B.C.", "Planta de serigrafía de playeras licenciadas para retail de EE. UU.", "Screen printing plant for licensed T-shirts for U.S. retail", "Mad Engine Global, Disney", "Mad Engine Global, Disney"],
    ["SOIR Textiles (TJ Factory Clothing)", "Ensenada, B.C.", "Estampado de prendas, serigrafía plana y teñido en dos plantas", "Garment printing, flatbed screen printing and dyeing in two plants", "Columbia, Disney", "Columbia, Disney"],
    ["Factory 1 (Factory1 Group)", "Ensenada, B.C.", "Paquete completo con serigrafía plana, teñido y lavado; 702 trabajadores", "Full package with flatbed screen printing, dyeing and washing; 702 workers", "Columbia, Disney", "Columbia, Disney"],
    ["Codipsa (San Fernando ScreenPrinting)", "Puebla, Pue.", "Punto vertical (tejido, teñido, acabado y estampado) para fast fashion; 35+ años exportando", "Vertical knit (knitting, dyeing, finishing, printing) for fast fashion; 35+ years exporting", "Puma, Gap, Hot Topic, Macy's, Disney", "Puma, Gap, Hot Topic, Macy's, Disney"],
    ["RMC de México", "Linares, N.L.", "Planta vertical con estampado, sublimación, bordado, corte y costura; 336 trabajadores", "Vertical plant with printing, sublimation, embroidery, cut and sew; 336 workers", "Under Armour, Nordstrom", "Under Armour, Nordstrom"],
  ],
  next: {
    es: "Siguiente nivel (OEM): Grumax / BEX Bordados y Estampados (Xalapa), California Cutting & Sewing (Puebla), Confecciones Clabeck / JHK (Tlalnepantla; auditada por Inditex y C&A), Private Label Tehuacán (PVH, J.Crew, L.L.Bean), Industrias Manufactureras MYR (adidas, Puma; jerseys de la Selección Mexicana), Augusta Sportswear de México (Fanatics), Zentrix (Nike, Lululemon) y Baja Skiva Screen Printing (Disney).",
    en: "Next tier (OEM): Grumax / BEX Bordados y Estampados (Xalapa), California Cutting & Sewing (Puebla), Confecciones Clabeck / JHK (Tlalnepantla; audited by Inditex and C&A), Private Label Tehuacán (PVH, J.Crew, L.L.Bean), Industrias Manufactureras MYR (adidas, Puma; Mexico national team jerseys), Augusta Sportswear de México (Fanatics), Zentrix (Nike, Lululemon) and Baja Skiva Screen Printing (Disney).",
  },
};
