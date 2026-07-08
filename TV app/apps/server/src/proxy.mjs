// Proxy de streams para el reproductor web. El navegador (Chrome) bloquea por
// CORS la lectura de listas M3U/Xtream y sus segmentos de terceros. Este proxy
// los pide desde el servidor (sin límite de CORS) y los reenvía con las
// cabeceras correctas, reescribiendo las playlists HLS para que sus segmentos
// también pasen por aquí.
//
// Es una herramienta neutral: reenvía exactamente lo que el usuario configure
// como su fuente (su propia suscripción/lista). No incluye ni provee contenido.

/** ¿La respuesta es una playlist HLS (.m3u8)? */
export function isM3u8(url, contentType) {
  if (contentType && /mpegurl|vnd\.apple\.mpegurl|x-mpegurl/i.test(contentType)) return true;
  return /\.m3u8($|\?)/i.test(url);
}

/**
 * Reescribe una playlist HLS para que las URLs de variantes, segmentos y claves
 * apunten de vuelta al proxy (resolviendo relativas contra la URL de origen).
 */
export function rewriteM3u8(text, sourceUrl, proxyPrefix) {
  const abs = (ref) => proxyPrefix + encodeURIComponent(new URL(ref, sourceUrl).toString());
  return text
    .split(/\r?\n/)
    .map((line) => {
      const t = line.trim();
      if (t === "") return line;
      if (t.startsWith("#")) {
        // Reescribe atributos URI="..." (p. ej. #EXT-X-KEY, #EXT-X-MEDIA).
        return line.replace(/URI="([^"]+)"/g, (_, u) => `URI="${abs(u)}"`);
      }
      // Línea de URL (variante o segmento).
      return abs(t);
    })
    .join("\n");
}

/** Valida que la URL destino sea http/https (evita file:, etc.). */
export function isValidTarget(target) {
  if (!target) return false;
  try {
    const u = new URL(target);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}
