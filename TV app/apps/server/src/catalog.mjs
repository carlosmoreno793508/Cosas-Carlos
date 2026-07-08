import { readFileSync, existsSync } from "node:fs";

/**
 * Carga y normaliza el catálogo y los usuarios. Prefiere `catalog.json` /
 * `users.json` si existen; si no, cae a los `*.example.json` versionados.
 *
 * Todo el contenido lo defines TÚ en estos JSON. El servidor no descarga ni
 * incluye nada por su cuenta: solo sirve lo que pongas, para lo que tengas
 * derechos (contenido propio, TV abierta/FAST gratuita o material licenciado).
 */
function loadJson(dir, name) {
  const real = `${dir}/${name}.json`;
  const example = `${dir}/${name}.example.json`;
  const path = existsSync(real) ? real : example;
  return JSON.parse(readFileSync(path, "utf8"));
}

export function loadCatalog(dataDir) {
  const raw = loadJson(dataDir, "catalog");
  return {
    live: (raw.live ?? []).map((c, i) => ({
      id: String(c.id ?? i + 1),
      name: c.name ?? "Canal",
      logo: c.logo || "",
      category: c.category || "General",
      epgId: c.epgId || "",
      url: c.url,
    })),
    movies: (raw.movies ?? []).map((m, i) => ({
      id: String(m.id ?? i + 1),
      name: m.name ?? "Película",
      logo: m.logo || "",
      category: m.category || "General",
      rating: m.rating,
      year: m.year || "",
      ext: extOf(m.url),
      url: m.url,
    })),
    series: (raw.series ?? []).map((s, i) => ({
      id: String(s.id ?? i + 1),
      name: s.name ?? "Serie",
      cover: s.cover || "",
      category: s.category || "General",
      rating: s.rating,
      year: s.year || "",
      seasons: s.seasons ?? [],
    })),
  };
}

export function loadUsers(dataDir) {
  const raw = loadJson(dataDir, "users");
  return raw.users ?? [];
}

/** Extrae la extensión de una URL (mp4, mkv, m3u8…) para el contenedor VOD. */
export function extOf(url) {
  const m = /\.([a-z0-9]{2,5})(?:\?|$)/i.exec(url || "");
  return m ? m[1].toLowerCase() : "mp4";
}

/** Deriva un id de categoría estable a partir de su nombre. */
export function catId(name) {
  return name.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "general";
}

/** Lista de categorías únicas (con id) para un tipo dado del catálogo. */
export function categoriesOf(items) {
  const seen = new Map();
  for (const it of items) {
    if (!seen.has(it.category)) seen.set(it.category, catId(it.category));
  }
  return [...seen.entries()].map(([name, id]) => ({ id, name }));
}
