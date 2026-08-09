/**
 * TID-MAX · sync-web
 * "Build" de una PWA sin bundler: copia tid-max/app -> tid-max/native/www
 * para que Capacitor lo empaquete dentro de la app nativa.
 *
 * No hay paso de compilacion: la app es HTML/JS estatico. Este script solo
 * copia los archivos web (sin node_modules ni carpetas nativas) a www/.
 *
 *   npm run build   -> copia app/ a www/
 *   npm run sync    -> build + cap sync (mete www/ en iOS y Android)
 */
import { cp, rm, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(here, "../../app"); // la PWA vive en tid-max/app
const OUT = resolve(here, "../www");    // destino que Capacitor empaqueta

// Nunca copiar estas carpetas/archivos al bundle nativo.
const SKIP_TOP = new Set(["node_modules", ".git", "ios", "android", "www"]);

await rm(OUT, { recursive: true, force: true });
await mkdir(OUT, { recursive: true });

await cp(SRC, OUT, {
  recursive: true,
  filter: (src) => {
    if (src === SRC) return true;
    const top = src.slice(SRC.length + 1).split(/[\\/]/)[0];
    return !SKIP_TOP.has(top);
  },
});

console.log("✓ Web copiado:  tid-max/app  ->  tid-max/native/www");
