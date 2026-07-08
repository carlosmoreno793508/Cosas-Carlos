import React, { useEffect, useState } from "react";
import { FlatList, Image, Pressable, StyleSheet, Text, View } from "react-native";
import {
  XtreamClient,
  fromPlaylist,
  type MediaItem,
  type Playlist,
  type SeriesDetail,
} from "@tvapp/core";
import { theme } from "../theme";

/** Detalle de serie: temporadas + episodios reproducibles (get_series_info). */
export function SeriesScreen({
  playlist,
  series,
  onPlayEpisode,
  onBack,
}: {
  playlist: Playlist;
  series: MediaItem;
  onPlayEpisode: (src: string, title: string) => void;
  onBack: () => void;
}) {
  const [detail, setDetail] = useState<SeriesDetail | null>(null);
  const [season, setSeason] = useState<number | null>(null);
  const [status, setStatus] = useState("Cargando episodios…");

  useEffect(() => {
    let alive = true;
    if (playlist.kind !== "xtream") {
      setStatus("Las series solo están disponibles en fuentes Xtream.");
      return;
    }
    const seriesId = series.extra?.seriesId ?? series.id.replace(/^series-/, "");
    new XtreamClient(fromPlaylist(playlist))
      .getSeriesInfo(seriesId)
      .then((d) => {
        if (!alive) return;
        setDetail(d);
        setSeason(d.seasons[0]?.season ?? null);
        setStatus(d.seasons.length === 0 ? "Esta serie no tiene episodios." : "");
      })
      .catch((err: unknown) => {
        if (!alive) return;
        setStatus(err instanceof Error ? err.message : "Error al cargar la serie");
      });
    return () => {
      alive = false;
    };
  }, [playlist, series]);

  const current = detail?.seasons.find((s) => s.season === season);

  return (
    <View style={styles.container}>
      <View style={styles.head}>
        <Pressable hasTVPreferredFocus style={({ focused }) => [styles.back, focused && styles.focused]} onPress={onBack}>
          <Text style={styles.backText}>‹</Text>
        </Pressable>
        {series.logo ? (
          <Image style={styles.cover} source={{ uri: series.logo }} resizeMode="cover" />
        ) : (
          <View style={[styles.cover, styles.ph]}>
            <Text style={styles.phText}>{series.title.slice(0, 2).toUpperCase()}</Text>
          </View>
        )}
        <View style={styles.meta}>
          <Text style={styles.title}>{detail?.name || series.title}</Text>
          {series.rating ? <Text style={styles.rating}>★ {series.rating.toFixed(1)}</Text> : null}
          {detail?.plot ? <Text style={styles.plot}>{detail.plot}</Text> : null}
        </View>
      </View>

      {status ? <Text style={styles.status}>{status}</Text> : null}

      {detail && detail.seasons.length > 0 ? (
        <>
          <View style={styles.seasons}>
            {detail.seasons.map((s) => (
              <Pressable
                key={s.season}
                style={({ focused }) => [styles.chip, s.season === season && styles.chipActive, focused && styles.focused]}
                onPress={() => setSeason(s.season)}
              >
                <Text style={styles.chipText}>Temporada {s.season}</Text>
              </Pressable>
            ))}
          </View>
          <FlatList
            data={current?.episodes ?? []}
            keyExtractor={(e) => e.id}
            renderItem={({ item: ep }) => (
              <Pressable
                style={({ focused }) => [styles.episode, focused && styles.focused]}
                onPress={() => onPlayEpisode(ep.streamUrl, ep.title)}
              >
                <View style={styles.epNum}>
                  <Text style={styles.epNumText}>{ep.episodeNum ?? "▶"}</Text>
                </View>
                <Text style={styles.epTitle}>{ep.title}</Text>
              </Pressable>
            )}
          />
        </>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 48 },
  head: { flexDirection: "row", gap: 28, marginBottom: 24 },
  back: { width: 48, height: 48, borderRadius: 12, backgroundColor: theme.surface2, alignItems: "center", justifyContent: "center" },
  backText: { color: theme.text, fontSize: 26 },
  cover: { width: 200, aspectRatio: 2 / 3, borderRadius: 16, backgroundColor: theme.surface2 },
  ph: { alignItems: "center", justifyContent: "center" },
  phText: { color: theme.muted, fontSize: 40, fontWeight: "800" },
  meta: { flex: 1 },
  title: { color: theme.text, fontSize: 34, fontWeight: "800", marginBottom: 10 },
  rating: { color: "#ffd24c", fontWeight: "800", fontSize: 22 },
  plot: { color: theme.muted, fontSize: 20, marginTop: 12 },
  status: { color: theme.muted, fontSize: 20 },
  seasons: { flexDirection: "row", gap: 12, flexWrap: "wrap", marginBottom: 20 },
  chip: { backgroundColor: theme.surface2, borderRadius: 999, paddingVertical: 12, paddingHorizontal: 22 },
  chipActive: { backgroundColor: theme.accent },
  chipText: { color: theme.text, fontSize: 19, fontWeight: "600" },
  episode: { flexDirection: "row", alignItems: "center", gap: 20, backgroundColor: theme.surface, borderRadius: 14, padding: 20, marginBottom: 12 },
  epNum: { minWidth: 42, height: 42, borderRadius: 10, backgroundColor: theme.surface2, alignItems: "center", justifyContent: "center" },
  epNumText: { color: theme.text, fontWeight: "800", fontSize: 20 },
  epTitle: { color: theme.text, fontSize: 22 },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.02 }] },
});
