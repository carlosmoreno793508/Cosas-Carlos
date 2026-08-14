import { test } from "node:test";
import assert from "node:assert/strict";
import { buildXmltv } from "../src/epg.mjs";

const catalog = {
  live: [
    { id: "1", name: "Canal & Uno", epgId: "uno.mx" },
    { id: "2", name: "Canal Dos", epgId: "" },
  ],
};

test("buildXmltv emite canales y programas escapados", () => {
  const xml = buildXmltv(catalog, Date.UTC(2026, 6, 8, 20, 30, 0));
  assert.match(xml, /<channel id="uno.mx">/);
  assert.match(xml, /Canal &amp; Uno/); // escape de &
  assert.match(xml, /channel="ch-2"/); // fallback de epgId
  assert.match(xml, /<programme start="20260708200000 \+0000"/); // franja alineada a la hora
});
