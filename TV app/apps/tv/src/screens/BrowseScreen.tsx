import React, { useEffect, useState } from "react";
import { FlatList, Image, Pressable, StyleSheet, Text, View } from "react-native";
import {
  parseM3U,
  XtreamClient,
  fromPlaylist,
  type MediaItem,
  type Playlist,
  type PlaylistContent,
} from "@tvapp/core";
import { theme } from "../theme";

/** Descarga el contenido de una playlist (M3U o Xtream) reutilizando el núcleo. */
async function loadContent(p: Playlist): Promise<PlaylistContent> {
  if (p.kind === "m3u") {
    const res = await fetch(p.url);
    if (!res.ok) throw new Error(`No se pudo descargar la lista (${res.status})`);
    return parseM3U(await res.text());
  }
  return new XtreamClient(fromPlaylist(p)).loadLive();
}

/** Navegador de canales con filtro por categoría y rejilla de tarjetas. */
export function BrowseScreen({
  playlist,
  onBack,
  onPlay,
}: {
  playlist: Playlist;
  onBack: () => void;
  onPlay: (item: MediaItem) => void;
}) {
  const [content, setContent] = useState<PlaylistContent | null>(null);
  const [category, setCategory] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("Cargando contenido…");

  useEffect(() => {
    let alive = true;
    loadContent(playlist)
      .then((c) => {
        if (!alive) return;
        setContent(c);
        setStatus(c.items.length === 0 ? "La lista no trajo canales." : "");
      })
      .catch((err: unknown) => {
        if (!alive) return;
        setStatus(err instanceof Error ? err.message : "Error al cargar la lista");
      });
    return () => {
      alive = false;
    };
  }, [playlist]);

  const items = content
    ? category
      ? content.items.filter((i) => i.group === category)
      : content.items
    : [];

  return (
    <View style={styles.container}>
      <Pressable
        style={({ focused }) => [styles.back, focused && styles.focused]}
        hasTVPreferredFocus
        onPress={onBack}
      >
        <Text style={styles.backText}>← Listas</Text>
      </Pressable>

      {status ? <Text style={styles.status}>{status}</Text> : null}

      {content && (
        <View style={styles.body}>
          <View style={styles.cats}>
            <CategoryChip
              label="Todos"
              active={category === null}
              onPress={() => setCategory(null)}
            />
            {content.categories.map((c) => (
              <CategoryChip
                key={c.id}
                label={c.name}
                active={category === c.id}
                onPress={() => setCategory(c.id)}
              />
            ))}
          </View>

          <FlatList
            style={styles.grid}
            data={items}
            keyExtractor={(i) => i.id}
            numColumns={4}
            columnWrapperStyle={styles.gridRow}
            renderItem={({ item }) => (
              <Pressable
                style={({ focused }) => [styles.card, focused && styles.focused]}
                onPress={() => onPlay(item)}
              >
                {item.logo ? (
                  <Image style={styles.logo} source={{ uri: item.logo }} resizeMode="contain" />
                ) : (
                  <View style={[styles.logo, styles.logoPh]}>
                    <Text style={styles.logoPhText}>{item.title.slice(0, 2).toUpperCase()}</Text>
                  </View>
                )}
                <Text style={styles.cardTitle} numberOfLines={1}>
                  {item.title}
                </Text>
              </Pressable>
            )}
          />
        </View>
      )}
    </View>
  );
}

function CategoryChip({
  label,
  active,
  onPress,
}: {
  label: string;
  active: boolean;
  onPress: () => void;
}) {
  return (
    <Pressable
      style={({ focused }) => [styles.chip, active && styles.chipActive, focused && styles.focused]}
      onPress={onPress}
    >
      <Text style={styles.chipText} numberOfLines={1}>
        {label}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 40 },
  back: {
    alignSelf: "flex-start",
    backgroundColor: theme.surface2,
    borderRadius: 999,
    paddingHorizontal: 22,
    paddingVertical: 12,
    marginBottom: 16,
  },
  backText: { color: theme.text, fontSize: 20, fontWeight: "700" },
  status: { color: theme.muted, fontSize: 22 },
  body: { flex: 1, flexDirection: "row", gap: 24 },
  cats: { width: 260 },
  chip: {
    backgroundColor: theme.surface,
    borderRadius: 12,
    paddingHorizontal: 20,
    paddingVertical: 14,
    marginBottom: 8,
  },
  chipActive: { backgroundColor: theme.accent },
  chipText: { color: theme.text, fontSize: 20 },
  grid: { flex: 1 },
  gridRow: { gap: 20, marginBottom: 20 },
  card: {
    flex: 1,
    backgroundColor: theme.surface,
    borderRadius: theme.radius,
    padding: 16,
    alignItems: "center",
  },
  logo: { width: "100%", height: 120, borderRadius: 8 },
  logoPh: { backgroundColor: theme.surface2, alignItems: "center", justifyContent: "center" },
  logoPhText: { color: theme.muted, fontSize: 40, fontWeight: "800" },
  cardTitle: { color: theme.text, fontSize: 18, marginTop: 12 },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.04 }] },
});
