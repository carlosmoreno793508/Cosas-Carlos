/**
 * Genera una guía XMLTV mínima a partir del catálogo. Como el catálogo no lleva
 * horarios, emitimos un bloque "en vivo" por canal para la franja actual, de
 * modo que MoreTV muestre algo en "ahora en pantalla". Si tienes horarios reales
 * puedes ampliar catalog.json y este generador para reflejarlos.
 */
function xmltvTime(ms) {
  const d = new Date(ms);
  const p = (n, w = 2) => String(n).padStart(w, "0");
  return (
    `${d.getUTCFullYear()}${p(d.getUTCMonth() + 1)}${p(d.getUTCDate())}` +
    `${p(d.getUTCHours())}${p(d.getUTCMinutes())}${p(d.getUTCSeconds())} +0000`
  );
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function buildXmltv(catalog, nowMs) {
  const startHour = Math.floor(nowMs / 3_600_000) * 3_600_000;
  const start = xmltvTime(startHour);
  const stop = xmltvTime(startHour + 2 * 3_600_000);

  const out = ['<?xml version="1.0" encoding="UTF-8"?>', "<tv>"];
  for (const c of catalog.live) {
    const id = c.epgId || `ch-${c.id}`;
    out.push(`  <channel id="${esc(id)}"><display-name>${esc(c.name)}</display-name></channel>`);
  }
  for (const c of catalog.live) {
    const id = c.epgId || `ch-${c.id}`;
    out.push(
      `  <programme start="${start}" stop="${stop}" channel="${esc(id)}">` +
        `<title>En vivo — ${esc(c.name)}</title></programme>`,
    );
  }
  out.push("</tv>");
  return out.join("\n") + "\n";
}
