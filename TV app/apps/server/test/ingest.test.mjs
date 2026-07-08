import { test } from "node:test";
import assert from "node:assert/strict";
import { parseM3U, mergeIntoSection } from "../src/ingest.mjs";

const SAMPLE = `#EXTM3U
#EXTINF:-1 tvg-id="a.mx" tvg-logo="http://x/a.png" group-title="Abierta",Canal A
http://s/a.m3u8
#EXTINF:-1 group-title="Abierta",Canal B
http://s/b.m3u8
`;

test("parseM3U extrae nombre, logo, grupo y url", () => {
  const items = parseM3U(SAMPLE);
  assert.equal(items.length, 2);
  assert.equal(items[0].name, "Canal A");
  assert.equal(items[0].logo, "http://x/a.png");
  assert.equal(items[0].epgId, "a.mx");
  assert.equal(items[0].url, "http://s/a.m3u8");
});

test("mergeIntoSection añade items nuevos con id incremental y addedAt", () => {
  const catalog = { live: [{ id: "5", name: "Prev", url: "http://s/prev.m3u8", category: "X" }] };
  const added = mergeIntoSection(catalog, "live", parseM3U(SAMPLE), { now: 1234 });
  assert.equal(added, 2);
  assert.equal(catalog.live.length, 3);
  assert.equal(catalog.live[1].id, "6");
  assert.equal(catalog.live[2].id, "7");
  assert.equal(catalog.live[1].addedAt, 1234);
});

test("mergeIntoSection deduplica por URL", () => {
  const catalog = { live: [{ id: "1", name: "A", url: "http://s/a.m3u8", category: "X" }] };
  const added = mergeIntoSection(catalog, "live", parseM3U(SAMPLE), { now: 1 });
  assert.equal(added, 1); // solo Canal B es nuevo
  assert.equal(catalog.live.length, 2);
});

test("mergeIntoSection respeta la categoría forzada", () => {
  const catalog = {};
  mergeIntoSection(catalog, "movies", parseM3U(SAMPLE), { now: 1, category: "Cine" });
  assert.equal(catalog.movies[0].category, "Cine");
});
