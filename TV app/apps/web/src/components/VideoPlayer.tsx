import { useEffect, useRef, useState } from "react";
import Hls from "hls.js";
import type { MediaItem } from "@tvapp/core";
import {
  getProgress,
  isFavorite,
  saveProgress,
  toggleFavorite,
  type Snapshot,
} from "../library.js";
import { proxied } from "../settings.js";

/**
 * Reproductor de video. Usa HLS nativo cuando el TV lo soporta y cae a hls.js en
 * el resto. Si recibe `item` + `playlistId`, guarda el progreso (continuar
 * viendo), reanuda desde donde quedó y permite marcar favorito.
 */
export function VideoPlayer({
  src,
  onBack,
  playlistId,
  item,
}: {
  src: string;
  onBack: () => void;
  playlistId?: string;
  item?: MediaItem | Snapshot;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [fav, setFav] = useState(false);

  const canTrack = Boolean(playlistId && item && item.type !== "live");

  useEffect(() => {
    if (playlistId && item) setFav(isFavorite(playlistId, item.id));
  }, [playlistId, item]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    // Enruta el stream por el proxy (si está configurado) para saltar CORS.
    const playSrc = proxied(src);
    const isHls = /\.m3u8($|\?)/i.test(src);
    let hls: Hls | null = null;

    if (isHls && !video.canPlayType("application/vnd.apple.mpegurl") && Hls.isSupported()) {
      hls = new Hls({ enableWorker: true });
      hls.loadSource(playSrc);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => void video.play().catch(() => {}));
    } else {
      video.src = playSrc;
      void video.play().catch(() => {});
    }

    // Reanudar desde la última posición guardada.
    const resume = () => {
      if (!canTrack || !playlistId || !item) return;
      const p = getProgress(playlistId, item.id);
      if (p && p.positionSec > 0 && p.positionSec < video.duration) {
        video.currentTime = p.positionSec;
      }
    };
    video.addEventListener("loadedmetadata", resume);

    // Guardar progreso cada ~10s.
    let last = 0;
    const onTime = () => {
      if (!canTrack || !playlistId || !item) return;
      if (video.currentTime - last < 10) return;
      last = video.currentTime;
      saveProgress(playlistId, snap(item), video.currentTime, video.duration || 0);
    };
    video.addEventListener("timeupdate", onTime);

    return () => {
      video.removeEventListener("loadedmetadata", resume);
      video.removeEventListener("timeupdate", onTime);
      // Guardado final al salir.
      if (canTrack && playlistId && item) {
        saveProgress(playlistId, snap(item), video.currentTime, video.duration || 0);
      }
      if (hls) hls.destroy();
      video.removeAttribute("src");
      video.load();
    };
  }, [src, playlistId, item, canTrack]);

  return (
    <div className="player" data-focusable tabIndex={0}>
      <video ref={videoRef} className="player__video" controls autoPlay playsInline />
      <button className="player__back btn btn--ghost" data-focusable onClick={onBack}>
        ← Volver
      </button>
      {playlistId && item && (
        <button
          className={`player__fav ${fav ? "is-fav" : ""}`}
          data-focusable
          onClick={() => item && setFav(toggleFavorite(playlistId, item as MediaItem))}
        >
          {fav ? "★ Favorito" : "☆ Favorito"}
        </button>
      )}
    </div>
  );
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
