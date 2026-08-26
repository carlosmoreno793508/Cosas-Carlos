import { test } from "node:test";
import assert from "node:assert/strict";
import { parseM3U } from "../src/m3u.ts";

const SAMPLE = `#EXTM3U
#EXTINF:-1 tvg-id="cnn.us" tvg-logo="http://x/cnn.png" group-title="Noticias",CNN
http://servidor/live/cnn.m3u8
#EXTINF:-1 tvg-id="espn.us" tvg-logo="http://x/espn.png" group-title="Deportes",ESPN
http://servidor/live/espn.m3u8
#EXTINF:-1 group-title="Deportes",Fox Sports
http://servidor/live/fox.ts
`;

test("parsea items con atributos y URL", () => {
  const { items } = parseM3U(SAMPLE);
  assert.equal(items.length, 3);
  assert.equal(items[0].title, "CNN");
  assert.equal(items[0].streamUrl, "http://servidor/live/cnn.m3u8");
  assert.equal(items[0].logo, "http://x/cnn.png");
  assert.equal(items[0].epgId, "cnn.us");
  assert.equal(items[0].group, "Noticias");
});

test("agrupa categorías sin duplicar", () => {
  const { categories } = parseM3U(SAMPLE);
  const names = categories.map((c) => c.name).sort();
  assert.deepEqual(names, ["Deportes", "Noticias"]);
});

test("usa 'General' cuando falta group-title", () => {
  const { items, categories } = parseM3U(
    `#EXTM3U\n#EXTINF:-1,Canal X\nhttp://x/x.m3u8\n`,
  );
  assert.equal(items[0].group, "General");
  assert.equal(categories[0].name, "General");
});

test("ignora líneas vacías y directivas #EXTM3U", () => {
  const { items } = parseM3U(`#EXTM3U\n\n\n#EXTINF:-1,Solo\nhttp://x/s.m3u8\n\n`);
  assert.equal(items.length, 1);
  assert.equal(items[0].title, "Solo");
});

test("cae a tvg-name cuando no hay título tras la coma", () => {
  const { items } = parseM3U(
    `#EXTM3U\n#EXTINF:-1 tvg-name="Respaldo",\nhttp://x/r.m3u8\n`,
  );
  assert.equal(items[0].title, "Respaldo");
});
