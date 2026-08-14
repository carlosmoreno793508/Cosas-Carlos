import { useEffect, useState } from "react";
import {
  XtreamClient,
  fromPlaylist,
  type MediaItem,
  type Playlist,
  type SeriesDetail as Detail,
} from "@tvapp/core";
import { proxiedFetch } from "../settings.js";

/**
 * Pantalla de detalle de una serie: carga temporadas y episodios (get_series_info)
 * y permite elegir temporada y reproducir un episodio. Solo aplica a fuentes
 * Xtream; las M3U no tienen jerarquía de series.
 */
export function SeriesDetail({
  playlist,
  series,
  onPlayEpisode,
  onBack,
}: {
  playlist: Playlist;
  series: MediaItem;
  onPlayEpisode: (streamUrl: string, title: string, episodeId: string) => void;
  onBack: () => void;
}) {
  const [detail, setDetail] = useState<Detail | null>(null);
  const [season, setSeason] = useState<number | null>(null);
  const [status, setStatus] = useState("Cargando episodios…");

  useEffect(() => {
    let alive = true;
    const seriesId = series.extra?.seriesId ?? series.id.replace(/^series-/, "");
    if (playlist.kind !== "xtream") {
      setStatus("Las series solo están disponibles en fuentes Xtream.");
      return;
    }
    new XtreamClient(fromPlaylist(playlist), proxiedFetch())
      .getSeriesInfo(seriesId)
      .then((d) => {
        if (!alive) return;
        setDetail(d);
        setSeason(d.seasons[0]?.season ?? null);
        setStatus(d.seasons.length === 0 ? "Esta serie no tiene episodios." : "");
      })
      .catch((err: unknown) => {
        if (!alive) return;
        setStatus(err instanceof Error ? err.message : "Error al cargar la serie");
      });
    return () => {
      alive = false;
    };
  }, [playlist, series]);

  const current = detail?.seasons.find((s) => s.season === season);

  return (
    <div className="series">
      <header className="series__head">
        <button data-focusable className="side__back" autoFocus onClick={onBack}>‹</button>
        {series.logo ? (
          <img className="series__cover" src={series.logo} alt="" />
        ) : (
          <div className="series__cover ph">{series.title.slice(0, 2).toUpperCase()}</div>
        )}
        <div className="series__meta">
          <h2 className="series__title">{detail?.name || series.title}</h2>
          {series.rating ? <span className="series__rating">★ {series.rating.toFixed(1)}</span> : null}
          {detail?.plot ? <p className="series__plot">{detail.plot}</p> : null}
        </div>
      </header>

      {status && <p className="status">{status}</p>}

      {detail && detail.seasons.length > 0 && (
        <>
          <div className="series__seasons">
            {detail.seasons.map((s) => (
              <button
                key={s.season}
                data-focusable
                className={`chip ${s.season === season ? "chip--active" : ""}`}
                onClick={() => setSeason(s.season)}
              >
                Temporada {s.season}
              </button>
            ))}
          </div>

          <ul className="episodes">
            {current?.episodes.map((ep) => (
              <li key={ep.id}>
                <button
                  data-focusable
                  className="episode"
                  onClick={() => onPlayEpisode(ep.streamUrl, ep.title, ep.id)}
                >
                  <span className="episode__num">{ep.episodeNum ?? "▶"}</span>
                  <span className="episode__title">{ep.title}</span>
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
