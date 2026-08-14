import type { Playlist } from "@tvapp/core";

/**
 * Persistencia local de las listas de reproducción del usuario. En TV usamos
 * localStorage (disponible en Tizen/webOS/navegador). No se envía nada a
 * ningún servidor: las credenciales del usuario viven solo en su dispositivo.
 */
const KEY = "tvapp.playlists.v1";

export function loadPlaylists(): Playlist[] {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Playlist[]) : [];
  } catch {
    return [];
  }
}

export function savePlaylists(playlists: Playlist[]): void {
  localStorage.setItem(KEY, JSON.stringify(playlists));
}

export function addPlaylist(playlist: Playlist): Playlist[] {
  const next = [...loadPlaylists(), playlist];
  savePlaylists(next);
  return next;
}

export function removePlaylist(id: string): Playlist[] {
  const next = loadPlaylists().filter((p) => p.id !== id);
  savePlaylists(next);
  return next;
}

/** Genera un id sin depender de crypto.randomUUID (no está en TV viejos). */
export function newId(): string {
  return `pl-${Date.now().toString(36)}-${Math.floor(Math.random() * 1e6).toString(36)}`;
}
