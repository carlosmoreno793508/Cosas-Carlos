import React, { useEffect, useMemo, useState } from "react";
import { FlatList, Image, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import {
  XtreamClient,
  fromPlaylist,
  parseM3U,
  type MediaItem,
  type Playlist,
} from "@tvapp/core";
import { theme } from "../theme";

async function loadAll(p: Playlist): Promise<MediaItem[]> {
  if (p.kind === "m3u") {
    const res = await fetch(p.url);
    if (!res.ok) throw new Error(`No se pudo descargar la lista (${res.status})`);
    return parseM3U(await res.text()).items;
  }
  const client = new XtreamClient(fromPlaylist(p));
  const [live, movies, series] = await Promise.all([
    client.getLiveStreams(),
    client.getMovies(),
    client.getSeries(),
  ]);
  return [...live, ...movies, ...series];
}

const KIND: Record<string, string> = { live: "TV", movie: "Película", series: "Serie" };

/** Buscador global: filtra por título en canales, películas y series. */
export function SearchScreen({
  playlist,
  onSelect,
  onBack,
}: {
  playlist: Playlist;
  onSelect: (item: MediaItem) => void;
  onBack: () => void;
}) {
  const [all, setAll] = useState<MediaItem[] | null>(null);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("Cargando catálogo…");

  useEffect(() => {
    let alive = true;
    loadAll(playlist)
      .then((items) => {
        if (!alive) return;
        setAll(items);
        setStatus("");
      })
      .catch((err: unknown) => {
        if (!alive) return;
        setStatus(err instanceof Error ? err.message : "Error al cargar");
      });
    return () => {
      alive = false;
    };
  }, [playlist]);

  const results = useMemo(() => {
    if (!all || query.trim().length < 2) return [];
    const q = query.toLowerCase();
    return all.filter((i) => i.title.toLowerCase().includes(q)).slice(0, 120);
  }, [all, query]);

  return (
    <View style={styles.container}>
      <View style={styles.bar}>
        <Pressable style={({ focused }) => [styles.back, focused && styles.focused]} onPress={onBack}>
          <Text style={styles.backText}>‹</Text>
        </Pressable>
        <TextInput
          style={styles.input}
          autoFocus
          placeholder="Buscar películas, series o canales…"
          placeholderTextColor={theme.muted}
          value={query}
          onChangeText={setQuery}
        />
      </View>

      {status ? <Text style={styles.status}>{status}</Text> : null}
      {!status && query.trim().length < 2 ? (
        <Text style={styles.status}>Escribe al menos 2 letras para buscar.</Text>
      ) : null}

      <FlatList
        data={results}
        numColumns={5}
        keyExtractor={(i) => `${i.type}-${i.id}`}
        columnWrapperStyle={styles.row}
        renderItem={({ item }) => (
          <Pressable style={({ focused }) => [styles.poster, focused && styles.focused]} onPress={() => onSelect(item)}>
            {item.logo ? (
              <Image style={styles.img} source={{ uri: item.logo }} resizeMode="cover" />
            ) : (
              <View style={[styles.img, styles.ph]}>
                <Text style={styles.phText}>{item.title.slice(0, 2).toUpperCase()}</Text>
              </View>
            )}
            <Text style={styles.kind}>{KIND[item.type]}</Text>
            <Text style={styles.title} numberOfLines={1}>{item.title}</Text>
          </Pressable>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 40 },
  bar: { flexDirection: "row", gap: 16, alignItems: "center", marginBottom: 24 },
  back: { width: 48, height: 48, borderRadius: 12, backgroundColor: theme.surface2, alignItems: "center", justifyContent: "center" },
  backText: { color: theme.text, fontSize: 26 },
  input: { flex: 1, backgroundColor: theme.surface, borderRadius: 16, padding: 18, color: theme.text, fontSize: 24 },
  status: { color: theme.muted, fontSize: 20 },
  row: { gap: 18, marginBottom: 18 },
  poster: { flex: 1, gap: 6 },
  img: { width: "100%", aspectRatio: 2 / 3, borderRadius: 12, backgroundColor: theme.surface2 },
  ph: { alignItems: "center", justifyContent: "center" },
  phText: { color: theme.muted, fontSize: 30, fontWeight: "800" },
  kind: { color: theme.muted, fontSize: 12, textTransform: "uppercase" },
  title: { color: theme.text, fontSize: 16 },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.04 }] },
});
