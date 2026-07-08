import { useCallback, useEffect, useState } from "react";
import type { MediaItem, Playlist } from "@tvapp/core";
import { addPlaylist, loadPlaylists } from "./storage.js";
import { moveFocus, useRemote, type RemoteKey } from "./remote.js";
import { PlaylistForm } from "./components/PlaylistForm.js";
import { Dashboard, type Section } from "./components/Dashboard.js";
import { Browse } from "./components/Browse.js";
import { SeriesDetail } from "./components/SeriesDetail.js";
import { VideoPlayer } from "./components/VideoPlayer.js";

type View =
  | { screen: "home" }
  | { screen: "form" }
  | { screen: "dashboard"; playlist: Playlist }
  | { screen: "account"; playlist: Playlist }
  | { screen: "browse"; playlist: Playlist; section: Section }
  | { screen: "series"; playlist: Playlist; series: MediaItem }
  | { screen: "play"; src: string; title: string; playlist: Playlist; item?: MediaItem; back: View };

export function App() {
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [view, setView] = useState<View>({ screen: "home" });

  useEffect(() => setPlaylists(loadPlaylists()), []);

  const onRemote = useCallback((key: RemoteKey) => {
    if (key === "enter") {
      (document.activeElement as HTMLElement | null)?.click();
      return;
    }
    if (key === "back") {
      setView((v) => {
        switch (v.screen) {
          case "play":
            return v.back;
          case "series":
            return { screen: "browse", playlist: v.playlist, section: "series" };
          case "browse":
          case "account":
            return { screen: "dashboard", playlist: v.playlist };
          case "dashboard":
          case "form":
            return { screen: "home" };
          default:
            return v;
        }
      });
      return;
    }
    moveFocus(key);
  }, []);
  useRemote(onRemote);

  function handleCreate(p: Playlist) {
    setPlaylists(addPlaylist(p));
    setView({ screen: "dashboard", playlist: p });
  }

  switch (view.screen) {
    case "form":
      return <PlaylistForm onCreate={handleCreate} onCancel={() => setView({ screen: "home" })} />;

    case "dashboard":
      return (
        <Dashboard
          playlist={view.playlist}
          onOpenSection={(section) => setView({ screen: "browse", playlist: view.playlist, section })}
          onAccount={() => setView({ screen: "account", playlist: view.playlist })}
          onBack={() => setView({ screen: "home" })}
        />
      );

    case "account":
      return (
        <div className="app account">
          <h2>Cuenta</h2>
          <p><b>Lista:</b> {view.playlist.name || view.playlist.url}</p>
          <p><b>Tipo:</b> {view.playlist.kind.toUpperCase()}</p>
          {view.playlist.username && <p><b>Usuario:</b> {view.playlist.username}</p>}
          <button
            data-focusable
            className="btn btn--ghost"
            autoFocus
            onClick={() => setView({ screen: "dashboard", playlist: view.playlist })}
          >
            ‹ Volver
          </button>
        </div>
      );

    case "browse": {
      const browseView = view;
      return (
        <Browse
          playlist={browseView.playlist}
          section={browseView.section}
          onPlay={(item) => {
            if (item.type === "series") {
              setView({ screen: "series", playlist: browseView.playlist, series: item });
            } else {
              setView({
                screen: "play",
                src: item.streamUrl,
                title: item.title,
                playlist: browseView.playlist,
                item,
                back: browseView,
              });
            }
          }}
          onBack={() => setView({ screen: "dashboard", playlist: browseView.playlist })}
        />
      );
    }

    case "series": {
      const seriesView = view;
      return (
        <SeriesDetail
          playlist={seriesView.playlist}
          series={seriesView.series}
          onPlayEpisode={(src, title, episodeId) =>
            setView({
              screen: "play",
              src,
              title,
              playlist: seriesView.playlist,
              item: { id: `ep-${episodeId}`, type: "movie", title, streamUrl: src },
              back: seriesView,
            })
          }
          onBack={() => setView({ screen: "browse", playlist: seriesView.playlist, section: "series" })}
        />
      );
    }

    case "play":
      return (
        <VideoPlayer
          src={view.src}
          playlistId={view.playlist.id}
          item={view.item}
          onBack={() => setView(view.back)}
        />
      );

    case "home":
    default:
      return (
        <div className="chooser">
          <header className="chooser__top">
            <h1 className="brand">
              More<span className="brand__accent">TV</span>
            </h1>
            <span className="chooser__ver">v0.1</span>
          </header>

          <h2 className="chooser__title">ELIGE TU LISTA</h2>

          <div className="profiles">
            {playlists.map((p, i) => (
              <button
                key={p.id}
                data-focusable
                className="profile"
                autoFocus={i === 0}
                onClick={() => setView({ screen: "dashboard", playlist: p })}
              >
                <span className="profile__avatar" aria-hidden>
                  <svg viewBox="0 0 100 100" width="120" height="120">
                    <circle cx="50" cy="38" r="22" fill="#f0b48f" />
                    <path d="M18 92c0-20 14-30 32-30s32 10 32 30z" fill="#6b8bff" />
                  </svg>
                </span>
                <span className="profile__name">{p.name || p.url}</span>
              </button>
            ))}

            <button
              data-focusable
              className="profile profile--add"
              autoFocus={playlists.length === 0}
              onClick={() => setView({ screen: "form" })}
            >
              <span className="profile__plus">+</span>
              <span className="profile__name">Añadir lista</span>
            </button>
          </div>

          <footer className="chooser__foot">
            <p className="chooser__terms">Términos del servicio</p>
            <p className="chooser__hint">Selecciona una lista para entrar.</p>
          </footer>
        </div>
      );
  }
}
