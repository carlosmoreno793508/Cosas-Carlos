// Diapositiva "Mercado en valor": impresión textil digital en México (Grand View Research). Se usa en la propuesta y en el estudio.
module.exports = function mercadoValor({ pres, content, stat, note, C, HEX }, es) {
  const s = content(es ? "Mercado en valor: impresión textil digital en México" : "Market value: digital textile printing in Mexico");
  s.addChart(pres.charts.BAR, [{ name: "US$ M", labels: ["2024", "2030 (proy.)".replace("proy.", es ? "proy." : "fcst.")], values: [116.5, 217.6] }], {
    x: 0.5, y: 1.05, w: 4.6, h: 3.7, barDir: "col", chartColors: ["0089C2", "C2185B"], showTitle: true,
    title: es ? "Millones de US$ · +11.5% anual" : "US$ millions · +11.5% a year", titleFontSize: 13, titleColor: HEX.dk1,
    catAxisLabelColor: HEX.dk2, catAxisLabelFontSize: 12, showValue: true, dataLabelPosition: "outEnd", dataLabelColor: HEX.dk1,
    dataLabelFontSize: 13, dataLabelFormatCode: "0.0", showLegend: false, valAxisHidden: true, valGridLine: { style: "none" },
  });
  const st = es
    ? [["74%", "directo a tela (rollo) en 2024"], ["DTG", "directo a prenda: el segmento que más crece"], ["~60%", "Epson en digital, según Epson"]]
    : [["74%", "direct to fabric (roll) in 2024"], ["DTG", "direct to garment: the fastest-growing segment"], ["~60%", "Epson in digital, per Epson"]];
  st.forEach(([b, l], i) => stat(s, 5.6, 1.15 + i * 1.2, 3.9, b, l, [C.accent1, C.accent2, C.accent1][i]));
  note(s, es
    ? "Fuente: Grand View Research (2024–2030); Epson en FESPA 2026. Solo impresión digital: no incluye la serigrafía ni la química que también vende CLT."
    : "Source: Grand View Research (2024–2030); Epson at FESPA 2026. Digital printing only: excludes the screen printing and chemistry CLT also sells.");
  return s;
};
