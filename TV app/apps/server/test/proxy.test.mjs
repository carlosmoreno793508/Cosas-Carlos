import { test } from "node:test";
import assert from "node:assert/strict";
import { isM3u8, rewriteM3u8, isValidTarget } from "../src/proxy.mjs";

test("isM3u8 detecta por extensión y content-type", () => {
  assert.equal(isM3u8("http://x/stream.m3u8", ""), true);
  assert.equal(isM3u8("http://x/seg", "application/vnd.apple.mpegurl"), true);
  assert.equal(isM3u8("http://x/seg.ts", "video/mp2t"), false);
});

test("isValidTarget solo acepta http/https", () => {
  assert.equal(isValidTarget("https://x/a.m3u8"), true);
  assert.equal(isValidTarget("file:///etc/passwd"), false);
  assert.equal(isValidTarget(""), false);
  assert.equal(isValidTarget(null), false);
});

test("rewriteM3u8 reescribe segmentos relativos y absolutos vía proxy", () => {
  const src = "https://cdn.example.com/live/stream.m3u8";
  const prefix = "http://localhost:8080/proxy?url=";
  const m3u = [
    "#EXTM3U",
    "#EXT-X-KEY:METHOD=AES-128,URI=\"key.bin\"",
    "#EXTINF:6,",
    "segment1.ts",
    "#EXTINF:6,",
    "https://otro.cdn.com/segment2.ts",
  ].join("\n");
  const out = rewriteM3u8(m3u, src, prefix);
  // Segmento relativo resuelto contra la base del origen
  assert.match(out, /proxy\?url=https%3A%2F%2Fcdn\.example\.com%2Flive%2Fsegment1\.ts/);
  // Segmento absoluto de otro CDN
  assert.match(out, /proxy\?url=https%3A%2F%2Fotro\.cdn\.com%2Fsegment2\.ts/);
  // Clave AES reescrita dentro de URI="..."
  assert.match(out, /URI="http:\/\/localhost:8080\/proxy\?url=https%3A%2F%2Fcdn\.example\.com%2Flive%2Fkey\.bin"/);
  // Los comentarios se conservan
  assert.match(out, /#EXTM3U/);
});
