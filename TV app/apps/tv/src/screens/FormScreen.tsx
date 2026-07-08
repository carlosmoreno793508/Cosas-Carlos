import React, { useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import type { PlaylistKind } from "@tvapp/core";
import { theme } from "../theme";
import { addPlaylist, newId } from "../storage";

/** Formulario "Nueva lista de reproducción" (M3U o Xtream), como en la web. */
export function FormScreen({
  onCancel,
  onCreated,
}: {
  onCancel: () => void;
  onCreated: () => void;
}) {
  const [kind, setKind] = useState<PlaylistKind>("xtream");
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    if (!url.trim()) return setError("La URL es obligatoria");
    if (kind === "xtream" && (!username.trim() || !password.trim())) {
      return setError("Xtream requiere usuario y contraseña");
    }
    await addPlaylist({
      id: newId(),
      kind,
      name: name.trim() || undefined,
      url: url.trim(),
      username: kind === "xtream" ? username.trim() : undefined,
      password: kind === "xtream" ? password.trim() : undefined,
      createdAt: Date.now(),
    });
    onCreated();
  }

  return (
    <ScrollView contentContainerStyle={styles.sheet}>
      <Text style={styles.title}>Nueva lista de reproducción</Text>

      <View style={styles.segmented}>
        {(["m3u", "xtream"] as PlaylistKind[]).map((k) => (
          <Pressable
            key={k}
            style={({ focused }) => [
              styles.segBtn,
              kind === k && styles.segActive,
              focused && styles.focused,
            ]}
            onPress={() => setKind(k)}
          >
            <Text style={styles.segText}>{k === "m3u" ? "M3U" : "Xtream"}</Text>
          </Pressable>
        ))}
      </View>

      <Field label="Nombre (opcional)" value={name} onChange={setName} />
      <Field
        label={kind === "m3u" ? "URL del archivo M3U" : "URL"}
        value={url}
        onChange={setUrl}
        placeholder={kind === "m3u" ? "https://.../lista.m3u" : "https://portal.com:8080"}
      />
      {kind === "xtream" && (
        <>
          <Field label="Nombre de usuario" value={username} onChange={setUsername} />
          <Field label="Contraseña" value={password} onChange={setPassword} secure />
        </>
      )}

      {error && <Text style={styles.error}>{error}</Text>}
      <Text style={styles.note}>
        Estos datos se guardan solo en este dispositivo. Usa fuentes de contenido
        para las que tengas derechos.
      </Text>

      <View style={styles.actions}>
        <Pressable
          style={({ focused }) => [styles.btnGhost, focused && styles.focused]}
          onPress={onCancel}
        >
          <Text style={styles.btnText}>Cancelar</Text>
        </Pressable>
        <Pressable
          style={({ focused }) => [styles.btnPrimary, focused && styles.focused]}
          onPress={submit}
        >
          <Text style={styles.btnText}>Crear lista de reproducción</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
  secure,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  secure?: boolean;
}) {
  return (
    <View style={styles.field}>
      <Text style={styles.fieldLabel}>{label}</Text>
      <TextInput
        style={styles.input}
        value={value}
        onChangeText={onChange}
        placeholder={placeholder}
        placeholderTextColor={theme.muted}
        secureTextEntry={secure}
        autoCapitalize="none"
        autoCorrect={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  sheet: { padding: 48, maxWidth: 1000, alignSelf: "center", width: "100%" },
  title: { color: theme.text, fontSize: 30, fontWeight: "800", textAlign: "center", marginBottom: 28 },
  segmented: { flexDirection: "row", backgroundColor: theme.surface2, borderRadius: 999, padding: 6, marginBottom: 28 },
  segBtn: { flex: 1, paddingVertical: 14, borderRadius: 999, alignItems: "center" },
  segActive: { backgroundColor: theme.accent },
  segText: { color: theme.text, fontSize: 22, fontWeight: "700" },
  field: { marginBottom: 22 },
  fieldLabel: { color: theme.muted, fontSize: 18, marginBottom: 8 },
  input: {
    color: theme.text,
    fontSize: 24,
    borderBottomWidth: 2,
    borderBottomColor: theme.surface2,
    paddingVertical: 8,
  },
  error: { color: theme.danger, fontSize: 20, fontWeight: "600", marginBottom: 8 },
  note: { color: theme.muted, fontSize: 15, marginBottom: 16 },
  actions: { flexDirection: "row", gap: 16 },
  btnGhost: { flex: 1, backgroundColor: theme.surface2, borderRadius: 999, paddingVertical: 16, alignItems: "center" },
  btnPrimary: { flex: 1, backgroundColor: theme.accent, borderRadius: 999, paddingVertical: 16, alignItems: "center" },
  btnText: { color: theme.text, fontSize: 22, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.04 }] },
});
