import React, { useEffect, useState } from "react";
import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import type { Playlist } from "@tvapp/core";
import { theme } from "../theme";
import { loadPlaylists, removePlaylist } from "../storage";

/** Pantalla de inicio: lista de "Listas de reproducción" del usuario. */
export function HomeScreen({
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

  async function remove(id: string) {
    setPlaylists(await removePlaylist(id));
  }

  return (
    <View style={styles.container}>
      <View style={styles.head}>
        <Text style={styles.title}>Listas de reproducción</Text>
        <Pressable
          style={({ focused }) => [styles.addBtn, focused && styles.focused]}
          hasTVPreferredFocus
          onPress={onAdd}
        >
          <Text style={styles.addBtnText}>+ Nueva lista</Text>
        </Pressable>
      </View>

      {playlists.length === 0 ? (
        <Text style={styles.empty}>
          Aún no tienes listas. Crea una con tus credenciales M3U o Xtream.
        </Text>
      ) : (
        <FlatList
          data={playlists}
          keyExtractor={(p) => p.id}
          renderItem={({ item }) => (
            <View style={styles.row}>
              <Pressable
                style={({ focused }) => [styles.open, focused && styles.focused]}
                onPress={() => onOpen(item)}
              >
                <Text style={styles.rowName}>{item.name || item.url}</Text>
                <Text style={styles.rowKind}>{item.kind.toUpperCase()}</Text>
              </Pressable>
              <Pressable
                style={({ focused }) => [styles.del, focused && styles.focused]}
                onPress={() => remove(item.id)}
              >
                <Text style={styles.delText}>Eliminar</Text>
              </Pressable>
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 48 },
  head: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 28,
  },
  title: { color: theme.text, fontSize: 34, fontWeight: "800" },
  addBtn: {
    backgroundColor: theme.accent,
    paddingHorizontal: 26,
    paddingVertical: 14,
    borderRadius: 999,
  },
  addBtnText: { color: theme.text, fontSize: 22, fontWeight: "700" },
  empty: { color: theme.muted, fontSize: 22 },
  row: { flexDirection: "row", gap: 16, marginBottom: 16 },
  open: {
    flex: 1,
    backgroundColor: theme.surface,
    borderRadius: theme.radius,
    padding: 24,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  rowName: { color: theme.text, fontSize: 24, fontWeight: "600" },
  rowKind: { color: theme.muted, fontSize: 16, letterSpacing: 1 },
  del: {
    backgroundColor: theme.surface2,
    borderRadius: theme.radius,
    paddingHorizontal: 24,
    justifyContent: "center",
  },
  delText: { color: theme.text, fontSize: 20, fontWeight: "700" },
  focused: {
    borderWidth: 4,
    borderColor: "#fff",
    transform: [{ scale: 1.04 }],
  },
});
