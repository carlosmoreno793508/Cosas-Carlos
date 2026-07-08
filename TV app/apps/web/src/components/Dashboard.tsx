import { useEffect, useState } from "react";
import type { Playlist } from "@tvapp/core";

/** Formatea la hora y fecha como en la barra superior de las apps IPTV. */
function useClock(): string {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 30_000);
    return () => clearInterval(t);
  }, []);
  const time = now.toLocaleTimeString("es-MX", { hour: "numeric", minute: "2-digit", hour12: true });
  const date = now.toLocaleDateString("es-MX", { day: "numeric", month: "short", year: "numeric" });
  return `${time}  ·  ${date}`;
}

export type Section = "live" | "movie" | "series";

/**
 * Pantalla principal tipo "dashboard": mosaicos grandes LIVE / MOVIES / SERIES y
 * accesos secundarios, replicando la estructura de IPTV Smarters pero con la
 * marca MoreTV.
 */
export function Dashboard({
  playlist,
  onOpenSection,
  onAccount,
  onBack,
}: {
  playlist: Playlist;
  onOpenSection: (s: Section) => void;
  onAccount: () => void;
  onBack: () => void;
}) {
  const clock = useClock();

  return (
    <div className="dash">
      <header className="dash__top">
        <h1 className="brand">
          More<span className="brand__accent">TV</span>
        </h1>
        <span className="dash__clock">{clock}</span>
        <div className="dash__tools">
          <button data-focusable className="tool" title="Buscar">⌕</button>
          <button data-focusable className="tool" title="Ajustes" onClick={onBack}>⚙</button>
        </div>
      </header>

      <main className="dash__grid">
        <button
          data-focusable
          className="tile tile--live"
          autoFocus
          onClick={() => onOpenSection("live")}
        >
          <span className="tile__icon">📺</span>
          <span className="tile__label">LIVE</span>
        </button>

        <div className="dash__col">
          <button data-focusable className="tile tile--movies" onClick={() => onOpenSection("movie")}>
            <span className="tile__icon">▶</span>
            <span className="tile__label">MOVIES</span>
          </button>
          <button data-focusable className="pill" onClick={() => onOpenSection("live")}>
            📖 UPDATE EPG
          </button>
        </div>

        <div className="dash__col">
          <button data-focusable className="tile tile--series" onClick={() => onOpenSection("series")}>
            <span className="tile__icon">🎬</span>
            <span className="tile__label">SERIES</span>
          </button>
          <button data-focusable className="pill" onClick={onAccount}>
            ⓘ ACCOUNT
          </button>
        </div>
      </main>

      <footer className="dash__foot">
        <span>Expira: —</span>
        <span className="dash__playlist">Lista: {playlist.name || playlist.url}</span>
      </footer>
    </div>
  );
}
