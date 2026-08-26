/**
 * Genera una lista M3U extendida a partir del catálogo, para reproductores en
 * modo "M3U" (o para descargar con get.php?type=m3u_plus). Las URLs apuntan de
 * vuelta al propio servidor, que redirige al stream real.
 */
export function buildM3U(catalog, { base, username, password }) {
  const lines = ["#EXTM3U"];

  const push = (item, type, id, ext) => {
    const attrs = [
      item.epgId ? `tvg-id="${item.epgId}"` : "",
      item.logo ? `tvg-logo="${item.logo}"` : "",
      `group-title="${item.category}"`,
    ]
      .filter(Boolean)
      .join(" ");
    lines.push(`#EXTINF:-1 ${attrs},${item.name}`);
    lines.push(`${base}/${type}/${username}/${password}/${id}.${ext}`);
  };

  for (const c of catalog.live) push(c, "live", c.id, "m3u8");
  for (const m of catalog.movies) push(m, "movie", m.id, m.ext);
  for (const s of catalog.series) {
    for (const season of s.seasons) {
      for (const ep of season.episodes) {
        push(
          { ...s, name: `${s.name} S${season.season} - ${ep.title}` },
          "series",
          ep.id,
          extFromUrl(ep.url),
        );
      }
    }
  }

  return lines.join("\n") + "\n";
}

function extFromUrl(url) {
  const m = /\.([a-z0-9]{2,5})(?:\?|$)/i.exec(url || "");
  return m ? m[1].toLowerCase() : "mp4";
}
