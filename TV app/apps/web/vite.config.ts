import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// base "./" para que funcione empaquetado dentro de un contenedor Tizen/webOS,
// donde la app se sirve desde rutas relativas.
export default defineConfig({
  base: "./",
  plugins: [react()],
  build: {
    // Los WebView de Samsung/LG antiguos necesitan un target conservador.
    target: "es2017",
    outDir: "dist",
  },
  server: {
    host: true,
    port: 5173,
  },
});
