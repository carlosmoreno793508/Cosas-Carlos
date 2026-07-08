import { useEffect, useMemo, useState } from "react";
import {
  XtreamClient,
  fromPlaylist,
  parseM3U,
  type MediaItem,
  type Playlist,
} from "@tvapp/core";

/**
 * Buscador global: carga canales, películas y series de la lista y filtra por
 * título en todas las secciones a la vez (lo que las apps IPTV llaman "Master
 * Search"). Para M3U solo hay canales.
 */
async function loadAll(p: Playlist): Promise<MediaItem[]> {
  if (p.kind === "m3u") {
    const res = await fetch(p.url);
    if (!res.ok) throw new Error(`No se pudo descargar la lista (${res.status})`);
    return parseM3U(await res.text()).items;
  }
  const client = new XtreamClient(fromPlaylist(p));
  const [live, movies, series] = await Promise.all([
    client.getLiveStreams(),
    client.getMovies(),
    client.getSeries(),
  ]);
  return [...live, ...movies, ...series];
}

const KIND_LABEL: Record<string, string> = { live: "TV", movie: "Película", series: "Serie" };

export function SearchScreen({
  playlist,
  onSelect,
  onBack,
}: {
  playlist: Playlist;
  onSelect: (item: MediaItem) => void;
  onBack: () => void;
}) {
  const [all, setAll] = useState<MediaItem[] | null>(null);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("Cargando catálogo…");

  useEffect(() => {
    let alive = true;
    loadAll(playlist)
      .then((items) => {
        if (!alive) return;
        setAll(items);
        setStatus("");
      })
      .catch((err: unknown) => {
        if (!alive) return;
        setStatus(err instanceof Error ? err.message : "Error al cargar");
      });
    return () => {
      alive = false;
    };
  }, [playlist]);

  const results = useMemo(() => {
    if (!all || query.trim().length < 2) return [];
    const q = query.toLowerCase();
    return all.filter((i) => i.title.toLowerCase().includes(q)).slice(0, 120);
  }, [all, query]);

  return (
    <div className="search-screen">
      <div className="search-bar">
        <button data-focusable className="side__back" onClick={onBack}>‹</button>
        <input
          data-focusable
          autoFocus
          className="search-bar__input"
          placeholder="Buscar películas, series o canales…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {status && <p className="status">{status}</p>}
      {!status && query.trim().length < 2 && (
        <p className="empty">Escribe al menos 2 letras para buscar en todo el catálogo.</p>
      )}
      {!status && query.trim().length >= 2 && results.length === 0 && (
        <p className="empty">Sin resultados para “{query}”.</p>
      )}

      <div className="poster-grid">
        {results.map((item) => (
          <button key={`${item.type}-${item.id}`} data-focusable className="poster" onClick={() => onSelect(item)}>
            {item.logo ? (
              <img className="poster__img" src={item.logo} alt="" loading="lazy" />
            ) : (
              <div className="poster__img ph">{item.title.slice(0, 2).toUpperCase()}</div>
            )}
            <span className="poster__kind">{KIND_LABEL[item.type]}</span>
            <span className="poster__title">{item.title}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
