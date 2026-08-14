import React, { useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View, useWindowDimensions } from "react-native";
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

/**
 * Dashboard con mosaicos LIVE / MOVIES / SERIES. Responsivo: en TV/horizontal
 * usa 3 columnas; en teléfono/vertical apila los mosaicos a lo ancho.
 */
export function DashboardScreen({
  playlist,
  onOpenSection,
  onAccount,
  onSearch,
}: {
  playlist: Playlist;
  onOpenSection: (s: Section) => void;
  onAccount: () => void;
  onSearch: () => void;
}) {
  const clock = useClock();
  const { width, height } = useWindowDimensions();
  const portrait = height >= width;

  const tile = (
    section: Section,
    label: string,
    icon: string,
    bg: object,
    preferred = false,
  ) => (
    <Pressable
      hasTVPreferredFocus={preferred}
      style={({ focused }) => [
        styles.tile,
        bg,
        portrait ? styles.tilePortrait : styles.tileLand,
        focused && styles.focused,
      ]}
      onPress={() => onOpenSection(section)}
    >
      <Text style={[styles.icon, portrait && styles.iconPortrait]}>{icon}</Text>
      <Text style={[styles.label, portrait && styles.labelPortrait]} numberOfLines={1}>
        {label}
      </Text>
    </Pressable>
  );

  const pill = (text: string, onPress: () => void) => (
    <Pressable style={({ focused }) => [styles.pill, focused && styles.focused]} onPress={onPress}>
      <Text style={styles.pillText} numberOfLines={1}>{text}</Text>
    </Pressable>
  );

  return (
    <View style={[styles.container, portrait && styles.containerPortrait]}>
      <View style={styles.top}>
        <Text style={styles.brand}>
          More<Text style={styles.accent}>TV</Text>
        </Text>
        {!portrait && <Text style={styles.clock}>{clock}</Text>}
        <Pressable style={({ focused }) => [styles.tool, focused && styles.focused]} onPress={onSearch}>
          <Text style={styles.toolText}>⌕</Text>
        </Pressable>
      </View>

      <View style={[styles.grid, portrait && styles.gridPortrait]}>
        {tile("live", "LIVE", "📺", styles.live, true)}
        <View style={[styles.col, portrait && styles.colPortrait]}>
          {tile("movie", "MOVIES", "▶", styles.movies)}
          {pill("📖 EPG", () => onOpenSection("live"))}
        </View>
        <View style={[styles.col, portrait && styles.colPortrait]}>
          {tile("series", "SERIES", "🎬", styles.series)}
          {pill("ⓘ Cuenta", onAccount)}
        </View>
      </View>

      <View style={styles.foot}>
        <Text style={styles.footMuted}>Lista activa</Text>
        <Text style={styles.footName} numberOfLines={1}>{playlist.name || playlist.url}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 48 },
  containerPortrait: { padding: 20 },
  top: { flexDirection: "row", alignItems: "center", gap: 20, marginBottom: 24 },
  brand: { color: theme.text, fontSize: 30, fontWeight: "800" },
  accent: { color: theme.accent2 },
  clock: { color: theme.text, fontSize: 20, fontWeight: "600" },
  tool: { marginLeft: "auto", width: 52, height: 52, borderRadius: 26, backgroundColor: theme.surface2, alignItems: "center", justifyContent: "center" },
  toolText: { color: theme.text, fontSize: 24 },

  grid: { flex: 1, flexDirection: "row", gap: 24 },
  gridPortrait: { flexDirection: "column", gap: 16 },
  col: { flex: 1, gap: 20 },
  colPortrait: { flex: 0, gap: 16 },

  tile: { borderRadius: 22, alignItems: "center", justifyContent: "center", gap: 10 },
  tileLand: { flex: 1 },
  tilePortrait: { height: 130, width: "100%", flexDirection: "row", gap: 18 },
  live: { flex: undefined, backgroundColor: "#2f7bff" },
  movies: { backgroundColor: "#e0245e" },
  series: { backgroundColor: "#7a3bff" },

  icon: { fontSize: 56 },
  iconPortrait: { fontSize: 40 },
  label: { color: "#fff", fontSize: 28, fontWeight: "800", letterSpacing: 1 },
  labelPortrait: { fontSize: 30 },

  pill: { backgroundColor: "#6db39a", borderRadius: 16, paddingVertical: 16, paddingHorizontal: 20, alignItems: "center" },
  pillText: { color: "#06251c", fontSize: 20, fontWeight: "800" },

  foot: { flexDirection: "row", justifyContent: "space-between", marginTop: 20, gap: 12 },
  footMuted: { color: theme.muted, fontSize: 18 },
  footName: { color: theme.text, fontSize: 18, fontWeight: "700", flexShrink: 1 },

  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.03 }] },
});
