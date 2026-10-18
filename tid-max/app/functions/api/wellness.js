// Pages Function (Cloudflare) — SUBIR el bienestar diario (TID-MAX).
//
// Guarda el registro diario (Hooper-Mackinnon + sRPE) en tid-max/software/bienestar/<slug>.json
// ("repo como BD"), autenticado con el token (HMAC). Upsert por 'fecha'. Portado de Vercel.
//
// Env: AUTH_SECRET, GH_TOKEN, (opc) GH_OWNER/GH_REPO/GH_BRANCH/BIENESTAR_DIR.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

const MAX_DIAS = 400;

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const secret = env.AUTH_SECRET || "";
    if (!secret) return J({ error: "Servidor sin AUTH_SECRET." }, 500);
    if (!env.GH_TOKEN) return J({ error: "Servidor sin GH_TOKEN." }, 500);

    const body = await readJson(request);
    const token = tokenFrom(request, body);
    const payload = verify(token, secret);
    if (!payload) return J({ error: "Sesión inválida o expirada." }, 401);
    const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
    if (!slug) return J({ error: "Token sin atleta." }, 400);

    const dia = limpiarDia(body.dia || {});
    if (!dia) return J({ error: "Registro no válido." }, 400);

    const dir = env.BIENESTAR_DIR || "tid-max/software/bienestar";
    const path = `${dir}/${slug}.json`;
    const file = await ghGet(env, path);
    const doc = (file.json && typeof file.json === "object") ? file.json : { slug, dias: [] };
    if (!Array.isArray(doc.dias)) doc.dias = [];

    doc.dias = doc.dias.filter((d) => d && d.fecha !== dia.fecha);  // upsert por fecha
    doc.dias.push(dia);
    doc.dias.sort((a, b) => (a.fecha < b.fecha ? -1 : 1));
    doc.dias = doc.dias.slice(-MAX_DIAS);
    doc.slug = slug;
    doc.actualizado = new Date().toISOString();

    await ghPut(env, path, doc, file.sha, `Bienestar de ${slug}: ${dia.fecha}`);
    return J({ ok: true, total: doc.dias.length });
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
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

function tokenFrom(request, body) {
  const h = request.headers.get("authorization") || "";
  if (h.startsWith("Bearer ")) return h.slice(7).trim();
  return (body && body.token) || "";
}
async function readJson(request) {
  try { return (await request.json()) || {}; } catch { return {}; }
}
function J(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "x-content-type-options": "nosniff" },
  });
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
function cfg(env) {
  return { owner: env.GH_OWNER || "carlosmoreno793508", repo: env.GH_REPO || "Cosas-Carlos", branch: env.GH_BRANCH || "main" };
}
function ghHeaders(env) {
  return { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": "tid-max-wellness", accept: "application/vnd.github+json" };
}
async function ghGet(env, path) {
  const c = cfg(env);
  const r = await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/${path}?ref=${c.branch}`, { headers: ghHeaders(env) });
  if (r.status === 404) return { sha: undefined, json: null };
  if (!r.ok) throw new Error("GitHub GET " + r.status + ": " + (await r.text()).slice(0, 160));
  const j = await r.json();
  let json = null;
  try { json = JSON.parse(Buffer.from(j.content, "base64").toString("utf8")); } catch { json = null; }
  return { sha: j.sha, json };
}
async function ghPut(env, path, obj, sha, message) {
  const c = cfg(env);
  const content = Buffer.from(JSON.stringify(obj, null, 2) + "\n", "utf8").toString("base64");
  const body = { message, content, branch: c.branch };
  if (sha) body.sha = sha;
  const r = await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/${path}`, {
    method: "PUT", headers: { ...ghHeaders(env), "content-type": "application/json" }, body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("GitHub PUT " + r.status + ": " + (await r.text()).slice(0, 160));
}
