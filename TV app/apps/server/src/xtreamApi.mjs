import { catId, categoriesOf } from "./catalog.mjs";

/**
 * Construye las respuestas de la API Xtream Codes (player_api.php) a partir del
 * catálogo. Son funciones puras (fáciles de testear); el servidor HTTP solo las
 * envuelve. Los nombres de campos imitan a Xtream para que cualquier reproductor
 * compatible (incluida MoreTV) los entienda.
 */

export function userInfo(user, { host, port }) {
  return {
    user_info: {
      username: user.username,
      password: user.password,
      auth: 1,
      status: "Active",
      exp_date: user.expDate ? String(Math.floor(new Date(user.expDate).getTime() / 1000)) : null,
      is_trial: "0",
      active_cons: "0",
      max_connections: String(user.maxConnections ?? 1),
      allowed_output_formats: ["m3u8", "ts", "mp4"],
    },
    server_info: {
      url: host,
      port: String(port),
      https_port: String(port),
      server_protocol: "http",
      rtmp_port: "0",
      timezone: "UTC",
    },
  };
}

export function liveCategories(catalog) {
  return categoriesOf(catalog.live).map((c) => ({
    category_id: c.id,
    category_name: c.name,
    parent_id: 0,
  }));
}

export function vodCategories(catalog) {
  return categoriesOf(catalog.movies).map((c) => ({
    category_id: c.id,
    category_name: c.name,
    parent_id: 0,
  }));
}

export function seriesCategories(catalog) {
  return categoriesOf(catalog.series).map((c) => ({
    category_id: c.id,
    category_name: c.name,
    parent_id: 0,
  }));
}

export function liveStreams(catalog) {
  return catalog.live.map((c, i) => ({
    num: i + 1,
    name: c.name,
    stream_type: "live",
    stream_id: Number(c.id) || i + 1,
    stream_icon: c.logo,
    epg_channel_id: c.epgId,
    added: "0",
    category_id: catId(c.category),
    custom_sid: "",
    tv_archive: 0,
    direct_source: "",
    tv_archive_duration: 0,
  }));
}

export function vodStreams(catalog) {
  return catalog.movies.map((m, i) => ({
    num: i + 1,
    name: m.name,
    stream_type: "movie",
    stream_id: Number(m.id) || i + 1,
    stream_icon: m.logo,
    rating: m.rating != null ? String(m.rating) : "",
    rating_5based: m.rating != null ? m.rating / 2 : 0,
    added: "0",
    category_id: catId(m.category),
    container_extension: m.ext,
    custom_sid: "",
    direct_source: "",
    year: m.year,
  }));
}

export function seriesList(catalog) {
  return catalog.series.map((s, i) => ({
    num: i + 1,
    name: s.name,
    series_id: Number(s.id) || i + 1,
    cover: s.cover,
    plot: "",
    genre: s.category,
    releaseDate: s.year,
    rating: s.rating != null ? String(s.rating) : "",
    rating_5based: s.rating != null ? s.rating / 2 : 0,
    category_id: catId(s.category),
  }));
}

/** get_series_info: temporadas y episodios de una serie. */
export function seriesInfo(catalog, seriesId) {
  const s = catalog.series.find((x) => String(x.id) === String(seriesId));
  if (!s) return { info: {}, episodes: {} };
  const episodes = {};
  for (const season of s.seasons) {
    episodes[String(season.season)] = season.episodes.map((ep, i) => ({
      id: String(ep.id),
      episode_num: i + 1,
      title: ep.title,
      container_extension: extFromUrl(ep.url),
      info: {},
      season: season.season,
    }));
  }
  return {
    info: { name: s.name, cover: s.cover, genre: s.category, rating: s.rating },
    episodes,
  };
}

function extFromUrl(url) {
  const m = /\.([a-z0-9]{2,5})(?:\?|$)/i.exec(url || "");
  return m ? m[1].toLowerCase() : "mp4";
}

/** Resuelve la URL real de reproducción de un item por tipo e id. */
export function resolveStream(catalog, type, id) {
  if (type === "live") return catalog.live.find((c) => String(c.id) === String(id))?.url;
  if (type === "movie") return catalog.movies.find((m) => String(m.id) === String(id))?.url;
  if (type === "series") {
    for (const s of catalog.series) {
      for (const season of s.seasons) {
        const ep = season.episodes.find((e) => String(e.id) === String(id));
        if (ep) return ep.url;
      }
    }
  }
  return undefined;
}
