/**
 * Punto de entrada del núcleo compartido de la TV app.
 *
 * Todo lo exportado aquí es lógica pura y sin dependencias de plataforma, para
 * poder reutilizarlo en Fire TV, Apple TV, Samsung/Tizen, LG/webOS, web y móvil.
 * (Roku usa BrightScript y reimplementa esta misma lógica; ver docs/PLATFORMS.md.)
 */
export * from "./types.js";
export { parseM3U } from "./m3u.js";
export { XtreamClient, fromPlaylist, withCounts } from "./xtream.js";
export type { XtreamConfig, FetchLike } from "./xtream.js";
export { FREE_SOURCES } from "./sources.js";
export type { FreeSource } from "./sources.js";
