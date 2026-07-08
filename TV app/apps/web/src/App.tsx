import { useCallback, useEffect, useRef, useState } from "react";
import {
  parseM3U,
  XtreamClient,
  fromPlaylist,
  type Category,
  type MediaItem,
  type Playlist,
  type PlaylistContent,
} from "@tvapp/core";
import { addPlaylist, loadPlaylists, removePlaylist } from "./storage.js";
import { moveFocus, useRemote, type RemoteKey } from "./remote.js";
import { PlaylistForm } from "./components/PlaylistForm.js";
import { ChannelGrid } from "./components/ChannelGrid.js";
import { VideoPlayer } from "./components/VideoPlayer.js";

type View =
  | { screen: "home" }
  | { screen: "form" }
  | { screen: "browse"; playlist: Playlist }
  | { screen: "play"; item: MediaItem };

/** Carga el contenido de una playlist según su tipo (M3U o Xtream). */
async function loadContent(p: Playlist): Promise<PlaylistContent> {
  if (p.kind === "m3u") {
    const res = await fetch(p.url);
    if (!res.ok) throw new Error(`No se pudo descargar la lista (${res.status})`);
    return parseM3U(await res.text());
  }
  const client = new XtreamClient(fromPlaylist(p));
  return client.loadLive();
}

export function App() {
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [view, setView] = useState<View>({ screen: "home" });
  const [content, setContent] = useState<PlaylistContent | null>(null);
  const [category, setCategory] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  // Recordamos la última playlist abierta para volver a ella desde el player.
  const lastPlaylist = useRef<Playlist | null>(null);

  useEffect(() => setPlaylists(loadPlaylists()), []);

  // Navegación con control remoto: flechas mueven foco, "Atrás" retrocede.
  const onRemote = useCallback((key: RemoteKey) => {
    if (key === "enter") {
      (document.activeElement as HTMLElement | null)?.click();
      return;
    }
    if (key === "back") {
      setView((v) => {
        if (v.screen === "play") {
          return lastPlaylist.current
            ? { screen: "browse", playlist: lastPlaylist.current }
            : { screen: "home" };
        }
        if (v.screen === "browse" || v.screen === "form") return { screen: "home" };
        return v;
      });
      return;
    }
    moveFocus(key);
  }, []);
  useRemote(onRemote);

  const openPlaylist = useCallback(async (p: Playlist) => {
    lastPlaylist.current = p;
    setStatus("Cargando contenido…");
    setView({ screen: "browse", playlist: p });
    try {
      const c = await loadContent(p);
      setContent(c);
      setCategory(null);
      setStatus(c.items.length === 0 ? "La lista no trajo canales." : null);
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Error al cargar la lista");
      setContent(null);
    }
  }, []);

  function handleCreate(p: Playlist) {
    setPlaylists(addPlaylist(p));
    setView({ screen: "home" });
  }

  function handleRemove(id: string) {
    setPlaylists(removePlaylist(id));
  }

  return (
    <div className="app">
      <header className="topbar">
        <h1 className="brand">TV App</h1>
      </header>

      {view.screen === "home" && (
        <main className="home">
          <div className="home__head">
            <h2>Listas de reproducción</h2>
            <button
              data-focusable
              className="btn btn--primary"
              onClick={() => setView({ screen: "form" })}
            >
              + Nueva lista
            </button>
          </div>

          {playlists.length === 0 ? (
            <p className="empty">
              Aún no tienes listas. Crea una con tus credenciales M3U o Xtream.
            </p>
          ) : (
            <ul className="playlists">
              {playlists.map((p) => (
                <li key={p.id} className="playlist-row">
                  <button
                    data-focusable
                    className="playlist-row__open"
                    onClick={() => openPlaylist(p)}
                  >
                    <span className="playlist-row__name">{p.name || p.url}</span>
                    <span className="playlist-row__kind">{p.kind.toUpperCase()}</span>
                  </button>
                  <button
                    data-focusable
                    className="btn btn--ghost"
                    onClick={() => handleRemove(p.id)}
                  >
                    Eliminar
                  </button>
                </li>
              ))}
            </ul>
          )}
        </main>
      )}

      {view.screen === "form" && (
        <PlaylistForm onCreate={handleCreate} onCancel={() => setView({ screen: "home" })} />
      )}

      {view.screen === "browse" && (
        <main className="browse-screen">
          <button
            data-focusable
            className="btn btn--ghost"
            onClick={() => setView({ screen: "home" })}
          >
            ← Listas
          </button>
          {status && <p className="status">{status}</p>}
          {content && (
            <ChannelGrid
              categories={content.categories as Category[]}
              items={content.items}
              activeCategory={category}
              onSelectCategory={setCategory}
              onPlay={(item) => setView({ screen: "play", item })}
            />
          )}
        </main>
      )}

      {view.screen === "play" && (
        <VideoPlayer
          src={view.item.streamUrl}
          onBack={() =>
            setView(
              lastPlaylist.current
                ? { screen: "browse", playlist: lastPlaylist.current }
                : { screen: "home" },
            )
          }
        />
      )}
    </div>
  );
}
