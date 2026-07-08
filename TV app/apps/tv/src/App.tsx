import React, { useCallback, useState } from "react";
import { StatusBar, StyleSheet, View, useTVEventHandler } from "react-native";
import type { MediaItem, Playlist } from "@tvapp/core";
import { theme } from "./theme";
import { ChooserScreen } from "./screens/ChooserScreen";
import { FormScreen } from "./screens/FormScreen";
import { DashboardScreen, type Section } from "./screens/DashboardScreen";
import { BrowseScreen } from "./screens/BrowseScreen";
import { SeriesScreen } from "./screens/SeriesScreen";
import { AccountScreen } from "./screens/AccountScreen";
import { SearchScreen } from "./screens/SearchScreen";
import { PlayerScreen } from "./screens/PlayerScreen";

type View_ =
  | { screen: "home" }
  | { screen: "form" }
  | { screen: "dashboard"; playlist: Playlist }
  | { screen: "account"; playlist: Playlist }
  | { screen: "search"; playlist: Playlist }
  | { screen: "browse"; playlist: Playlist; section: Section }
  | { screen: "series"; playlist: Playlist; series: MediaItem }
  | { screen: "play"; src: string; title: string; playlist: Playlist; item?: MediaItem; back: View_ };

/**
 * Raíz de la app de TV, con el mismo flujo que la web: selector de listas →
 * dashboard (LIVE/MOVIES/SERIES) → navegador → detalle de serie → reproductor.
 * El botón Atrás/Menu del control se maneja con useTVEventHandler.
 */
export function App() {
  const [view, setView] = useState<View_>({ screen: "home" });

  const goBack = useCallback(() => {
    setView((v) => {
      switch (v.screen) {
        case "play":
          return v.back;
        case "series":
          return { screen: "browse", playlist: v.playlist, section: "series" };
        case "browse":
        case "account":
        case "search":
          return { screen: "dashboard", playlist: v.playlist };
        case "dashboard":
        case "form":
          return { screen: "home" };
        default:
          return v;
      }
    });
  }, []);

  useTVEventHandler((evt) => {
    if (evt && (evt.eventType === "menu" || evt.eventType === "back")) goBack();
  });

  return (
    <View style={styles.root}>
      <StatusBar hidden />
      {view.screen === "home" && (
        <ChooserScreen
          onAdd={() => setView({ screen: "form" })}
          onOpen={(playlist) => setView({ screen: "dashboard", playlist })}
        />
      )}
      {view.screen === "form" && (
        <FormScreen
          onCancel={() => setView({ screen: "home" })}
          onCreated={(playlist) => setView({ screen: "dashboard", playlist })}
        />
      )}
      {view.screen === "dashboard" && (
        <DashboardScreen
          playlist={view.playlist}
          onOpenSection={(section) => setView({ screen: "browse", playlist: view.playlist, section })}
          onAccount={() => setView({ screen: "account", playlist: view.playlist })}
          onSearch={() => setView({ screen: "search", playlist: view.playlist })}
        />
      )}
      {view.screen === "search" && (
        <SearchScreen
          playlist={view.playlist}
          onBack={goBack}
          onSelect={(item) => {
            if (item.type === "series") {
              setView({ screen: "series", playlist: view.playlist, series: item });
            } else {
              setView({ screen: "play", src: item.streamUrl, title: item.title, playlist: view.playlist, item, back: view });
            }
          }}
        />
      )}
      {view.screen === "account" && (
        <AccountScreen playlist={view.playlist} onBack={goBack} />
      )}
      {view.screen === "browse" && (
        <BrowseScreen
          playlist={view.playlist}
          section={view.section}
          onBack={goBack}
          onSelect={(item) => {
            if (item.type === "series") {
              setView({ screen: "series", playlist: view.playlist, series: item });
            } else {
              setView({ screen: "play", src: item.streamUrl, title: item.title, playlist: view.playlist, item, back: view });
            }
          }}
        />
      )}
      {view.screen === "series" && (
        <SeriesScreen
          playlist={view.playlist}
          series={view.series}
          onBack={goBack}
          onPlayEpisode={(src, title, episodeId) =>
            setView({
              screen: "play",
              src,
              title,
              playlist: view.playlist,
              item: { id: `ep-${episodeId}`, type: "movie", title, streamUrl: src },
              back: view,
            })
          }
        />
      )}
      {view.screen === "play" && (
        <PlayerScreen src={view.src} title={view.title} playlistId={view.playlist.id} item={view.item} onBack={goBack} />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: theme.bg },
});
