import type {
  Category,
  EpgEntry,
  MediaItem,
  Playlist,
  PlaylistContent,
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
      }>
    >(this.api("get_vod_streams"), signal);

    return raw.map((s) => ({
      id: `movie-${s.stream_id}`,
      type: "movie" as const,
      title: s.name,
      streamUrl: this.buildStreamUrl("movie", s.stream_id, s.container_extension || "mp4"),
      logo: s.stream_icon || undefined,
      group: s.category_id ? String(s.category_id) : undefined,
    }));
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

  /** Carga en vivo (categorías + canales) como PlaylistContent unificado. */
  async loadLive(signal?: AbortSignal): Promise<PlaylistContent> {
    const [categories, items] = await Promise.all([
      this.getCategories("live", signal),
      this.getLiveStreams(signal),
    ]);
    return { categories, items };
  }
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
