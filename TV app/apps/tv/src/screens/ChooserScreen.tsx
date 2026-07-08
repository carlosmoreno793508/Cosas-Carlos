import React, { useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import Svg, { Circle, Path } from "react-native-svg";
import type { Playlist } from "@tvapp/core";
import { theme } from "../theme";
import { loadPlaylists } from "../storage";

/** Selector de listas tipo perfil (equivalente a "CHOOSE YOUR PLAYLIST"). */
export function ChooserScreen({
  onAdd,
  onOpen,
}: {
  onAdd: () => void;
  onOpen: (p: Playlist) => void;
}) {
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  useEffect(() => {
    loadPlaylists().then(setPlaylists);
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.top}>
        <Text style={styles.brand}>
          More<Text style={styles.accent}>TV</Text>
        </Text>
        <Text style={styles.ver}>v0.1</Text>
      </View>

      <Text style={styles.title}>ELIGE TU LISTA</Text>

      <View style={styles.profiles}>
        {playlists.map((p, i) => (
          <Pressable
            key={p.id}
            hasTVPreferredFocus={i === 0}
            style={({ focused }) => [styles.profile, focused && styles.focused]}
            onPress={() => onOpen(p)}
          >
            {p.pin ? <Text style={styles.lock}>🔒</Text> : null}
            <Avatar color={i % 2 === 0 ? theme.accent2 : "#8b3bff"} />
            <Text style={styles.name}>{p.name || p.url}</Text>
          </Pressable>
        ))}
        <Pressable
          hasTVPreferredFocus={playlists.length === 0}
          style={({ focused }) => [styles.profile, styles.add, focused && styles.focused]}
          onPress={onAdd}
        >
          <Text style={styles.plus}>+</Text>
          <Text style={styles.name}>Añadir lista</Text>
        </Pressable>
      </View>
    </View>
  );
}

function Avatar({ color }: { color: string }) {
  return (
    <Svg viewBox="0 0 100 100" width={120} height={120}>
      <Circle cx={50} cy={38} r={22} fill="#f0b48f" />
      <Path d="M18 92c0-20 14-30 32-30s32 10 32 30z" fill={color} />
    </Svg>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 48, alignItems: "center" },
  top: { width: "100%", flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  brand: { color: theme.text, fontSize: 34, fontWeight: "800" },
  accent: { color: theme.accent2 },
  ver: { color: theme.muted, fontSize: 18 },
  title: { color: theme.text, fontSize: 34, fontWeight: "800", letterSpacing: 2, marginVertical: 44 },
  profiles: { flexDirection: "row", gap: 40, flexWrap: "wrap", justifyContent: "center" },
  profile: {
    width: 300,
    height: 320,
    borderRadius: 20,
    backgroundColor: "#6a6f7a",
    alignItems: "center",
    justifyContent: "flex-end",
    paddingBottom: 24,
    gap: 20,
  },
  add: { backgroundColor: "#23304d", justifyContent: "center" },
  plus: { color: "#aebbe0", fontSize: 96, fontWeight: "300" },
  lock: { position: "absolute", top: 14, right: 16, fontSize: 26 },
  name: { color: "#fff", fontSize: 24, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.04 }] },
});
