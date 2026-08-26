import type { MediaItem } from "@tvapp/core";

/**
 * Biblioteca local del usuario: favoritos y "continuar viendo". Todo vive en el
 * dispositivo (localStorage), separado por lista de reproducción. Guardamos una
 * instantánea mínima del item para poder pintarlo sin volver a la fuente.
 */
const FAV_KEY = "tvapp.favorites.v1";
const PROG_KEY = "tvapp.progress.v1";

/** Instantánea reproducible de un item. */
export type Snapshot = Pick<
  MediaItem,
  "id" | "type" | "title" | "streamUrl" | "logo" | "group" | "rating"
>;

export interface Progress {
  item: Snapshot;
  positionSec: number;
  durationSec: number;
  updatedAt: number;
}

function snap(item: MediaItem): Snapshot {
  return {
    id: item.id,
    type: item.type,
    title: item.title,
    streamUrl: item.streamUrl,
    logo: item.logo,
    group: item.group,
    rating: item.rating,
  };
}

function readMap<T>(key: string): Record<string, T> {
  try {
    return JSON.parse(localStorage.getItem(key) || "{}") as Record<string, T>;
  } catch {
    return {};
  }
}
function writeMap<T>(key: string, map: Record<string, T>): void {
  localStorage.setItem(key, JSON.stringify(map));
}
function composite(playlistId: string, itemId: string): string {
  return `${playlistId}::${itemId}`;
}

// --- Favoritos ---

export function isFavorite(playlistId: string, itemId: string): boolean {
  return composite(playlistId, itemId) in readMap<Snapshot>(FAV_KEY);
}

/** Alterna favorito y devuelve el nuevo estado (true = ahora es favorito). */
export function toggleFavorite(playlistId: string, item: MediaItem): boolean {
  const map = readMap<Snapshot>(FAV_KEY);
  const key = composite(playlistId, item.id);
  const nowFav = !(key in map);
  if (nowFav) map[key] = snap(item);
  else delete map[key];
  writeMap(FAV_KEY, map);
  return nowFav;
}

/** Favoritos de una lista, opcionalmente filtrados por tipo (live/movie/series). */
export function listFavorites(playlistId: string, type?: Snapshot["type"]): Snapshot[] {
  const prefix = `${playlistId}::`;
  return Object.entries(readMap<Snapshot>(FAV_KEY))
    .filter(([k]) => k.startsWith(prefix))
    .map(([, v]) => v)
    .filter((s) => (type ? s.type === type : true));
}

// --- Continuar viendo ---

export function saveProgress(
  playlistId: string,
  item: Snapshot,
  positionSec: number,
  durationSec: number,
): void {
  const map = readMap<Progress>(PROG_KEY);
  const key = composite(playlistId, item.id);
  // Si casi terminó (>92%), lo quitamos de "continuar viendo".
  if (durationSec > 0 && positionSec / durationSec > 0.92) {
    delete map[key];
  } else if (positionSec > 15) {
    map[key] = { item, positionSec, durationSec, updatedAt: Date.now() };
  }
  writeMap(PROG_KEY, map);
}

export function getProgress(playlistId: string, itemId: string): Progress | null {
  return readMap<Progress>(PROG_KEY)[composite(playlistId, itemId)] ?? null;
}

/** Lista "continuar viendo" de una lista, de más reciente a más antiguo. */
export function listContinue(playlistId: string): Progress[] {
  const prefix = `${playlistId}::`;
  return Object.entries(readMap<Progress>(PROG_KEY))
    .filter(([k]) => k.startsWith(prefix))
    .map(([, v]) => v)
    .sort((a, b) => b.updatedAt - a.updatedAt);
}
