import React, { useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import type { Playlist } from "@tvapp/core";
import { theme } from "../theme";

export type Section = "live" | "movie" | "series";

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

/** Dashboard con mosaicos LIVE / MOVIES / SERIES y accesos secundarios. */
export function DashboardScreen({
  playlist,
  onOpenSection,
  onAccount,
}: {
  playlist: Playlist;
  onOpenSection: (s: Section) => void;
  onAccount: () => void;
}) {
  const clock = useClock();

  return (
    <View style={styles.container}>
      <View style={styles.top}>
        <Text style={styles.brand}>
          More<Text style={styles.accent}>TV</Text>
        </Text>
        <Text style={styles.clock}>{clock}</Text>
      </View>

      <View style={styles.grid}>
        <Pressable
          hasTVPreferredFocus
          style={({ focused }) => [styles.tile, styles.live, focused && styles.focused]}
          onPress={() => onOpenSection("live")}
        >
          <Text style={styles.icon}>📺</Text>
          <Text style={styles.label}>LIVE</Text>
        </Pressable>

        <View style={styles.col}>
          <Pressable
            style={({ focused }) => [styles.tile, styles.movies, focused && styles.focused]}
            onPress={() => onOpenSection("movie")}
          >
            <Text style={styles.icon}>▶</Text>
            <Text style={styles.label}>MOVIES</Text>
          </Pressable>
          <Pressable
            style={({ focused }) => [styles.pill, focused && styles.focused]}
            onPress={() => onOpenSection("live")}
          >
            <Text style={styles.pillText}>UPDATE EPG</Text>
          </Pressable>
        </View>

        <View style={styles.col}>
          <Pressable
            style={({ focused }) => [styles.tile, styles.series, focused && styles.focused]}
            onPress={() => onOpenSection("series")}
          >
            <Text style={styles.icon}>🎬</Text>
            <Text style={styles.label}>SERIES</Text>
          </Pressable>
          <Pressable
            style={({ focused }) => [styles.pill, focused && styles.focused]}
            onPress={onAccount}
          >
            <Text style={styles.pillText}>ACCOUNT</Text>
          </Pressable>
        </View>
      </View>

      <View style={styles.foot}>
        <Text style={styles.footMuted}>Lista activa</Text>
        <Text style={styles.footName}>{playlist.name || playlist.url}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 48 },
  top: { flexDirection: "row", alignItems: "center", gap: 32, marginBottom: 40 },
  brand: { color: theme.text, fontSize: 34, fontWeight: "800" },
  accent: { color: theme.accent2 },
  clock: { color: theme.text, fontSize: 22, fontWeight: "600" },
  grid: { flex: 1, flexDirection: "row", gap: 28 },
  col: { flex: 1, gap: 24 },
  tile: { flex: 1, borderRadius: 24, alignItems: "center", justifyContent: "center", gap: 16 },
  // Colores sólidos de los mosaicos (para degradados usar react-native-linear-gradient).
  live: { flex: 1.15, backgroundColor: "#2f7bff" },
  movies: { backgroundColor: "#e0245e" },
  series: { backgroundColor: "#7a3bff" },
  icon: { fontSize: 64 },
  label: { color: "#fff", fontSize: 30, fontWeight: "800", letterSpacing: 1 },
  pill: { backgroundColor: "#6db39a", borderRadius: 16, padding: 20, alignItems: "center" },
  pillText: { color: "#06251c", fontSize: 22, fontWeight: "800" },
  foot: { flexDirection: "row", justifyContent: "space-between", marginTop: 32 },
  footMuted: { color: theme.muted, fontSize: 20 },
  footName: { color: theme.text, fontSize: 20, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.03 }] },
});
