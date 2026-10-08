// Base visual compartida de las presentaciones: tema, patrones, ayudas de diapositiva y transiciones.
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
const IMG = (f) => path.join(__dirname, "..", "img", f);

// CMYK: motivo visual (círculos de tinta)
const DOTS = ["0089C2", "C2185B", "F2B705", "1B1F3B"];

// Crea la presentación con sus patrones y devuelve las ayudas de diapositiva
function makeDeck(lang, t) {
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
  return { pres, C, content, section, stat, card, badge, note, dots };
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

module.exports = { THEME, HEX, DOTS, IMG, makeDeck, addTransitions };
