import { test } from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { loadCatalog } from "../src/catalog.mjs";
import {
  liveCategories,
  liveStreams,
  vodStreams,
  seriesInfo,
  resolveStream,
} from "../src/xtreamApi.mjs";
import { buildM3U } from "../src/m3u.mjs";

const DATA = resolve(dirname(fileURLToPath(import.meta.url)), "../data");
const catalog = loadCatalog(DATA);

test("carga el catálogo de ejemplo", () => {
  assert.ok(catalog.live.length >= 1);
  assert.ok(catalog.movies.length >= 1);
  assert.ok(catalog.series.length >= 1);
});

test("live categories son únicas con id derivado", () => {
  const cats = liveCategories(catalog);
  const names = cats.map((c) => c.category_name);
  assert.ok(names.includes("TV Abierta"));
  assert.equal(new Set(cats.map((c) => c.category_id)).size, cats.length);
});

test("live streams incluyen icon, epg y category_id", () => {
  const s = liveStreams(catalog)[0];
  assert.equal(s.stream_type, "live");
  assert.equal(typeof s.stream_id, "number");
  assert.equal(s.category_id, "tv-abierta");
  assert.equal(s.epg_channel_id, "canal1.mx");
});

test("vod streams convierten rating a rating_5based", () => {
  const m = vodStreams(catalog).find((x) => x.name.startsWith("Big Buck"));
  assert.equal(m.rating_5based, 8.1 / 2);
  assert.equal(m.container_extension, "mp4");
});

test("seriesInfo devuelve temporadas y episodios", () => {
  const info = seriesInfo(catalog, "301");
  assert.ok(info.episodes["1"]);
  assert.equal(info.episodes["1"][0].id, "3011");
});

test("resolveStream encuentra la URL real por tipo e id", () => {
  assert.match(resolveStream(catalog, "live", "101"), /^https?:\/\//);
  assert.match(resolveStream(catalog, "movie", "201"), /\.mp4/);
  assert.match(resolveStream(catalog, "series", "3011"), /^https?:\/\//);
  assert.equal(resolveStream(catalog, "movie", "999"), undefined);
});

test("buildM3U genera cabecera y URLs hacia el servidor", () => {
  const m3u = buildM3U(catalog, { base: "http://host:8080", username: "u", password: "p" });
  assert.ok(m3u.startsWith("#EXTM3U"));
  assert.match(m3u, /http:\/\/host:8080\/live\/u\/p\/101\.m3u8/);
  assert.match(m3u, /group-title="TV Abierta"/);
});
