// Lanzador de la demo de MoreTV: construye el núcleo y arranca, a la vez, el
// servidor de contenido y la app web. Sin dependencias externas; multiplataforma.
import { spawn, spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const npm = process.platform === "win32" ? "npm.cmd" : "npm";
const run = (args) => spawn(npm, args, { cwd: root, stdio: "inherit", shell: process.platform === "win32" });

console.log("→ Construyendo el núcleo (@tvapp/core)…");
const build = spawnSync(npm, ["run", "build:core"], { cwd: root, stdio: "inherit", shell: process.platform === "win32" });
if (build.status !== 0) {
  console.error("Falló la construcción del núcleo. Revisa que hiciste `npm install`.");
  process.exit(1);
}

console.log("→ Arrancando servidor de contenido (http://localhost:8080) y app web (http://localhost:5173)…");
console.log("  Abre http://localhost:5173 en tu navegador. Ctrl+C para detener.\n");

const server = run(["run", "start:server"]);
const web = run(["run", "dev:web"]);

function shutdown() {
  server.kill();
  web.kill();
  process.exit(0);
}
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
server.on("exit", shutdown);
web.on("exit", shutdown);
