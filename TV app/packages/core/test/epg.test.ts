import { test } from "node:test";
import assert from "node:assert/strict";
import { parseXmltv, parseXmltvTime, groupEpgByChannel, nowNext } from "../src/epg.ts";

const XML = `<?xml version="1.0"?>
<tv>
  <channel id="canal1.mx"><display-name>Canal 1</display-name></channel>
  <programme start="20260708200000 +0000" stop="20260708210000 +0000" channel="canal1.mx">
    <title>Noticias de la Noche</title>
    <desc>Resumen del d&#237;a</desc>
  </programme>
  <programme start="20260708210000 +0000" stop="20260708220000 +0000" channel="canal1.mx">
    <title>Pel&#237;cula</title>
  </programme>
</tv>`;

test("parseXmltvTime interpreta fecha y zona horaria", () => {
  const t = parseXmltvTime("20260708200000 +0000");
  assert.equal(new Date(t).toISOString(), "2026-07-08T20:00:00.000Z");
});

test("parseXmltv extrae título, descripción y tiempos", () => {
  const entries = parseXmltv(XML);
  assert.equal(entries.length, 2);
  assert.equal(entries[0].channelId, "canal1.mx");
  assert.equal(entries[0].title, "Noticias de la Noche");
  assert.equal(entries[0].description, "Resumen del día");
  assert.equal(entries[1].title, "Película");
});

test("groupEpgByChannel agrupa y ordena", () => {
  const map = groupEpgByChannel(parseXmltv(XML));
  assert.equal(map.get("canal1.mx")?.length, 2);
});

test("nowNext identifica el programa actual y el siguiente", () => {
  const entries = parseXmltv(XML);
  const at = Date.parse("2026-07-08T20:30:00Z");
  const { now, next } = nowNext(entries, at);
  assert.equal(now?.title, "Noticias de la Noche");
  assert.equal(next?.title, "Película");
});

test("nowNext sin programa en curso solo devuelve el siguiente", () => {
  const entries = parseXmltv(XML);
  const at = Date.parse("2026-07-08T19:00:00Z");
  const { now, next } = nowNext(entries, at);
  assert.equal(now, undefined);
  assert.equal(next?.title, "Noticias de la Noche");
});
