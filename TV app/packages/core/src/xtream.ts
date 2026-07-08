import type {
  Category,
  EpgEntry,
  MediaItem,
  Playlist,
  PlaylistContent,
  SeriesDetail,
  SeriesSeason,
  StreamType,
} from "./types.js";

/**
 * Cliente para la API "Xtream Codes", que es el protocolo que usan la mayoría
 * de portales IPTV (el modo "Xtream" de la pantalla de alta: URL + usuario +
 * contraseña). La app cliente habla este protocolo estándar; el contenido lo
 * aporta el servidor del proveedor.
 *
 * Endpoints estándar (todos sobre `player_api.php`):
 *   .../player_api.php?username=U&password=P&action=get_live_categories
 *   .../player_api.php?username=U&password=P&action=get_live_streams
 *   .../player_api.php?username=U&password=P&action=get_vod_streams
 *   .../player_api.php?username=U&password=P&action=get_series
 *
 * URL de reproducción resultante:
 *   live:   {base}/live/{user}/{pass}/{stream_id}.m3u8
 *   movie:  {base}/movie/{user}/{pass}/{stream_id}.{ext}
 *   series: {base}/series/{user}/{pass}/{episode_id}.{ext}
 */

export interface XtreamConfig {
  /** URL base del portal, sin barra final. Ej: https://portal.com:8080 */
  baseUrl: string;
  username: string;
  password: string;
}

/** Permite inyectar fetch en tests / plataformas sin fetch global. */
export type FetchLike = (
  url: string,
  init?: { signal?: AbortSignal },
) => Promise<{ ok: boolean; status: number; json(): Promise<unknown>; text(): Promise<string> }>;

function trimSlash(url: string): string {
  return url.replace(/\/+$/, "");
}

export function fromPlaylist(p: Playlist): XtreamConfig {
  if (p.kind !== "xtream") throw new Error("La playlist no es de tipo Xtream");
  if (!p.username || !p.password) throw new Error("Faltan credenciales Xtream");
  return { baseUrl: p.url, username: p.username, password: p.password };
}

export class XtreamClient {
  private readonly base: string;
  private readonly user: string;
  private readonly pass: string;
  private readonly fetchFn: FetchLike;

  constructor(config: XtreamConfig, fetchFn?: FetchLike) {
    this.base = trimSlash(config.baseUrl);
    this.user = config.username;
    this.pass = config.password;
    // globalThis.fetch existe en navegadores, Node 18+, Tizen y webOS modernos.
    this.fetchFn = fetchFn ?? (globalThis.fetch as unknown as FetchLike);
    if (!this.fetchFn) {
      throw new Error("No hay implementación de fetch disponible en esta plataforma");
    }
  }

  private api(action: string, params: Record<string, string> = {}): string {
    const q = new URLSearchParams({
      username: this.user,
      password: this.pass,
      action,
      ...params,
    });
    return `${this.base}/player_api.php?${q.toString()}`;
  }

  private async getJson<T>(url: string, signal?: AbortSignal): Promise<T> {
    const res = await this.fetchFn(url, { signal });
    if (!res.ok) {
      throw new Error(`Xtream respondió ${res.status} en ${url}`);
    }
    return (await res.json()) as T;
  }

  /** URL de reproducción para un item según su tipo. */
  buildStreamUrl(type: StreamType, streamId: string | number, ext = "m3u8"): string {
    const segment = type === "live" ? "live" : type === "movie" ? "movie" : "series";
    return `${this.base}/${segment}/${this.user}/${this.pass}/${streamId}.${ext}`;
  }

  async getCategories(type: StreamType, signal?: AbortSignal): Promise<Category[]> {
    const action =
      type === "live"
        ? "get_live_categories"
        : type === "movie"
          ? "get_vod_categories"
          : "get_series_categories";
    const raw = await this.getJson<Array<{ category_id: string; category_name: string }>>(
      this.api(action),
      signal,
    );
    return raw.map((c) => ({
      id: String(c.category_id),
      name: c.category_name,
      type,
    }));
  }

