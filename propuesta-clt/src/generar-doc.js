// Genera la propuesta en Word (ES y EN). Uso: node generar-doc.js <carpeta_salida>
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  ShadingType, HeadingLevel, AlignmentType, BorderStyle, LevelFormat, Footer,
  Header, PageNumber, PageBreak,
} = require("docx");
const content = require("./contenido-doc");

const INK = "1B1F3B";
const MAGENTA = "C2185B";
const CYAN = "0079A8";
const LIGHT = "EEF2F7";
const GRID = "C9D1DC";
const FONT = "Calibri";
const TABLE_W = 9360;

const border = { style: BorderStyle.SINGLE, size: 4, color: GRID };
const borders = { top: border, bottom: border, left: border, right: border };

function cell(text, width, opts = {}) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 80, bottom: 80, left: 110, right: 110 },
    children: [
      new Paragraph({
        keepNext: !!opts.keepNext,
        children: [new TextRun({ text, bold: !!opts.bold, color: opts.color, size: 19, font: FONT })],
      }),
    ],
  });
}

function table({ cols, rows, widths, bold }) {
  const header = new TableRow({
    tableHeader: true,
    cantSplit: true,
    children: cols.map((c, i) => cell(c, widths[i], { bold: true, fill: INK, color: "FFFFFF", keepNext: true })),
  });
  const body = rows.map((r, ri) => {
    const isTotal = bold && /^(Total|Resultado|Annual|Cumulative)/.test(r[0]);
    return new TableRow({
      cantSplit: true,
      children: r.map((t, i) =>
        cell(t, widths[i], { bold: isTotal || i === 0, fill: isTotal ? "FCE4EC" : ri % 2 ? LIGHT : undefined, keepNext: ri < rows.length - 1 })
      ),
    });
  });
  return new Table({ width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: widths, rows: [header, ...body] });
}

function build(lang) {
  const { meta, body } = content[lang];
  const children = [];

  // Portada
  children.push(
    new Paragraph({ spacing: { before: 2400 }, children: [new TextRun({ text: "CLT · TID · VSP · CEB", color: CYAN, bold: true, size: 24, font: FONT })] }),
    new Paragraph({ spacing: { before: 200 }, children: [new TextRun({ text: meta.title, color: INK, bold: true, size: 64, font: FONT })] }),
    new Paragraph({ spacing: { before: 120, after: 600 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: MAGENTA, space: 12 } }, children: [new TextRun({ text: meta.subtitle, color: MAGENTA, size: 30, font: FONT })] }),
    new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: meta.preparedFor, size: 24, font: FONT })] }),
    new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: meta.preparedBy, size: 24, font: FONT })] }),
    new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: meta.date, size: 24, font: FONT })] }),
    new Paragraph({ spacing: { before: 1800, after: 120 }, children: [new TextRun({ text: meta.contact, size: 20, color: "555555", font: FONT })] }),
    new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: meta.estimateNote, size: 18, italics: true, color: "555555", font: FONT })] }),
    new Paragraph({ children: [new TextRun({ text: meta.conf.toUpperCase(), size: 18, bold: true, color: MAGENTA, font: FONT })] }),
    new Paragraph({ children: [new PageBreak()] })
  );

  for (const b of body) {
    if (b.h1) children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(b.h1)] }));
    else if (b.h2) children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(b.h2)] }));
    else if (b.p) children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun(b.p)] }));
    else if (b.note) children.push(new Paragraph({ spacing: { before: 80, after: 200 }, children: [new TextRun({ text: b.note, italics: true, size: 18, color: "555555" })] }));
    else if (b.bullets) b.bullets.forEach((t) => children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 }, children: [new TextRun(t)] })));
    else if (b.table) {
      children.push(table(b.table));
      children.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    } else if (b.pagebreak) children.push(new Paragraph({ children: [new PageBreak()] }));
  }

  return new Document({
    creator: "TID México",
    title: meta.title,
    styles: {
      default: { document: { run: { font: FONT, size: 21 } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 32, bold: true, color: INK, font: FONT }, paragraph: { keepNext: true, keepLines: true, spacing: { before: 360, after: 160 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 25, bold: true, color: MAGENTA, font: FONT }, paragraph: { keepNext: true, keepLines: true, spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      ],
    },
    numbering: {
      config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }],
    },
    sections: [{
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, right: 1440, bottom: 1300, left: 1440 } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: meta.title, size: 16, color: "888888" })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: meta.footer + "   ·   ", size: 16, color: "888888" }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888" }),
      ] })] }) },
      children,
    }],
  });
}

(async () => {
  const out = process.argv[2] || ".";
  fs.mkdirSync(out, { recursive: true });
  for (const lang of ["es", "en"]) {
    const buf = await Packer.toBuffer(build(lang));
    const f = path.join(out, content[lang].meta.file + ".docx");
    fs.writeFileSync(f, buf);
    console.log("ok", f);
  }
})();
