import React, { useCallback, useEffect, useState } from "react";
import { StatusBar, StyleSheet, View, useTVEventHandler } from "react-native";
import type { MediaItem, Playlist } from "@tvapp/core";
import { theme } from "./theme";
import { HomeScreen } from "./screens/HomeScreen";
import { FormScreen } from "./screens/FormScreen";
import { BrowseScreen } from "./screens/BrowseScreen";
import { PlayerScreen } from "./screens/PlayerScreen";

type View_ =
  | { screen: "home" }
  | { screen: "form" }
  | { screen: "browse"; playlist: Playlist }
  | { screen: "play"; item: MediaItem; playlist: Playlist };

/**
 * Raíz de la app de TV. Navegación por estado (sin librería de routing para
 * mantener el árbol simple) y manejo del botón "Atrás"/"Menu" del control con
 * useTVEventHandler, que funciona igual en Fire TV, Android TV y Apple TV.
 */
export function App() {
  const [view, setView] = useState<View_>({ screen: "home" });

  const goBack = useCallback(() => {
    setView((v) => {
      if (v.screen === "play") return { screen: "browse", playlist: v.playlist };
      if (v.screen === "browse" || v.screen === "form") return { screen: "home" };
      return v;
    });
  }, []);

  // El evento "menu" (Apple TV) y el "back" de Android/Fire llegan aquí.
  useTVEventHandler((evt) => {
    if (evt && (evt.eventType === "menu" || evt.eventType === "back")) {
      goBack();
    }
  });

  return (
    <View style={styles.root}>
      <StatusBar hidden />
      {view.screen === "home" && (
        <HomeScreen
          onAdd={() => setView({ screen: "form" })}
          onOpen={(playlist) => setView({ screen: "browse", playlist })}
        />
      )}
      {view.screen === "form" && (
        <FormScreen
          onCancel={() => setView({ screen: "home" })}
          onCreated={() => setView({ screen: "home" })}
        />
      )}
      {view.screen === "browse" && (
        <BrowseScreen
          playlist={view.playlist}
          onBack={() => setView({ screen: "home" })}
          onPlay={(item) => setView({ screen: "play", item, playlist: view.playlist })}
        />
      )}
      {view.screen === "play" && (
        <PlayerScreen item={view.item} onBack={goBack} />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: theme.bg },
});