  /** Descarga los streams en vivo y los normaliza a MediaItem. */
  async getLiveStreams(signal?: AbortSignal): Promise<MediaItem[]> {
    const raw = await this.getJson<
      Array<{
        stream_id: number;
        name: string;
        stream_icon?: string;
        epg_channel_id?: string;
        category_id?: string;
        added?: string | number;
      }>
    >(this.api("get_live_streams"), signal);

    return raw.map((s) => ({
      id: `live-${s.stream_id}`,
      type: "live" as const,
      title: s.name,
      streamUrl: this.buildStreamUrl("live", s.stream_id, "m3u8"),
      logo: s.stream_icon || undefined,
      group: s.category_id ? String(s.category_id) : undefined,
      epgId: s.epg_channel_id || undefined,
      addedAt: s.added ? Number(s.added) || undefined : undefined,
    }));
  }

  /** Descarga el catálogo VOD (películas). */
  async getMovies(signal?: AbortSignal): Promise<MediaItem[]> {
    const raw = await this.getJson<
      Array<{
        stream_id: number;
        name: string;
        stream_icon?: string;
        category_id?: string;
        container_extension?: string;
        rating_5based?: number | string;
        rating?: number | string;
        year?: string;
        added?: string | number;
      }>
    >(this.api("get_vod_streams"), signal);

    return raw.map((s) => ({
      id: `movie-${s.stream_id}`,
      type: "movie" as const,
      title: s.name,
      streamUrl: this.buildStreamUrl("movie", s.stream_id, s.container_extension || "mp4"),
      logo: s.stream_icon || undefined,
      group: s.category_id ? String(s.category_id) : undefined,
      rating: normalizeRating(s.rating_5based, s.rating),
      year: s.year || undefined,
      addedAt: s.added ? Number(s.added) || undefined : undefined,
    }));
  }

  /**
   * Descarga el catálogo de series. Ojo: en Xtream una serie no es reproducible
   * directamente; hay que pedir `get_series_info` para obtener sus episodios
   * (streamUrl queda vacío aquí y se resuelve al abrir la serie).
   */
  async getSeries(signal?: AbortSignal): Promise<MediaItem[]> {
    const raw = await this.getJson<
      Array<{
        series_id: number;
        name: string;
        cover?: string;
        category_id?: string;
        rating_5based?: number | string;
        rating?: number | string;
        releaseDate?: string;
      }>
    >(this.api("get_series"), signal);

    return raw.map((s) => ({
      id: `series-${s.series_id}`,
      type: "series" as const,
      title: s.name,
      streamUrl: "", // se resuelve con get_series_info al abrir la serie
      logo: s.cover || undefined,
      group: s.category_id ? String(s.category_id) : undefined,
      rating: normalizeRating(s.rating_5based, s.rating),
      year: s.releaseDate ? s.releaseDate.slice(0, 4) : undefined,
      extra: { seriesId: String(s.series_id) },
    }));
  }

  /**
   * Detalle de una serie: temporadas con sus episodios ya reproducibles.
   * Llama a `get_series_info` y arma la URL de cada episodio.
   */
  async getSeriesInfo(seriesId: string | number, signal?: AbortSignal): Promise<SeriesDetail> {
    const raw = await this.getJson<{
      info?: { name?: string; cover?: string; plot?: string };
      episodes?: Record<
        string,
        Array<{
          id: string | number;
          title?: string;
          episode_num?: number | string;
          container_extension?: string;
        }>
      >;
    }>(this.api("get_series_info", { series_id: String(seriesId) }), signal);

    const seasons: SeriesSeason[] = Object.entries(raw.episodes ?? {})
      .map(([season, eps]) => ({
        season: Number(season),
        episodes: eps.map((e) => ({
          id: String(e.id),
          title: e.title || `Episodio ${e.episode_num ?? ""}`.trim(),
          episodeNum: Number(e.episode_num) || undefined,
          streamUrl: this.buildStreamUrl("series", e.id, e.container_extension || "mp4"),
        })),
      }))
      .sort((a, b) => a.season - b.season);

    return {
      name: raw.info?.name,
      cover: raw.info?.cover,
      plot: raw.info?.plot,
      seasons,
    };
  }

