// Pages Function (Cloudflare) — "mi reporte" (TID-MAX).
//
// Recibe el TOKEN de /api/login, lo verifica (HMAC + expiración) y devuelve SOLO el
// reporte del atleta dueño (reportes/<slug>.json), leído por la API de GitHub con
// GH_TOKEN (funciona con repo privado). Portado de Vercel; acepta GET o POST.
//
// Env: AUTH_SECRET, GH_TOKEN, (opc) GH_OWNER/GH_REPO/GH_BRANCH/REPORTES_DIR.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method !== "POST" && request.method !== "GET")
    return J({ error: "Usa POST o GET." }, 405);
  try {
    const secret = env.AUTH_SECRET || "";
    if (!secret) return J({ error: "Servidor sin AUTH_SECRET." }, 500);

    const body = request.method === "POST" ? await readJson(request) : {};
    const token = tokenFrom(request, body);
    if (!token) return J({ error: "Falta el token." }, 401);

    const payload = verify(token, secret);
    if (!payload) return J({ error: "Sesión inválida o expirada. Entra de nuevo." }, 401);

    const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
    if (!slug) return J({ error: "Token sin atleta." }, 400);

    const dir = env.REPORTES_DIR || "tid-max/software/reportes";
    const reporte = await leerReporte(env, `${dir}/${slug}.json`);
    if (reporte === null)
      return J({ error: "Aún no hay reporte para tu cuenta (falta que fluya tu fuente de datos)." }, 404);

    return J({ ok: true, slug, data: reporte });
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
  }
}

function tokenFrom(request, body) {
  const h = request.headers.get("authorization") || "";
  if (h.startsWith("Bearer ")) return h.slice(7).trim();
  if (body && body.token) return body.token;
  try { return new URL(request.url).searchParams.get("token") || ""; } catch { return ""; }
}

async function leerReporte(env, path) {
  const c = { owner: env.GH_OWNER || "carlosmoreno793508", repo: env.GH_REPO || "Cosas-Carlos", branch: env.GH_BRANCH || "main" };
  const r = await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/${path}?ref=${c.branch}`, {
    headers: { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": "tid-max-me", accept: "application/vnd.github+json" },
  });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error("GitHub GET " + r.status + ": " + (await r.text()).slice(0, 160));
  const j = await r.json();
  return JSON.parse(Buffer.from(j.content, "base64").toString("utf8"));
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
