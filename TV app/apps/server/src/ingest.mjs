// Importa contenido a tu catálogo desde una lista M3U (archivo o URL) y lo
// fusiona en data/catalog.json, deduplicando por URL y marcando la fecha de
// alta (para la sección "Recién agregado"). Opcionalmente recarga el servidor.
//
// Ejemplos:
//   node src/ingest.mjs --m3u ./mis-canales.m3u --section live
//   node src/ingest.mjs --m3u https://ejemplo/lista.m3u --section movies --reload
//   node src/ingest.mjs --m3u ./abierta.m3u --section live --category "TV Abierta"
//
// Pensado para TUS fuentes: contenido propio, TV abierta/FAST o material
// licenciado. No descarga video; solo guarda las URLs de los streams.

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const out = { section: "live" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--m3u") out.m3u = argv[++i];
    else if (a === "--section") out.section = argv[++i];
    else if (a === "--category") out.category = argv[++i];
    else if (a === "--out") out.out = argv[++i];
    else if (a === "--reload") out.reload = true;
    else if (a === "--reload-url") out.reloadUrl = argv[++i];
  }
  return out;
}

/** Parser M3U mínimo (id/nombre/logo/grupo/url). */
export function parseM3U(text) {
  const lines = text.split(/\r?\n/);
  const items = [];
  let pending = null;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line === "#EXTM3U") continue;
    if (line.startsWith("#EXTINF")) {
      const attrs = {};
      const re = /([a-zA-Z0-9_-]+)="([^"]*)"/g;
      let m;
      while ((m = re.exec(line)) !== null) attrs[m[1].toLowerCase()] = m[2];
      const comma = line.lastIndexOf(",");
      pending = {
        name: (comma === -1 ? "" : line.slice(comma + 1).trim()) || attrs["tvg-name"] || "Sin título",
        logo: attrs["tvg-logo"] || "",
        epgId: attrs["tvg-id"] || "",
        category: attrs["group-title"] || "General",
      };
    } else if (!line.startsWith("#")) {
      if (pending) {
        items.push({ ...pending, url: line });
        pending = null;
      }
    }
  }
  return items;
}

async function readSource(src) {
  if (/^https?:\/\//.test(src)) {
    const res = await fetch(src);
    if (!res.ok) throw new Error(`No se pudo descargar ${src} (${res.status})`);
    return res.text();
  }
  return readFileSync(resolve(src), "utf8");
}

/** Fusiona items nuevos en una sección del catálogo, deduplicando por URL. */
export function mergeIntoSection(catalog, section, incoming, { category, now }) {
  const list = catalog[section] ?? (catalog[section] = []);
  const existingUrls = new Set(list.map((x) => x.url));
  let maxId = list.reduce((max, x) => Math.max(max, Number(x.id) || 0), 0);
  let added = 0;

  for (const it of incoming) {
    if (!it.url || existingUrls.has(it.url)) continue;
    existingUrls.add(it.url);
    maxId += 1;
    const base = {
      id: String(maxId),
      name: it.name,
      category: category || it.category || "General",
      addedAt: now,
      url: it.url,
    };
    if (section === "series") {
      list.push({ ...base, cover: it.logo || "", seasons: [] });
    } else {
      list.push({ ...base, logo: it.logo || "", ...(it.epgId ? { epgId: it.epgId } : {}) });
    }
    added += 1;
  }
  return added;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.m3u) {
    console.error("Uso: node src/ingest.mjs --m3u <archivo-o-url> [--section live|movies|series] [--category NOMBRE] [--reload]");
    process.exit(1);
  }

  const dataDir = resolve(__dirname, "../data");
  const catalogPath = args.out ? resolve(args.out) : resolve(dataDir, "catalog.json");
  const catalog = existsSync(catalogPath)
    ? JSON.parse(readFileSync(catalogPath, "utf8"))
    : JSON.parse(readFileSync(resolve(dataDir, "catalog.example.json"), "utf8"));

  const text = await readSource(args.m3u);
  const items = parseM3U(text);
  const now = Math.floor(Date.now() / 1000);
  const added = mergeIntoSection(catalog, args.section, items, { category: args.category, now });

  writeFileSync(catalogPath, JSON.stringify(catalog, null, 2) + "\n");
  console.log(`✓ Importados ${added} items nuevos a "${args.section}" (${items.length} en la fuente).`);
  console.log(`  Catálogo: ${catalogPath}`);

  const reloadUrl = args.reloadUrl || (args.reload ? "http://localhost:8080/reload" : null);
  if (reloadUrl) {
    try {
      await fetch(reloadUrl);
      console.log(`✓ Servidor recargado (${reloadUrl}).`);
    } catch {
      console.warn(`⚠ No se pudo recargar el servidor en ${reloadUrl} (¿está corriendo?).`);
    }
  }
}

// Ejecuta solo si se llama directamente (no al importar en tests).
if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  main().catch((err) => {
    console.error(err.message);
    process.exit(1);
  });
}