  /** Guía electrónica (EPG) corta para un canal. */
  async getShortEpg(streamId: string | number, signal?: AbortSignal): Promise<EpgEntry[]> {
    const raw = await this.getJson<{
      epg_listings?: Array<{
        title: string;
        description?: string;
        start_timestamp: string | number;
        stop_timestamp: string | number;
      }>;
    }>(this.api("get_short_epg", { stream_id: String(streamId) }), signal);

    return (raw.epg_listings ?? []).map((e) => ({
      channelId: String(streamId),
      title: decodeMaybeBase64(e.title),
      description: e.description ? decodeMaybeBase64(e.description) : undefined,
      start: Number(e.start_timestamp) * 1000,
      stop: Number(e.stop_timestamp) * 1000,
    }));
  }

  /**
   * Descarga la guía completa (XMLTV) del portal y la agrupa por canal. Útil
   * para mostrar "ahora / después" en todos los canales de una vez.
   */
  async getEpg(signal?: AbortSignal): Promise<Map<string, EpgEntry[]>> {
    const res = await this.fetchFn(
      `${this.base}/xmltv.php?username=${encodeURIComponent(this.user)}&password=${encodeURIComponent(this.pass)}`,
      { signal },
    );
    if (!res.ok) throw new Error(`No se pudo descargar la EPG (${res.status})`);
    // Carga diferida del parser EPG (solo se necesita al pedir la guía).
    const { parseXmltv, groupEpgByChannel } = await import("./epg.js");
    return groupEpgByChannel(parseXmltv(await res.text()));
  }

  /** Carga en vivo (categorías + canales) como PlaylistContent unificado. */
  async loadLive(signal?: AbortSignal): Promise<PlaylistContent> {
    const [categories, items] = await Promise.all([
      this.getCategories("live", signal),
      this.getLiveStreams(signal),
    ]);
    return { categories: withCounts(categories, items), items };
  }

  /** Carga películas (categorías + items) como PlaylistContent. */
  async loadMovies(signal?: AbortSignal): Promise<PlaylistContent> {
    const [categories, items] = await Promise.all([
      this.getCategories("movie", signal),
      this.getMovies(signal),
    ]);
    return { categories: withCounts(categories, items), items };
  }

  /** Carga series (categorías + items) como PlaylistContent. */
  async loadSeries(signal?: AbortSignal): Promise<PlaylistContent> {
    const [categories, items] = await Promise.all([
      this.getCategories("series", signal),
      this.getSeries(signal),
    ]);
    return { categories: withCounts(categories, items), items };
  }
}

/** Convierte el rating de Xtream (0–5 o 0–10) a una escala 0–10. */
function normalizeRating(
  fiveBased?: number | string,
  raw?: number | string,
): number | undefined {
  if (fiveBased != null && fiveBased !== "") {
    const v = Number(fiveBased);
    if (!Number.isNaN(v)) return Math.round(v * 2 * 10) / 10;
  }
  if (raw != null && raw !== "") {
    const v = Number(raw);
    if (!Number.isNaN(v)) return v;
  }
  return undefined;
}

/**
 * Rellena `count` en cada categoría contando los items que pertenecen a ella,
 * como la barra lateral de las apps IPTV (p. ej. "TV | DEPORTES  510").
 */
export function withCounts(categories: Category[], items: MediaItem[]): Category[] {
  const counts = new Map<string, number>();
  for (const it of items) {
    if (!it.group) continue;
    counts.set(it.group, (counts.get(it.group) ?? 0) + 1);
  }
  return categories.map((c) => ({ ...c, count: counts.get(c.id) ?? 0 }));
}

/** Xtream a veces devuelve títulos EPG en base64; los decodificamos si aplica. */
function decodeMaybeBase64(value: string): string {
  if (!/^[A-Za-z0-9+/=]+$/.test(value) || value.length % 4 !== 0) return value;
  try {
    // atob existe en navegadores/Tizen/webOS; en Node caemos a Buffer sin
    // depender de @types/node (el núcleo debe tipar igual en navegador).
    const nodeBuffer = (globalThis as { Buffer?: { from(s: string, enc: string): { toString(e: string): string } } })
      .Buffer;
    const decoded =
      typeof atob === "function"
        ? atob(value)
        : nodeBuffer
          ? nodeBuffer.from(value, "base64").toString("utf-8")
          : value;
    // Si el resultado es imprimible, lo usamos; si no, devolvemos el original.
    return /[\x00-\x08\x0e-\x1f]/.test(decoded) ? value : decoded;
  } catch {
    return value;
  }
}
