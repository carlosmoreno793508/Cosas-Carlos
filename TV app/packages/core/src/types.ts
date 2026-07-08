/**
 * Modelos de dominio compartidos por todas las plataformas (Fire TV, Roku,
 * Apple TV, Samsung/Tizen, LG/webOS, web y móvil).
 *
 * La idea central: la app cliente NO aloja contenido. Solo describe y reproduce
 * fuentes que el usuario aporta (lista M3U o credenciales Xtream Codes) o que
 * provienen de un proveedor con licencia. Estos tipos son el lenguaje común.
 */

/** Tipo de fuente que el usuario da de alta, tal como en la pantalla de la app. */
export type PlaylistKind = "m3u" | "xtream";

/** Categoría de reproducción de un stream. */
export type StreamType = "live" | "movie" | "series";

/** Una fuente de contenido registrada por el usuario (una "lista de reproducción"). */
export interface Playlist {
  id: string;
  kind: PlaylistKind;
  /** Nombre opcional que el usuario le pone (campo "Nombre (opcional)"). */
  name?: string;
  /**
   * Para `m3u`: URL directa al archivo .m3u/.m3u8.
   * Para `xtream`: URL base del portal (p. ej. https://miportal.com:8080).
   */
  url: string;
  /** Solo Xtream Codes. */
  username?: string;
  /** Solo Xtream Codes. */
  password?: string;
  /** Marca de tiempo (epoch ms) de creación. */
  createdAt: number;
}

/** Un canal / película / episodio reproducible, ya normalizado. */
export interface MediaItem {
  /** Identificador estable dentro de la playlist. */
  id: string;
  type: StreamType;
  title: string;
  /** URL final reproducible (HLS, TS, MP4, etc.). */
  streamUrl: string;
  /** Logo o póster. */
  logo?: string;
  /** Nombre de grupo/categoría (group-title en M3U, category en Xtream). */
  group?: string;
  /** Identificador EPG (tvg-id) para cruzar con la guía. */
  epgId?: string;
  /** Calificación 0–10 (para VOD), si la fuente la aporta. */
  rating?: number;
  /** Año de estreno (para VOD), si la fuente lo aporta. */
  year?: string;
  /** Fecha de alta (epoch en segundos) para ordenar "Recién agregado". */
  addedAt?: number;
  /** Metadatos libres extraídos de la fuente. */
  extra?: Record<string, string>;
}

/** Categoría agrupadora (canales por grupo, VOD por género, etc.). */
export interface Category {
  id: string;
  name: string;
  type: StreamType;
  /** Cantidad de items en la categoría (como muestra la barra lateral). */
  count?: number;
}

/** Programa de la guía electrónica (EPG). */
export interface EpgEntry {
  channelId: string;
  title: string;
  description?: string;
  /** Epoch ms. */
  start: number;
  /** Epoch ms. */
  stop: number;
}

/** Resultado normalizado de cargar una playlist, independiente de la fuente. */
export interface PlaylistContent {
  categories: Category[];
  items: MediaItem[];
}

/** Un episodio reproducible dentro de una temporada. */
export interface Episode {
  id: string;
  title: string;
  episodeNum?: number;
  streamUrl: string;
}

/** Una temporada con sus episodios. */
export interface SeriesSeason {
  season: number;
  episodes: Episode[];
}

/** Detalle de una serie: metadatos + temporadas/episodios reproducibles. */
export interface SeriesDetail {
  name?: string;
  cover?: string;
  plot?: string;
  seasons: SeriesSeason[];
}
