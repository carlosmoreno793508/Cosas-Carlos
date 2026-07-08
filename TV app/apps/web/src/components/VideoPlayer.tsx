import { useEffect, useRef } from "react";
import Hls from "hls.js";

/**
 * Reproductor de video. Usa HLS nativo cuando el TV lo soporta (Safari/tvOS,
 * algunos Tizen/webOS) y cae a hls.js en el resto. Los .ts/.mp4 directos los
 * reproduce el propio <video>.
 */
export function VideoPlayer({ src, onBack }: { src: string; onBack: () => void }) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const isHls = /\.m3u8($|\?)/i.test(src);
    let hls: Hls | null = null;

    if (isHls && !video.canPlayType("application/vnd.apple.mpegurl") && Hls.isSupported()) {
      hls = new Hls({ enableWorker: true, lowLatencyMode: false });
      hls.loadSource(src);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => void video.play().catch(() => {}));
    } else {
      video.src = src;
      void video.play().catch(() => {});
    }

    return () => {
      if (hls) hls.destroy();
      video.removeAttribute("src");
      video.load();
    };
  }, [src]);

  return (
    <div className="player" data-focusable tabIndex={0}>
      <video ref={videoRef} className="player__video" controls autoPlay playsInline />
      <button className="player__back btn btn--ghost" data-focusable onClick={onBack}>
        ← Volver
      </button>
    </div>
  );
}
