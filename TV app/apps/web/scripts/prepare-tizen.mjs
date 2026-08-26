// Prepara el directorio dist/ para empaquetarlo como app Tizen (Samsung Crystal
// y demás Samsung Smart TV): copia el manifiesto config.xml y verifica el icono.
//
// Uso:  npm run prepare:tizen   (dentro de apps/web)
// Luego: cd dist && tizen package -t wgt

import { copyFileSync, existsSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const webRoot = join(here, "..");
const dist = join(webRoot, "dist");

if (!existsSync(dist)) {
  console.error("No existe dist/. Corre primero `npm run build`.");
  process.exit(1);
}

// 1) Copiar el manifiesto Tizen.
copyFileSync(join(webRoot, "tizen", "config.xml"), join(dist, "config.xml"));
console.log("✓ config.xml copiado a dist/");

// 2) Verificar el icono requerido por Tizen (512x512 recomendado).
const iconInDist = join(dist, "icon.png");
const iconSource = join(webRoot, "tizen", "icon.png");
if (existsSync(iconSource)) {
  copyFileSync(iconSource, iconInDist);
  console.log("✓ icon.png copiado a dist/");
} else if (!existsSync(iconInDist)) {
  // Dejamos una nota para que el packaging no falle silenciosamente.
  writeFileSync(
    join(dist, "ICONO-REQUERIDO.txt"),
    "Tizen requiere un icon.png (p. ej. 512x512). Ponlo en apps/web/tizen/icon.png\n" +
      "y vuelve a correr `npm run prepare:tizen`.\n",
  );
  console.warn(
    "⚠ Falta apps/web/tizen/icon.png — añádelo antes de empaquetar el .wgt.",
  );
}

console.log("\nListo. Ahora, con Tizen Studio CLI instalado:");
console.log("  cd dist");
console.log("  tizen package -t wgt -s <tu-perfil-de-firma>");
console.log("  tizen install -n TVApp.wgt -t <nombre-del-TV>");
