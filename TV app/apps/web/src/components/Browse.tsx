import { useEffect, useMemo, useState } from "react";
import {
  XtreamClient,
  fromPlaylist,
  parseM3U,
  type MediaItem,
  type Playlist,
  type PlaylistContent,
} from "@tvapp/core";
import type { Section } from "./Dashboard.js";

const TITLES: Record<Section, string> = {
  live: "TV en vivo",
  movie: "Películas",
  series: "Series",
};

async function loadSection(p: Playlist, section: Section): Promise<PlaylistContent> {
  if (p.kind === "m3u") {
    const res = await fetch(p.url);
    if (!res.ok) throw new Error(`No se pudo descargar la lista (${res.status})`);
    return parseM3U(await res.text());
  }
  const client = new XtreamClient(fromPlaylist(p));
  if (section === "movie") return client.loadMovies();
  if (section === "series") return client.loadSeries();
  return client.loadLive();
}

/**
 * Navegador con barra lateral de categorías (con contadores y buscador) y una
 * rejilla a la derecha: logos para TV en vivo, pósters para películas/series.
 */
export function Browse({
  playlist,
  section,
  onPlay,
  onBack,
}: {
  playlist: Playlist;
  section: Section;
  onPlay: (item: MediaItem) => void;
  onBack: () => void;
}) {
  const RECENT = "__recent__";
  const [content, setContent] = useState<PlaylistContent | null>(null);
  const [category, setCategory] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("Cargando…");
  const [query, setQuery] = useState("");
  const [nonce, setNonce] = useState(0);

  useEffect(() => {
    let alive = true;
    if (nonce === 0) setContent(null);
    setStatus(content ? "" : "Cargando…");
    loadSection(playlist, section)
      .then((c) => {
        if (!alive) return;
        setContent(c);
        setStatus(c.items.length === 0 ? "Sin contenido en esta sección." : "");
      })
      .catch((err: unknown) => {
        if (!alive) return;
        setStatus(err instanceof Error ? err.message : "Error al cargar");
      });
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playlist, section, nonce]);

  // Auto-refresco: vuelve a consultar la fuente cada 10 minutos para traer lo
  // nuevo que el servidor/proveedor haya agregado, sin intervención del usuario.
  useEffect(() => {
    const t = setInterval(() => setNonce((n) => n + 1), 10 * 60 * 1000);
    return () => clearInterval(t);
  }, []);

  const cats = useMemo(() => {
    const list = content?.categories ?? [];
    if (!query.trim()) return list;
    const q = query.toLowerCase();
    return list.filter((c) => c.name.toLowerCase().includes(q));
  }, [content, query]);

  const recent = content
    ? [...content.items]
        .filter((i) => i.addedAt)
        .sort((a, b) => (b.addedAt ?? 0) - (a.addedAt ?? 0))
        .slice(0, 60)
    : [];

  const items = content
    ? category === RECENT
      ? recent
      : category
        ? content.items.filter((i) => i.group === category)
        : content.items
    : [];

  const isVod = section !== "live";
  const total = content?.items.length ?? 0;

  return (
    <div className="browse2">
      <aside className="side">
        <div className="side__head">
          <button data-focusable className="side__back" onClick={onBack}>‹</button>
          <span className="brand brand--sm">
            More<span className="brand__accent">TV</span>
          </span>
        </div>
        <input
          data-focusable
          className="side__search"
          placeholder="Buscar en categorías"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="side__list">
          <button
            data-focusable
            className={`side__item ${category === null ? "is-active" : ""}`}
            onClick={() => setCategory(null)}
          >
            <span>ALL</span>
            <span className="side__count">{total}</span>
          </button>
          {recent.length > 0 && (
            <button
              data-focusable
              className={`side__item ${category === RECENT ? "is-active" : ""}`}
              onClick={() => setCategory(RECENT)}
            >
              <span className="side__name">🆕 Recién agregado</span>
              <span className="side__count">{recent.length}</span>
            </button>
          )}
          {cats.map((c) => (
            <button
              key={c.id}
              data-focusable
              className={`side__item ${category === c.id ? "is-active" : ""}`}
              onClick={() => setCategory(c.id)}
            >
              <span className="side__name">{c.name}</span>
              <span className="side__count">{c.count ?? 0}</span>
            </button>
          ))}
        </div>
      </aside>

      <section className="content">
        <div className="content__head">
          <h2 className="content__title">{TITLES[section]}</h2>
          <button
            data-focusable
            className="content__refresh"
            title="Refrescar"
            onClick={() => setNonce((n) => n + 1)}
          >
            ⟳
          </button>
        </div>
        {status && <p className="status">{status}</p>}
        <div className={isVod ? "poster-grid" : "logo-grid"}>
          {items.slice(0, 120).map((item) => (
            <button
              key={item.id}
              data-focusable
              className={isVod ? "poster" : "logo-card"}
              onClick={() => onPlay(item)}
            >
              {item.logo ? (
                <img
                  className={isVod ? "poster__img" : "logo-card__img"}
                  src={item.logo}
                  alt=""
                  loading="lazy"
                />
              ) : (
                <div className={`${isVod ? "poster__img" : "logo-card__img"} ph`}>
                  {item.title.slice(0, 2).toUpperCase()}
                </div>
              )}
              {isVod && item.rating ? (
                <span className="poster__badge">{item.rating.toFixed(1)}</span>
              ) : null}
              <span className={isVod ? "poster__title" : "logo-card__title"}>{item.title}</span>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}
