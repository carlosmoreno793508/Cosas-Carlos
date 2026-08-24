// Función serverless (Vercel) — "Evento objetivo" del app TID-MAX (multiusuario).
//
// Guarda el evento objetivo del atleta EN SU CUENTA (no global), para que el pipeline
// calcule su taper/pico de forma AISLADA por persona:
//   tid-max/software/eventos/<slug>.json
// El driver (tid_multi.py) copia ese archivo a la carpeta del atleta como evento.json,
// que es lo que build_evento (tid_data.py) ya lee. "Repo como BD", igual que run/wellness.
//
// Autenticación:
//   • token de sesión (HMAC, igual que /api/run y /api/wellness) → escribe por-atleta.
//   • (LEGACY) secret == UPLOAD_SECRET → escribe al evento.json GLOBAL compartido.
//     Se mantiene por compatibilidad; el camino nuevo y correcto es el token.
//
// Para BORRAR/limpiar el evento: manda evento null / vacío / {} → deja la cuenta sin
// evento (build_evento devuelve None y el reporte no muestra evento).
//
// Env (Vercel → tid-max-app → Settings → Environment Variables):
//   AUTH_SECRET — la MISMA con que /api/login firma los tokens (para el token).
//   GH_TOKEN    — PAT fino con "Contents: Read and write".
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, EVENTOS_DIR, EVENTO_PATH, UPLOAD_SECRET.

import crypto from "crypto";

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  dir: process.env.EVENTOS_DIR || "tid-max/software/eventos",       // por-atleta (nuevo)
  globalPath: process.env.EVENTO_PATH || "tid-max/software/evento.json", // global (legacy)
};

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    if (!process.env.GH_TOKEN) return res.status(500).json({ error: "Servidor sin GH_TOKEN." });

    const body = req.body || {};
    const evento = body.evento;                       // puede venir null/{} para limpiar
    const limpio = sanitize(evento);                  // null si no hay nombre válido

    // --- Camino nuevo: token de sesión → evento por-atleta ---
    const secret = process.env.AUTH_SECRET || "";
    const token = body.token ||
      ((req.headers.authorization || "").startsWith("Bearer ") ? req.headers.authorization.slice(7).trim() : "");
    if (token) {
      if (!secret) return res.status(500).json({ error: "Servidor sin AUTH_SECRET." });
      const payload = verify(token, secret);
      if (!payload) return res.status(401).json({ error: "Sesión inválida o expirada." });
      const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
      if (!slug) return res.status(400).json({ error: "Token sin atleta." });

      const path = `${CFG.dir}/${slug}.json`;
      // Documento a escribir: el evento limpio, o un "vaciado" explícito si se borró.
      const doc = limpio
        ? { slug, ...limpio, actualizado: new Date().toISOString() }
        : { slug, _vaciado: true, actualizado: new Date().toISOString(),
            _nota: "Sin evento objetivo activo (limpiado desde la app)." };
      const message = limpio ? `Evento de ${slug}: ${limpio.nombre}` : `Evento de ${slug}: (sin evento)`;
      const commit = await ghPutPath(path, doc, message);
      return res.status(200).json({ ok: true, evento: limpio, cleared: !limpio, commit });
    }

    // --- Camino LEGACY: contraseña compartida → evento global ---
    if (process.env.UPLOAD_SECRET && body.secret === process.env.UPLOAD_SECRET) {
      if (!limpio) return res.status(400).json({ error: "Falta el evento (al menos el nombre)." });
      const doc = { ...limpio, _nota:
        "Capturado desde la app TID-MAX (api/evento, legacy global). El camino nuevo es por-atleta." };
      const commit = await ghPutPath(CFG.globalPath, doc, `Evento objetivo: ${limpio.nombre}`);
      return res.status(200).json({ ok: true, evento: limpio, commit });
    }

    return res.status(401).json({ error: "Necesitas iniciar sesión (o clave válida)." });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

// ---- Normaliza y valida el evento (no confiar en el cliente). null si no hay nombre. ----
function sanitize(e) {
  if (!e || typeof e !== "object") return null;
  const s = (v) => (v == null || v === "" ? null : String(v).slice(0, 200));
  const fecha = (v) => (/^\d{4}-\d{2}-\d{2}$/.test(v || "") ? v : null);
  const nombre = s(e.nombre);
  if (!nombre || !nombre.trim()) return null;   // sin nombre = limpiar
  return {
    nombre,
    tipo_deporte: s(e.tipo_deporte),
    prioridad: ["A", "B", "C"].includes(e.prioridad) ? e.prioridad : null,
    sede: s(e.sede),
    fecha_inicio: fecha(e.fecha_inicio),
    fecha_fin: fecha(e.fecha_fin),
    fecha_viaje: fecha(e.fecha_viaje),
    meta: s(e.meta),
  };
}

// ---- Token HMAC (igual que /api/wellness) ----
function verify(token, secret) {
  if (!token) return null;
  const dot = token.lastIndexOf(".");
  if (dot < 1) return null;
  const bodyB = token.slice(0, dot), sig = token.slice(dot + 1);
  const esperado = b64url(crypto.createHmac("sha256", secret).update(bodyB).digest());
  const a = Buffer.from(sig, "utf8"), b = Buffer.from(esperado, "utf8");
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let payload;
  try { payload = JSON.parse(Buffer.from(bodyB.replace(/-/g, "+").replace(/_/g, "/"), "base64").toString("utf8")); }
  catch { return null; }
  if (!payload || typeof payload.exp !== "number" || payload.exp < Math.floor(Date.now() / 1000)) return null;
  return payload;
}
function b64url(buf) { return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }

// ---- GitHub: crear/actualizar un archivo JSON ----
function ghHeaders() {
  return { authorization: `Bearer ${process.env.GH_TOKEN}`, "user-agent": "tid-max-evento", accept: "application/vnd.github+json" };
}
async function ghPutPath(path, obj, message) {
  const api = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${path}`;
  let sha;
  const g = await fetch(`${api}?ref=${CFG.branch}`, { headers: ghHeaders() });
  if (g.ok) sha = (await g.json()).sha;
  else if (g.status !== 404) throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));

  const content = Buffer.from(JSON.stringify(obj, null, 2) + "\n", "utf8").toString("base64");
  const reqBody = { message, content, branch: CFG.branch };
  if (sha) reqBody.sha = sha;

  const p = await fetch(api, {
    method: "PUT", headers: { ...ghHeaders(), "content-type": "application/json" }, body: JSON.stringify(reqBody),
  });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
  const out = await p.json();
  return (out.commit && out.commit.sha) || null;
}
