import { createServer } from "node:http";
import { Readable } from "node:stream";
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
import { buildXmltv } from "./epg.mjs";
import { isM3u8, rewriteM3u8, isValidTarget } from "./proxy.mjs";

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

/** Proxy: descarga la URL de terceros y la reenvía con CORS; reescribe HLS. */
async function handleProxy(url, req, res) {
  const target = url.searchParams.get("url");
  if (!isValidTarget(target)) {
    res.writeHead(400, { "content-type": "text/plain" });
    return res.end("Parámetro 'url' inválido");
  }
  try {
    const headers = {};
    if (req.headers.range) headers.range = req.headers.range;
    if (req.headers["user-agent"]) headers["user-agent"] = req.headers["user-agent"];
    const upstream = await fetch(target, { headers, redirect: "follow" });
    const ct = upstream.headers.get("content-type") || "";

    if (isM3u8(target, ct)) {
      const text = await upstream.text();
      const base = process.env.PUBLIC_URL || `http://${req.headers.host}`;
      const body = rewriteM3u8(text, upstream.url || target, `${base}/proxy?url=`);
      res.writeHead(200, {
        "content-type": "application/vnd.apple.mpegurl; charset=utf-8",
        "access-control-allow-origin": "*",
      });
      return res.end(body);
    }

    // Otros recursos (segmentos .ts, .mp4, claves): reenvío por streaming.
    const out = { "access-control-allow-origin": "*", "accept-ranges": "bytes" };
    for (const h of ["content-type", "content-length", "content-range", "cache-control"]) {
      const v = upstream.headers.get(h);
      if (v) out[h] = v;
    }
    res.writeHead(upstream.status, out);
    if (upstream.body) Readable.fromWeb(upstream.body).pipe(res);
    else res.end();
  } catch (err) {
    res.writeHead(502, { "content-type": "text/plain", "access-control-allow-origin": "*" });
    res.end("Proxy error: " + (err && err.message ? err.message : "desconocido"));
  }
}

export const server = createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  const path = url.pathname;

  // CORS: permite que la app web (otro origen) consuma la API del servidor.
  res.setHeader("access-control-allow-origin", "*");
  res.setHeader("access-control-allow-headers", "*");
  if (req.method === "OPTIONS") {
    res.writeHead(204);
    return res.end();
  }

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

  // Proxy de streams (para el reproductor web: salta la restricción CORS).
  if (path === "/proxy") {
    handleProxy(url, req, res);
    return;
  }

  // Guía de programación (XMLTV)
  if (path === "/xmltv.php") {
    const q = url.searchParams;
    if (!authenticate(q.get("username"), q.get("password"))) return notFound(res);
    res.writeHead(200, { "content-type": "application/xml; charset=utf-8" });
    return res.end(buildXmltv(catalog, Date.now()));
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
