import AsyncStorage from "@react-native-async-storage/async-storage";
import type { MediaItem } from "@tvapp/core";

/**
 * Biblioteca local (favoritos + continuar viendo) para la app de TV, con
 * AsyncStorage. Misma lógica que la web pero asíncrona. Separada por lista.
 */
const FAV_KEY = "tvapp.favorites.v1";
const PROG_KEY = "tvapp.progress.v1";

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

function snap(item: MediaItem | Snapshot): Snapshot {
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

async function readMap<T>(key: string): Promise<Record<string, T>> {
  try {
    return JSON.parse((await AsyncStorage.getItem(key)) || "{}") as Record<string, T>;
  } catch {
    return {};
  }
}
async function writeMap<T>(key: string, map: Record<string, T>): Promise<void> {
  await AsyncStorage.setItem(key, JSON.stringify(map));
}
function composite(playlistId: string, itemId: string): string {
  return `${playlistId}::${itemId}`;
}

export async function isFavorite(playlistId: string, itemId: string): Promise<boolean> {
  return composite(playlistId, itemId) in (await readMap<Snapshot>(FAV_KEY));
}

export async function toggleFavorite(playlistId: string, item: MediaItem): Promise<boolean> {
  const map = await readMap<Snapshot>(FAV_KEY);
  const key = composite(playlistId, item.id);
  const nowFav = !(key in map);
  if (nowFav) map[key] = snap(item);
  else delete map[key];
  await writeMap(FAV_KEY, map);
  return nowFav;
}

export async function listFavorites(playlistId: string, type?: Snapshot["type"]): Promise<Snapshot[]> {
  const prefix = `${playlistId}::`;
  return Object.entries(await readMap<Snapshot>(FAV_KEY))
    .filter(([k]) => k.startsWith(prefix))
    .map(([, v]) => v)
    .filter((s) => (type ? s.type === type : true));
}

export async function saveProgress(
  playlistId: string,
  item: MediaItem | Snapshot,
  positionSec: number,
  durationSec: number,
): Promise<void> {
  const map = await readMap<Progress>(PROG_KEY);
  const key = composite(playlistId, item.id);
  if (durationSec > 0 && positionSec / durationSec > 0.92) delete map[key];
  else if (positionSec > 15) map[key] = { item: snap(item), positionSec, durationSec, updatedAt: Date.now() };
  await writeMap(PROG_KEY, map);
}

export async function getProgress(playlistId: string, itemId: string): Promise<Progress | null> {
  return (await readMap<Progress>(PROG_KEY))[composite(playlistId, itemId)] ?? null;
}

export async function listContinue(playlistId: string): Promise<Progress[]> {
  const prefix = `${playlistId}::`;
  return Object.entries(await readMap<Progress>(PROG_KEY))
    .filter(([k]) => k.startsWith(prefix))
    .map(([, v]) => v)
    .sort((a, b) => b.updatedAt - a.updatedAt);
}
