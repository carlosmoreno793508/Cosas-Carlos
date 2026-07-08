import AsyncStorage from "@react-native-async-storage/async-storage";
import type { Playlist } from "@tvapp/core";

/**
 * Persistencia local de las listas del usuario con AsyncStorage. Igual que en la
 * app web: los datos (incluidas credenciales) viven solo en el dispositivo.
 */
const KEY = "tvapp.playlists.v1";

export async function loadPlaylists(): Promise<Playlist[]> {
  try {
    const raw = await AsyncStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Playlist[]) : [];
  } catch {
    return [];
  }
}

export async function savePlaylists(playlists: Playlist[]): Promise<void> {
  await AsyncStorage.setItem(KEY, JSON.stringify(playlists));
}

export async function addPlaylist(playlist: Playlist): Promise<Playlist[]> {
  const next = [...(await loadPlaylists()), playlist];
  await savePlaylists(next);
  return next;
}

export async function removePlaylist(id: string): Promise<Playlist[]> {
  const next = (await loadPlaylists()).filter((p) => p.id !== id);
  await savePlaylists(next);
  return next;
}

export function newId(): string {
  return `pl-${Date.now().toString(36)}-${Math.floor(Math.random() * 1e6).toString(36)}`;
}
