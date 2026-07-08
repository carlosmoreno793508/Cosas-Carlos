import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import type { Playlist } from "@tvapp/core";
import { theme } from "../theme";

/** Pantalla simple de cuenta / datos de la lista activa. */
export function AccountScreen({ playlist, onBack }: { playlist: Playlist; onBack: () => void }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Cuenta</Text>
      <Text style={styles.row}>Lista: {playlist.name || playlist.url}</Text>
      <Text style={styles.row}>Tipo: {playlist.kind.toUpperCase()}</Text>
      {playlist.username ? <Text style={styles.row}>Usuario: {playlist.username}</Text> : null}
      <Pressable hasTVPreferredFocus style={({ focused }) => [styles.btn, focused && styles.focused]} onPress={onBack}>
        <Text style={styles.btnText}>‹ Volver</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 48, gap: 12 },
  title: { color: theme.text, fontSize: 34, fontWeight: "800", marginBottom: 12 },
  row: { color: theme.text, fontSize: 22 },
  btn: { alignSelf: "flex-start", marginTop: 20, backgroundColor: theme.surface2, borderRadius: 999, paddingHorizontal: 26, paddingVertical: 14 },
  btnText: { color: theme.text, fontSize: 22, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.04 }] },
});
