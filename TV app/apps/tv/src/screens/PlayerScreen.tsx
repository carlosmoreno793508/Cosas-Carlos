import React, { useEffect, useRef, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import Video, { type VideoRef } from "react-native-video";
import type { MediaItem } from "@tvapp/core";
import { theme } from "../theme";
import { getProgress, isFavorite, saveProgress, toggleFavorite } from "../library";

/**
 * Reproductor a pantalla completa con react-native-video (ExoPlayer/Media3 en
 * Android/Fire TV, AVPlayer en Apple TV). Si recibe item + playlistId, guarda
 * progreso (continuar viendo), reanuda desde donde quedó y marca favorito.
 */
export function PlayerScreen({
  src,
  title,
  onBack,
  playlistId,
  item,
}: {
  src: string;
  title: string;
  onBack: () => void;
  playlistId?: string;
  item?: MediaItem;
}) {
  const videoRef = useRef<VideoRef>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fav, setFav] = useState(false);
  const [resumeAt, setResumeAt] = useState(0);
  const lastSaved = useRef(0);

  const canTrack = Boolean(playlistId && item && item.type !== "live");

  useEffect(() => {
    if (!playlistId || !item) return;
    isFavorite(playlistId, item.id).then(setFav);
    if (canTrack) getProgress(playlistId, item.id).then((p) => p && setResumeAt(p.positionSec));
  }, [playlistId, item, canTrack]);

  return (
    <View style={styles.container}>
      <Video
        ref={videoRef}
        style={styles.video}
        source={{ uri: src }}
        resizeMode="contain"
        controls
        paused={false}
        onLoad={() => {
          setLoading(false);
          if (resumeAt > 0) videoRef.current?.seek(resumeAt);
        }}
        onProgress={({ currentTime, seekableDuration }) => {
          if (!canTrack || !playlistId || !item) return;
          if (currentTime - lastSaved.current < 10) return;
          lastSaved.current = currentTime;
          saveProgress(playlistId, item, currentTime, seekableDuration || 0);
        }}
        onError={() => {
          setLoading(false);
          setError("No se pudo reproducir este stream.");
        }}
      />

      {loading && !error && (
        <View style={styles.overlay}>
          <ActivityIndicator size="large" color={theme.text} />
          <Text style={styles.overlayText}>{title}</Text>
        </View>
      )}

      {error && (
        <View style={styles.overlay}>
          <Text style={styles.error}>{error}</Text>
        </View>
      )}

      <Pressable
        style={({ focused }) => [styles.back, focused && styles.focused]}
        hasTVPreferredFocus
        onPress={onBack}
      >
        <Text style={styles.backText}>← Volver</Text>
      </Pressable>

      {playlistId && item ? (
        <Pressable
          style={({ focused }) => [styles.fav, fav && styles.favOn, focused && styles.focused]}
          onPress={async () => setFav(await toggleFavorite(playlistId, item))}
        >
          <Text style={styles.favText}>{fav ? "★ Favorito" : "☆ Favorito"}</Text>
        </Pressable>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000" },
  video: { ...StyleSheet.absoluteFillObject },
  overlay: { ...StyleSheet.absoluteFillObject, alignItems: "center", justifyContent: "center" },
  overlayText: { color: theme.text, fontSize: 22, marginTop: 16 },
  error: { color: theme.danger, fontSize: 24, fontWeight: "700" },
  back: { position: "absolute", top: 32, left: 32, backgroundColor: theme.surface2, borderRadius: 999, paddingHorizontal: 22, paddingVertical: 12 },
  backText: { color: theme.text, fontSize: 20, fontWeight: "700" },
  fav: { position: "absolute", top: 32, right: 32, backgroundColor: theme.surface2, borderRadius: 999, paddingHorizontal: 22, paddingVertical: 12 },
  favOn: { backgroundColor: "#b8860b" },
  favText: { color: theme.text, fontSize: 20, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff" },
});
