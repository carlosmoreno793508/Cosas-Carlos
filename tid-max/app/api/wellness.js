// Función serverless (Vercel) — SUBIR el bienestar diario del atleta (TID-MAX).
//
// Guarda el registro diario (Hooper-Mackinnon + sRPE) en la cuenta del atleta:
//   tid-max/software/bienestar/<slug>.json
// Autenticado con el TOKEN (HMAC, igual que /api/me y /api/run). Upsert por 'fecha'
// (un registro por día). El pipeline puede leer estos datos para el ACWR del tablero.
//
// Env (Vercel → tid-max-app → Settings → Environment Variables):
//   AUTH_SECRET — la MISMA con que /api/login firma los tokens.
//   GH_TOKEN    — PAT fino con "Contents: Read and write".
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, BIENESTAR_DIR.

import crypto from "crypto";

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  dir: process.env.BIENESTAR_DIR || "tid-max/software/bienestar",
};
const MAX_DIAS = 400;

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const secret = process.env.AUTH_SECRET || "";
    if (!secret) return res.status(500).json({ error: "Servidor sin AUTH_SECRET." });
    if (!process.env.GH_TOKEN) return res.status(500).json({ error: "Servidor sin GH_TOKEN." });

    const token = (req.body && req.body.token) ||
      ((req.headers.authorization || "").startsWith("Bearer ") ? req.headers.authorization.slice(7).trim() : "");
    const payload = verify(token, secret);
    if (!payload) return res.status(401).json({ error: "Sesión inválida o expirada." });
    const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
    if (!slug) return res.status(400).json({ error: "Token sin atleta." });

    const dia = limpiarDia((req.body && req.body.dia) || {});
    if (!dia) return res.status(400).json({ error: "Registro no válido." });

    const path = `${CFG.dir}/${slug}.json`;
    const file = await ghGet(path);
    const doc = (file.json && typeof file.json === "object") ? file.json : { slug, dias: [] };
    if (!Array.isArray(doc.dias)) doc.dias = [];

    doc.dias = doc.dias.filter((d) => d && d.fecha !== dia.fecha);   // upsert por fecha
    doc.dias.push(dia);
    doc.dias.sort((a, b) => (a.fecha < b.fecha ? -1 : 1));
    doc.dias = doc.dias.slice(-MAX_DIAS);
    doc.slug = slug;
    doc.actualizado = new Date().toISOString();

    await ghPut(path, doc, file.sha, `Bienestar de ${slug}: ${dia.fecha}`);
    return res.status(200).json({ ok: true, total: doc.dias.length });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

function limpiarDia(r) {
  if (!r || typeof r !== "object") return null;
  const fecha = String(r.fecha || "").slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(fecha)) return null;
  const clamp = (v, lo, hi) => { const n = Number(v); return Number.isFinite(n) ? Math.min(hi, Math.max(lo, Math.round(n))) : null; };
  return {
    fecha,
    sueno: clamp(r.sueno, 1, 7), estres: clamp(r.estres, 1, 7),
    fatiga: clamp(r.fatiga, 1, 7), dolor: clamp(r.dolor, 1, 7),
    hooper: clamp(r.hooper, 4, 28),
    rpe: r.rpe == null ? null : clamp(r.rpe, 1, 10),
    min: r.min == null ? null : clamp(r.min, 0, 600),
    carga: r.carga == null ? null : clamp(r.carga, 0, 6000),
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
function b64url(buf) { return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }
function ghHeaders() { return { authorization: `Bearer ${process.env.GH_TOKEN}`, "user-agent": "tid-max-wellness", accept: "application/vnd.github+json" }; }
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
