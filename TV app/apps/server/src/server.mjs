import { createServer } from "node:http";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { loadCatalog, loadUsers } from "./catalog.mjs";
import {
  userInfo,
  liveCategories,
  vodCategories,
  seriesCategories,
  liveStreams,
  vodStreams,
  seriesList,
  seriesInfo,
  resolveStream,
} from "./xtreamApi.mjs";
import { buildM3U } from "./m3u.mjs";

/**
 * Servidor propio compatible con Xtream Codes + exportación M3U. MoreTV (u otro
 * reproductor) se conecta con URL + usuario + contraseña y ve tu catálogo. El
 * servidor no aloja video: guarda las URLs de tus streams y redirige a ellas.
 *
 * Config por variables de entorno:
 *   PORT       (por defecto 8080)
 *   DATA_DIR   (por defecto ../data)
 *   PUBLIC_URL (URL pública p. ej. http://mi-ip:8080; por defecto se infiere)
 */
const __dirname = dirname(fileURLToPath(import.meta.url));
const PORT = Number(process.env.PORT || 8080);
const DATA_DIR = process.env.DATA_DIR || resolve(__dirname, "../data");

let catalog = loadCatalog(DATA_DIR);
let users = loadUsers(DATA_DIR);

/** Relee catálogo y usuarios en caliente (para actualizar sin reiniciar). */
export function reload() {
  catalog = loadCatalog(DATA_DIR);
  users = loadUsers(DATA_DIR);
}

function authenticate(u, p) {
  return users.find((x) => x.username === u && String(x.password) === String(p));
}

function json(res, body) {
  const payload = JSON.stringify(body);
  res.writeHead(200, { "content-type": "application/json; charset=utf-8" });
  res.end(payload);
}

function notFound(res) {
  res.writeHead(404, { "content-type": "text/plain" });
  res.end("Not found");
}

function handlePlayerApi(url, res) {
  const q = url.searchParams;
  const user = authenticate(q.get("username"), q.get("password"));
  if (!user) return json(res, { user_info: { auth: 0 } });

  const action = q.get("action");
  const host = process.env.PUBLIC_URL || `localhost:${PORT}`;

  switch (action) {
    case null:
    case "":
      return json(res, userInfo(user, { host, port: PORT }));
    case "get_live_categories":
      return json(res, liveCategories(catalog));
    case "get_vod_categories":
      return json(res, vodCategories(catalog));
    case "get_series_categories":
      return json(res, seriesCategories(catalog));
    case "get_live_streams":
      return json(res, liveStreams(catalog));
    case "get_vod_streams":
      return json(res, vodStreams(catalog));
    case "get_series":
      return json(res, seriesList(catalog));
    case "get_series_info":
      return json(res, seriesInfo(catalog, q.get("series_id")));
    case "get_short_epg":
    case "get_simple_data_table":
      return json(res, { epg_listings: [] });
    default:
      return json(res, []);
  }
}

/** /live|movie|series/{user}/{pass}/{id}.{ext} → redirige al stream real. */
function handlePlayback(pathname, res) {
  const parts = pathname.split("/").filter(Boolean); // [type, user, pass, id.ext]
  if (parts.length !== 4) return notFound(res);
  const [type, u, p, file] = parts;
  if (!authenticate(u, p)) return notFound(res);
  const id = file.replace(/\.[a-z0-9]+$/i, "");
  const target = resolveStream(catalog, type, id);
  if (!target) return notFound(res);
  res.writeHead(302, { location: target });
  res.end();
}

export const server = createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  const path = url.pathname;

  // Salud / diagnóstico
  if (path === "/" || path === "/health") {
    return json(res, {
      ok: true,
      live: catalog.live.length,
      movies: catalog.movies.length,
      series: catalog.series.length,
    });
  }

  // Recarga de catálogo en caliente
  if (path === "/reload") {
    reload();
    return json(res, { reloaded: true });
  }

  // API Xtream
  if (path === "/player_api.php") return handlePlayerApi(url, res);

  // Exportación M3U (modo M3U de los reproductores)
  if (path === "/get.php") {
    const q = url.searchParams;
    if (!authenticate(q.get("username"), q.get("password"))) return notFound(res);
    const base = process.env.PUBLIC_URL || `http://${req.headers.host}`;
    const m3u = buildM3U(catalog, {
      base,
      username: q.get("username"),
      password: q.get("password"),
    });
    res.writeHead(200, { "content-type": "application/vnd.apple.mpegurl; charset=utf-8" });
    return res.end(m3u);
  }

  // Reproducción
  if (/^\/(live|movie|series)\//.test(path)) return handlePlayback(path, res);

  return notFound(res);
});

// Arranca solo si se ejecuta directamente (no al importarlo en tests).
if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  server.listen(PORT, () => {
    console.log(`MoreTV server escuchando en http://localhost:${PORT}`);
    console.log(`  Xtream:  http://localhost:${PORT}  (usuario/contraseña de data/users.json)`);
    console.log(`  M3U:     http://localhost:${PORT}/get.php?username=U&password=P&type=m3u_plus`);
    console.log(`  Catálogo: ${catalog.live.length} canales · ${catalog.movies.length} pelis · ${catalog.series.length} series`);
  });
}
