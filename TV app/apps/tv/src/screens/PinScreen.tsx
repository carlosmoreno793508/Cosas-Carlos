import React, { useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { theme } from "../theme";

/** Pantalla de PIN (control parental) con teclado numérico para el D-pad. */
export function PinScreen({
  expected,
  onOk,
  onCancel,
}: {
  expected: string;
  onOk: () => void;
  onCancel: () => void;
}) {
  const [pin, setPin] = useState("");
  const [error, setError] = useState(false);

  function push(d: string) {
    setError(false);
    const next = (pin + d).slice(0, 4);
    setPin(next);
    if (next.length === 4) {
      if (next === expected) onOk();
      else {
        setError(true);
        setTimeout(() => setPin(""), 400);
      }
    }
  }

  const keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "cancel", "0", "del"];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Introduce el PIN</Text>
      <View style={styles.dots}>
        {[0, 1, 2, 3].map((i) => (
          <View key={i} style={[styles.dot, i < pin.length && styles.dotOn]} />
        ))}
      </View>
      {error ? <Text style={styles.error}>PIN incorrecto</Text> : null}
      <View style={styles.pad}>
        {keys.map((k) => (
          <Pressable
            key={k}
            hasTVPreferredFocus={k === "1"}
            style={({ focused }) => [styles.key, focused && styles.focused]}
            onPress={() => (k === "cancel" ? onCancel() : k === "del" ? setPin((p) => p.slice(0, -1)) : push(k))}
          >
            <Text style={styles.keyText}>{k === "cancel" ? "Cancelar" : k === "del" ? "⌫" : k}</Text>
          </Pressable>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center", gap: 24 },
  title: { color: theme.text, fontSize: 32, fontWeight: "800" },
  dots: { flexDirection: "row", gap: 20 },
  dot: { width: 26, height: 26, borderRadius: 13, borderWidth: 3, borderColor: theme.muted },
  dotOn: { backgroundColor: theme.accent, borderColor: theme.accent },
  error: { color: theme.danger, fontWeight: "700", fontSize: 20 },
  pad: { flexDirection: "row", flexWrap: "wrap", width: 3 * 120 + 2 * 16, gap: 16, justifyContent: "center" },
  key: { width: 120, height: 90, borderRadius: 16, backgroundColor: theme.surface, alignItems: "center", justifyContent: "center" },
  keyText: { color: theme.text, fontSize: 30, fontWeight: "700" },
  focused: { borderWidth: 4, borderColor: "#fff", transform: [{ scale: 1.05 }] },
});
