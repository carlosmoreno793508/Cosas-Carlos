import React, { useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import type { Playlist } from "@tvapp/core";
import { theme } from "../theme";
import { loadPlaylists, removePlaylist } from "../storage";

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
          <View key={p.id} style={styles.wrap}>
            <Pressable
              hasTVPreferredFocus={i === 0}
              style={({ focused }) => [styles.profile, focused && styles.focused]}
              onPress={() => onOpen(p)}
            >
              {p.pin ? <Text style={styles.lock}>🔒</Text> : null}
              <Avatar color={i % 2 === 0 ? theme.accent2 : "#8b3bff"} />
              <Text style={styles.name}>{p.name || p.url}</Text>
            </Pressable>
            <Pressable
              style={({ focused }) => [styles.del, focused && styles.focused]}
              onPress={async () => setPlaylists(await removePlaylist(p.id))}
            >
              <Text style={styles.delText}>🗑 Borrar</Text>
            </Pressable>
          </View>
        ))}
        <View style={styles.wrap}>
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
    </View>
  );
}

function Avatar({ color }: { color: string }) {
  // Avatar con vistas nativas (sin react-native-svg): cabeza (círculo) + cuerpo
  // (media luna con esquinas superiores redondeadas).
  return (
    <View style={styles.avatar}>
      <View style={styles.avatarHead} />
      <View style={[styles.avatarBody, { backgroundColor: color }]} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 48, alignItems: "center" },
  top: { width: "100%", flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  brand: { color: theme.text, fontSize: 34, fontWeight: "800" },
  accent: { color: theme.accent2 },
  ver: { color: theme.muted, fontSize: 18 },
  title: { color: theme.text, fontSize: 34, fontWeight: "800", letterSpacing: 2, marginVertical: 44 },
  profiles: { flexDirection: "row", gap: 40, flexWrap: "wrap", justifyContent: "center", alignItems: "flex-start" },
  wrap: { alignItems: "center", gap: 12 },
  del: { backgroundColor: theme.surface2, borderRadius: 999, paddingHorizontal: 22, paddingVertical: 10 },
  delText: { color: theme.danger, fontSize: 18, fontWeight: "700" },
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
  avatar: { width: 120, height: 120, alignItems: "center", justifyContent: "flex-end" },
  avatarHead: { width: 52, height: 52, borderRadius: 26, backgroundColor: "#f0b48f", marginBottom: 4 },
  avatarBody: { width: 84, height: 44, borderTopLeftRadius: 42, borderTopRightRadius: 42 },
  plus: { color: "#aebbe0", fontSize: 96, fontWeight: "300" },
  lock: { position: "absolute", top: 14, right: 16, fontSize: 26 },
  name: { color: "#fff", fontSize: 24, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.04 }] },
});
