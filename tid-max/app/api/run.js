// Función serverless (Vercel) — SUBIR una corrida del grabador (TID-MAX, Fase A).
//
// El grabador de app/index.html guarda cada carrera en el teléfono (localStorage
// tid_runs). Este endpoint la sube TAMBIÉN a la cuenta del atleta autenticado, para
// que sea durable (sobrevive cambio de teléfono), cuente de verdad para el desbloqueo
// de zonas y quede lista para que el pipeline la lea.
//
// "Repo como BD" (igual que api/registro / api/me): se verifica el TOKEN (HMAC +
// expiración, idéntico a /api/login) y la corrida se agrega a
//   tid-max/software/corridas/<slug>.json
// vía la API de GitHub con GH_TOKEN. Dedup por 'fecha'; se conservan las últimas 200.
//
// Variables de entorno (Vercel → tid-max-app → Settings → Environment Variables):
//   AUTH_SECRET — la MISMA con que /api/login firma los tokens.
//   GH_TOKEN    — PAT fino con "Contents: Read and write".
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, CORRIDAS_DIR.

import crypto from "crypto";

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  dir: process.env.CORRIDAS_DIR || "tid-max/software/corridas",
};

const MAX_RUNS = 200;      // corridas que se conservan por atleta
const MAX_PUNTOS = 3000;   // puntos de ruta por corrida (recorte de seguridad)

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const secret = process.env.AUTH_SECRET || "";
    if (!secret) return res.status(500).json({ error: "Servidor sin AUTH_SECRET." });
    if (!process.env.GH_TOKEN) return res.status(500).json({ error: "Servidor sin GH_TOKEN." });

    const token = (req.body && req.body.token) ||
      ((req.headers.authorization || "").startsWith("Bearer ") ? req.headers.authorization.slice(7).trim() : "");
    const payload = verify(token, secret);
    if (!payload) return res.status(401).json({ error: "Sesión inválida o expirada. Entra de nuevo." });
    const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
    if (!slug) return res.status(400).json({ error: "Token sin atleta." });

    const run = limpiarCorrida((req.body && req.body.run) || {});
    if (!run) return res.status(400).json({ error: "Corrida no válida." });

    const path = `${CFG.dir}/${slug}.json`;
    const file = await ghGet(path);
    const doc = (file.json && typeof file.json === "object") ? file.json : { slug, corridas: [] };
    if (!Array.isArray(doc.corridas)) doc.corridas = [];

    // Dedup por 'fecha' (marca de tiempo ISO única por carrera).
    if (doc.corridas.some((c) => c && c.fecha === run.fecha))
      return res.status(200).json({ ok: true, dup: true, total: doc.corridas.length });

    doc.slug = slug;
    doc.corridas.unshift(run);
    doc.corridas = doc.corridas.slice(0, MAX_RUNS);
    doc.actualizado = new Date().toISOString();

    await ghPut(path, doc, file.sha, `Corrida de ${slug}: ${run.dist_km} km`);
    return res.status(200).json({ ok: true, total: doc.corridas.length });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

// Solo campos conocidos, con tipos/topes sanos: nada de datos arbitrarios al repo.
function limpiarCorrida(r) {
  if (!r || typeof r !== "object") return null;
  const num = (v) => (typeof v === "number" && isFinite(v) ? v : null);
  const fecha = String(r.fecha || "").slice(0, 40);
  if (!/^\d{4}-\d{2}-\d{2}T/.test(fecha)) return null;
  const splits = Array.isArray(r.splits) ? r.splits.slice(0, 100).map((s) => ({
    km: num(s && s.km), sec: num(s && s.sec), hr_avg: num(s && s.hr_avg), hr_max: num(s && s.hr_max),
  })) : [];
  let ruta = Array.isArray(r.ruta) ? r.ruta : [];
  if (ruta.length > MAX_PUNTOS) {          // muestreo uniforme si es muy larga
    const paso = Math.ceil(ruta.length / MAX_PUNTOS);
    ruta = ruta.filter((_, i) => i % paso === 0);
  }
  ruta = ruta.filter((p) => Array.isArray(p) && p.length === 2 && isFinite(p[0]) && isFinite(p[1]))
             .map((p) => [+(+p[0]).toFixed(5), +(+p[1]).toFixed(5)]);
  return {
    fecha,
    deporte: String(r.deporte || "running").slice(0, 24),
    dist_km: num(r.dist_km), dur_s: num(r.dur_s), pace_min_km: num(r.pace_min_km),
    n_puntos: num(r.n_puntos), hr_avg: num(r.hr_avg), hr_max: num(r.hr_max),
    splits, ruta,
  };
}

function verify(token, secret) {
  if (!token) return null;
  const dot = token.lastIndexOf(".");
  if (dot < 1) return null;
  const body = token.slice(0, dot), sig = token.slice(dot + 1);
  const esperado = b64url(crypto.createHmac("sha256", secret).update(body).digest());
  const a = Buffer.from(sig, "utf8"), b = Buffer.from(esperado, "utf8");
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let payload;
  try { payload = JSON.parse(Buffer.from(body.replace(/-/g, "+").replace(/_/g, "/"), "base64").toString("utf8")); }
  catch { return null; }
  if (!payload || typeof payload.exp !== "number" || payload.exp < Math.floor(Date.now() / 1000)) return null;
  return payload;
}

function b64url(buf) {
  return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function ghHeaders() {
  return { authorization: `Bearer ${process.env.GH_TOKEN}`, "user-agent": "tid-max-run", accept: "application/vnd.github+json" };
}
async function ghGet(path) {
  const r = await fetch(`https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${path}?ref=${CFG.branch}`, { headers: ghHeaders() });
  if (r.status === 404) return { sha: undefined, json: null };
  if (!r.ok) throw new Error("GitHub GET " + r.status + ": " + (await r.text()).slice(0, 160));
  const j = await r.json();
  let json = null;
  try { json = JSON.parse(Buffer.from(j.content, "base64").toString("utf8")); } catch { json = null; }
  return { sha: j.sha, json };
}
async function ghPut(path, obj, sha, message) {
  const content = Buffer.from(JSON.stringify(obj, null, 2) + "\n", "utf8").toString("base64");
  const body = { message, content, branch: CFG.branch };
  if (sha) body.sha = sha;
  const r = await fetch(`https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${path}`, {
    method: "PUT", headers: { ...ghHeaders(), "content-type": "application/json" }, body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("GitHub PUT " + r.status + ": " + (await r.text()).slice(0, 160));
}
