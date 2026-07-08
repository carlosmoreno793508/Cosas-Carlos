import React, { useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import Video from "react-native-video";
import { theme } from "../theme";

/**
 * Reproductor a pantalla completa con react-native-video, que usa el reproductor
 * nativo de cada plataforma: ExoPlayer/Media3 en Fire TV y Android TV, AVPlayer
 * en Apple TV. Soporta HLS (.m3u8), TS y MP4.
 */
export function PlayerScreen({ src, title, onBack }: { src: string; title: string; onBack: () => void }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  return (
    <View style={styles.container}>
      <Video
        style={styles.video}
        source={{ uri: src }}
        resizeMode="contain"
        controls
        paused={false}
        onLoad={() => setLoading(false)}
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
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000" },
  video: { ...StyleSheet.absoluteFillObject },
  overlay: { ...StyleSheet.absoluteFillObject, alignItems: "center", justifyContent: "center" },
  overlayText: { color: theme.text, fontSize: 22, marginTop: 16 },
  error: { color: theme.danger, fontSize: 24, fontWeight: "700" },
  back: {
    position: "absolute",
    top: 32,
    left: 32,
    backgroundColor: theme.surface2,
    borderRadius: 999,
    paddingHorizontal: 22,
    paddingVertical: 12,
  },
  backText: { color: theme.text, fontSize: 20, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff" },
});
