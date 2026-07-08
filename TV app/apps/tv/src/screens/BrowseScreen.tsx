import React, { useEffect, useMemo, useState } from "react";
import { FlatList, Image, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import {
  XtreamClient,
  fromPlaylist,
  parseM3U,
  type MediaItem,
  type Playlist,
  type PlaylistContent,
} from "@tvapp/core";
import { theme } from "../theme";
import type { Section } from "./DashboardScreen";

const RECENT = "__recent__";
const TITLES: Record<Section, string> = { live: "TV en vivo", movie: "Películas", series: "Series" };

async function loadSection(p: Playlist, section: Section): Promise<PlaylistContent> {
  if (p.kind === "m3u") {
    const res = await fetch(p.url);
    if (!res.ok) throw new Error(`No se pudo descargar la lista (${res.status})`);
    return parseM3U(await res.text());
  }
  const client = new XtreamClient(fromPlaylist(p));
  if (section === "movie") return client.loadMovies();
  if (section === "series") return client.loadSeries();
  return client.loadLive();
}

/** Navegador con barra lateral de categorías (contadores + buscador) y rejilla. */
export function BrowseScreen({
  playlist,
  section,
  onSelect,
  onBack,
}: {
  playlist: Playlist;
  section: Section;
  onSelect: (item: MediaItem) => void;
  onBack: () => void;
}) {
  const [content, setContent] = useState<PlaylistContent | null>(null);
  const [category, setCategory] = useState<string | null>(null);
  const [status, setStatus] = useState("Cargando…");
  const [query, setQuery] = useState("");
  const [nonce, setNonce] = useState(0);

  useEffect(() => {
    let alive = true;
    loadSection(playlist, section)
      .then((c) => {
        if (!alive) return;
        setContent(c);
        setStatus(c.items.length === 0 ? "Sin contenido en esta sección." : "");
      })
      .catch((err: unknown) => {
        if (!alive) return;
        setStatus(err instanceof Error ? err.message : "Error al cargar");
      });
    return () => {
      alive = false;
    };
  }, [playlist, section, nonce]);

  // Auto-refresco cada 10 minutos.
  useEffect(() => {
    const t = setInterval(() => setNonce((n) => n + 1), 10 * 60 * 1000);
    return () => clearInterval(t);
  }, []);

  const recent = useMemo(
    () =>
      content
        ? [...content.items].filter((i) => i.addedAt).sort((a, b) => (b.addedAt ?? 0) - (a.addedAt ?? 0)).slice(0, 60)
        : [],
    [content],
  );

  const cats = useMemo(() => {
    const list = content?.categories ?? [];
    if (!query.trim()) return list;
    const q = query.toLowerCase();
    return list.filter((c) => c.name.toLowerCase().includes(q));
  }, [content, query]);

  const items = content
    ? category === RECENT
      ? recent
      : category
        ? content.items.filter((i) => i.group === category)
        : content.items
    : [];

  const isVod = section !== "live";

  return (
    <View style={styles.container}>
      <View style={styles.side}>
        <View style={styles.sideHead}>
          <Pressable style={({ focused }) => [styles.back, focused && styles.focused]} onPress={onBack}>
            <Text style={styles.backText}>‹</Text>
          </Pressable>
          <Text style={styles.brand}>
            More<Text style={styles.accent}>TV</Text>
          </Text>
        </View>
        <TextInput
          style={styles.search}
          placeholder="Buscar en categorías"
          placeholderTextColor={theme.muted}
          value={query}
          onChangeText={setQuery}
        />
        <FlatList
          data={[{ id: null, name: "ALL", count: content?.items.length ?? 0 } as never].concat(
            recent.length ? [{ id: RECENT, name: "🆕 Recién agregado", count: recent.length } as never] : [],
            cats as never[],
          )}
          keyExtractor={(c: { id: string | null }, i) => c.id ?? `all-${i}`}
          renderItem={({ item: c }: { item: { id: string | null; name: string; count?: number } }) => (
            <Pressable
              style={({ focused }) => [
                styles.cat,
                category === c.id && styles.catActive,
                focused && styles.focused,
              ]}
              onPress={() => setCategory(c.id)}
            >
              <Text style={styles.catName} numberOfLines={1}>{c.name}</Text>
              <Text style={styles.catCount}>{c.count ?? 0}</Text>
            </Pressable>
          )}
        />
      </View>

      <View style={styles.content}>
        <View style={styles.contentHead}>
          <Text style={styles.contentTitle}>{TITLES[section]}</Text>
          <Pressable
            style={({ focused }) => [styles.refresh, focused && styles.focused]}
            onPress={() => setNonce((n) => n + 1)}
          >
            <Text style={styles.refreshText}>⟳</Text>
          </Pressable>
        </View>
        {status ? <Text style={styles.status}>{status}</Text> : null}
        <FlatList
          data={items.slice(0, 120)}
          key={isVod ? "vod" : "live"}
          numColumns={isVod ? 5 : 4}
          keyExtractor={(i) => i.id}
          columnWrapperStyle={styles.row}
          renderItem={({ item }) => (
            <Pressable
              style={({ focused }) => [isVod ? styles.poster : styles.logoCard, focused && styles.focused]}
              onPress={() => onSelect(item)}
            >
              {item.logo ? (
                <Image
                  style={isVod ? styles.posterImg : styles.logoImg}
                  source={{ uri: item.logo }}
                  resizeMode={isVod ? "cover" : "contain"}
                />
              ) : (
                <View style={[isVod ? styles.posterImg : styles.logoImg, styles.ph]}>
                  <Text style={styles.phText}>{item.title.slice(0, 2).toUpperCase()}</Text>
                </View>
              )}
              {isVod && item.rating ? <Text style={styles.badge}>{item.rating.toFixed(1)}</Text> : null}
              <Text style={styles.cardTitle} numberOfLines={1}>{item.title}</Text>
            </Pressable>
          )}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, flexDirection: "row" },
  side: { width: 420, backgroundColor: "#05070d", padding: 24, gap: 16 },
  sideHead: { flexDirection: "row", alignItems: "center", gap: 16 },
  back: { width: 48, height: 48, borderRadius: 12, backgroundColor: theme.surface2, alignItems: "center", justifyContent: "center" },
  backText: { color: theme.text, fontSize: 26 },
  brand: { color: theme.text, fontSize: 26, fontWeight: "800" },
  accent: { color: theme.accent2 },
  search: { backgroundColor: theme.surface2, borderRadius: 14, padding: 16, color: theme.text, fontSize: 20 },
  cat: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 18,
    paddingHorizontal: 12,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(255,255,255,0.06)",
  },
  catActive: { backgroundColor: "#1f5b6b" },
  catName: { color: theme.text, fontSize: 20, flex: 1, marginRight: 8 },
  catCount: { color: theme.muted, fontSize: 17 },
  content: { flex: 1, padding: 28 },
  contentHead: { flexDirection: "row", alignItems: "center", justifyContent: "center", gap: 20, marginBottom: 20 },
  contentTitle: { color: theme.text, fontSize: 30, fontWeight: "800" },
  refresh: { width: 46, height: 46, borderRadius: 23, backgroundColor: theme.surface2, alignItems: "center", justifyContent: "center" },
  refreshText: { color: theme.text, fontSize: 22 },
  status: { color: theme.muted, fontSize: 20, textAlign: "center" },
  row: { gap: 18, marginBottom: 18 },
  logoCard: { flex: 1, gap: 8 },
  logoImg: { width: "100%", aspectRatio: 1, borderRadius: 12, backgroundColor: "#fff", padding: 8 },
  poster: { flex: 1, gap: 8 },
  posterImg: { width: "100%", aspectRatio: 2 / 3, borderRadius: 12, backgroundColor: theme.surface2 },
  ph: { alignItems: "center", justifyContent: "center" },
  phText: { color: theme.muted, fontSize: 30, fontWeight: "800" },
  badge: { position: "absolute", top: 8, left: 8, backgroundColor: "rgba(0,0,0,0.75)", color: "#ffd24c", fontWeight: "800", fontSize: 14, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8 },
  cardTitle: { color: theme.text, fontSize: 16, textAlign: "center" },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.04 }] },
});
