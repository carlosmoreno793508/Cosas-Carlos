import type { EpgEntry } from "./types.js";

/**
 * Guía de programación (EPG). Los proveedores de IPTV y las listas de TV abierta
 * publican la guía en formato **XMLTV** (por ejemplo iptv-org/epg, o el endpoint
 * `xmltv.php` de un portal Xtream). Aquí la parseamos sin dependencias y damos un
 * helper "ahora / después" por canal.
 */

/** Convierte una marca XMLTV ("20260708200000 +0000") a epoch ms. */
export function parseXmltvTime(value: string): number {
  const m = /^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(?:\s*([+-]\d{4}))?/.exec(value.trim());
  if (!m) return NaN;
  const [, y, mo, d, h, mi, s, tz] = m;
  const iso = `${y}-${mo}-${d}T${h}:${mi}:${s}${formatTz(tz)}`;
  return new Date(iso).getTime();
}

function formatTz(tz?: string): string {
  if (!tz) return "Z";
  return `${tz.slice(0, 3)}:${tz.slice(3)}`; // +0000 -> +00:00
}

function decodeEntities(s: string): string {
  return s
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, code) => String.fromCodePoint(parseInt(code, 16)))
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&");
}

/**
 * Parsea un documento XMLTV a una lista de programas. Usa expresiones regulares
 * (no un parser XML completo) porque XMLTV es plano y regular; suficiente para
 * título, tiempos y canal, que es lo que muestra la guía.
 */
export function parseXmltv(xml: string): EpgEntry[] {
  const entries: EpgEntry[] = [];
  const re = /<programme\b([^>]*)>([\s\S]*?)<\/programme>/g;
  let match: RegExpExecArray | null;

  while ((match = re.exec(xml)) !== null) {
    const attrs = match[1];
    const body = match[2];
    const channel = attr(attrs, "channel");
    const start = parseXmltvTime(attr(attrs, "start"));
    const stop = parseXmltvTime(attr(attrs, "stop"));
    if (!channel || Number.isNaN(start)) continue;

    const title = tag(body, "title");
    const desc = tag(body, "desc");
    entries.push({
      channelId: channel,
      title: title ? decodeEntities(title) : "(sin título)",
      description: desc ? decodeEntities(desc) : undefined,
      start,
      stop: Number.isNaN(stop) ? start : stop,
    });
  }
  return entries;
}

function attr(attrs: string, name: string): string {
  const m = new RegExp(`${name}="([^"]*)"`).exec(attrs);
  return m ? m[1] : "";
}

function tag(body: string, name: string): string {
  const m = new RegExp(`<${name}\\b[^>]*>([\\s\\S]*?)</${name}>`).exec(body);
  return m ? m[1].trim() : "";
}

/** Agrupa los programas por canal (channelId → programas ordenados por inicio). */
export function groupEpgByChannel(entries: EpgEntry[]): Map<string, EpgEntry[]> {
  const map = new Map<string, EpgEntry[]>();
  for (const e of entries) {
    const list = map.get(e.channelId);
    if (list) list.push(e);
    else map.set(e.channelId, [e]);
  }
  for (const list of map.values()) list.sort((a, b) => a.start - b.start);
  return map;
}

/** Programa actual y siguiente de un canal en el instante `nowMs`. */
export function nowNext(
  entries: EpgEntry[],
  nowMs: number,
): { now?: EpgEntry; next?: EpgEntry } {
  const sorted = [...entries].sort((a, b) => a.start - b.start);
  let now: EpgEntry | undefined;
  let next: EpgEntry | undefined;
  for (const e of sorted) {
    if (e.start <= nowMs && nowMs < e.stop) now = e;
    else if (e.start > nowMs) {
      next = e;
      break;
    }
  }
  return { now, next };
}
