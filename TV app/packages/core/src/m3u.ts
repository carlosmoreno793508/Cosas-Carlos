import type { Category, MediaItem, PlaylistContent } from "./types.js";

/**
 * Parser de listas M3U / M3U8 extendidas (formato #EXTINF), que es el estándar
 * de facto para IPTV y el que exportan la mayoría de proveedores.
 *
 * Ejemplo de entrada:
 *   #EXTM3U
 *   #EXTINF:-1 tvg-id="cnn.us" tvg-logo="http://x/cnn.png" group-title="Noticias",CNN
 *   http://servidor/stream/cnn.m3u8
 *
 * No hace peticiones de red: recibe el texto crudo y devuelve el contenido
 * normalizado. Así es testeable y reutilizable en cualquier plataforma.
 */

/** Extrae los atributos `clave="valor"` de una línea #EXTINF. */
function parseAttributes(line: string): Record<string, string> {
  const attrs: Record<string, string> = {};
  const re = /([a-zA-Z0-9_-]+)="([^"]*)"/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(line)) !== null) {
    attrs[match[1].toLowerCase()] = match[2];
  }
  return attrs;
}

/** El título es lo que va después de la última coma de la línea #EXTINF. */
function parseTitle(line: string): string {
  const commaIndex = line.lastIndexOf(",");
  return commaIndex === -1 ? "" : line.slice(commaIndex + 1).trim();
}

/** Deriva un id estable de la categoría a partir de su nombre. */
function categoryId(name: string): string {
  return name.trim().toLowerCase().replace(/\s+/g, "-") || "sin-categoria";
}

export function parseM3U(text: string): PlaylistContent {
  const lines = text.split(/\r?\n/);
  const items: MediaItem[] = [];
  const categoriesByName = new Map<string, Category>();

  let pending: Partial<MediaItem> | null = null;
  let index = 0;

  for (const raw of lines) {
    const line = raw.trim();
    if (line === "" || line === "#EXTM3U") continue;

    if (line.startsWith("#EXTINF")) {
      const attrs = parseAttributes(line);
      const group = attrs["group-title"] || "General";
      pending = {
        title: parseTitle(line) || attrs["tvg-name"] || "Sin título",
        logo: attrs["tvg-logo"] || undefined,
        group,
        epgId: attrs["tvg-id"] || undefined,
        extra: attrs,
      };
      continue;
    }

    // Directivas VLC opcionales (audio, user-agent, etc.): las ignoramos aquí.
    if (line.startsWith("#")) continue;

    // Línea de URL: cierra el item pendiente.
    const group = pending?.group || "General";
    if (!categoriesByName.has(group)) {
      categoriesByName.set(group, {
        id: categoryId(group),
        name: group,
        type: "live",
      });
    }

    items.push({
      id: pending?.epgId || `m3u-${index}`,
      type: "live",
      title: pending?.title || "Sin título",
      streamUrl: line,
      logo: pending?.logo,
      group,
      epgId: pending?.epgId,
      extra: pending?.extra,
    });
    index++;
    pending = null;
  }

  return {
    categories: [...categoriesByName.values()],
    items,
  };
}
