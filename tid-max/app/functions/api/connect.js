// Pages Function (Cloudflare) — Conectar una FUENTE desde la app (TID-MAX).
//
// El atleta pica "Conectar" -> crea/reusa su usuario en Junction (ex-Vital), genera un
// link token y devuelve la URL del widget. Guarda el mapeo atleta->user_id en
// tid-max/software/agregador_users.json ("repo como BD"). Portado de Vercel.
//
// Env: JUNCTION_API_KEY, (opc) JUNCTION_API_BASE/JUNCTION_LINK_BASE/JUNCTION_ENV/JUNCTION_REGION,
//   AUTH_SECRET, GH_TOKEN, UPLOAD_SECRET, (opc) GH_OWNER/GH_REPO/GH_BRANCH/AGREGADOR_USERS_PATH.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const J2 = jcfg(env);
    if (!J2.apiKey) return J({ error: "Falta JUNCTION_API_KEY en las variables de entorno de Cloudflare." }, 500);

    const body = await readJson(request);
    const { secret, atleta, provider } = body;

    // Autenticación: token de sesión (correcto, multiusuario) o LEGACY UPLOAD_SECRET + atleta.
    let slug = "";
    const authSecret = env.AUTH_SECRET || "";
    const token = tokenFrom(request, body);
    if (token) {
      if (!authSecret) return J({ error: "Servidor sin AUTH_SECRET." }, 500);
      const payload = verify(token, authSecret);
      if (!payload) return J({ error: "Sesión inválida o expirada." }, 401);
      slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
      if (!slug) return J({ error: "Token sin atleta." }, 400);
    } else if (env.UPLOAD_SECRET && secret === env.UPLOAD_SECRET) {
      slug = slugify(atleta);
      if (!slug) return J({ error: "Falta el atleta." }, 400);
    } else {
      return J({ error: "Necesitas iniciar sesión (o clave válida)." }, 401);
    }

    const userId = await junctionUser(J2, slug);
    const origin = request.headers.get("origin") ||
      (request.headers.get("host") ? `https://${request.headers.get("host")}` : "");
    const redirectUrl = origin ? `${origin}/?connected=ok` : null;
    const link = await junctionLinkToken(J2, userId, null, redirectUrl);
    const widgetUrl = link.link_web_url
      || `${J2.linkBase}/?token=${encodeURIComponent(link.link_token)}&env=${J2.env}&region=${J2.region}`;

    let mappingSaved = false;
    try { await guardarMapeo(env, J2, slug, userId); mappingSaved = true; }
    catch (e) { console.error("guardarMapeo (no fatal):", (e && e.message) || e); }

    return J({ ok: true, atleta: slug, provider: provider || null, user_id: userId, widget_url: widgetUrl, mapping_saved: mappingSaved });
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
  }
}

function jcfg(env) {
  return {
    apiKey: env.JUNCTION_API_KEY || "",
    apiBase: (env.JUNCTION_API_BASE || "https://api.sandbox.us.junction.com").replace(/\/+$/, ""),
    linkBase: (env.JUNCTION_LINK_BASE || "https://link.tryvital.io").replace(/\/+$/, ""),
    env: env.JUNCTION_ENV || "sandbox",
    region: env.JUNCTION_REGION || "us",
  };
}
function jhdr(J2) {
  return { "x-vital-api-key": J2.apiKey, "content-type": "application/json", accept: "application/json" };
}
async function junctionUser(J2, slug) {
  const clientUserId = `tidmax-${slug}`;
  const r = await fetch(`${J2.apiBase}/v2/user`, { method: "POST", headers: jhdr(J2), body: JSON.stringify({ client_user_id: clientUserId }) });
  if (r.ok) return (await r.json()).user_id;
  if (r.status === 400 || r.status === 409) {
    const g = await fetch(`${J2.apiBase}/v2/user/resolve/${encodeURIComponent(clientUserId)}`, { headers: jhdr(J2) });
    if (g.ok) return (await g.json()).user_id;
  }
  throw new Error("Junction /v2/user " + r.status + ": " + (await r.text()).slice(0, 160));
}
async function junctionLinkToken(J2, userId, provider, redirectUrl) {
  const base = { user_id: userId };
  if (provider) base.provider = provider;
  const intentos = redirectUrl ? [{ ...base, redirect_url: redirectUrl }, base] : [base];
  let lastErr = "";
  for (const b of intentos) {
    const r = await fetch(`${J2.apiBase}/v2/link/token`, { method: "POST", headers: jhdr(J2), body: JSON.stringify(b) });
    if (r.ok) return await r.json();
    lastErr = r.status + ": " + (await r.text()).slice(0, 160);
  }
  throw new Error("Junction /v2/link/token " + lastErr);
}
async function guardarMapeo(env, J2, slug, userId) {
  const c = cfg(env);
  const path = env.AGREGADOR_USERS_PATH || "tid-max/software/agregador_users.json";
  const api = `https://api.github.com/repos/${c.owner}/${c.repo}/contents/${path}`;
  const H = { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": "tid-max-connect", accept: "application/vnd.github+json" };
  let sha, store = {};
  const g = await fetch(`${api}?ref=${c.branch}`, { headers: H });
  if (g.ok) {
    const j = await g.json();
    sha = j.sha;
    try { store = JSON.parse(Buffer.from(j.content, "base64").toString("utf8")) || {}; } catch { store = {}; }
  } else if (g.status !== 404) {
    throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));
  }
  store[slug] = { user_id: userId, client_user_id: `tidmax-${slug}`, env: J2.env };
  const content = Buffer.from(JSON.stringify(store, null, 2) + "\n", "utf8").toString("base64");
  const body = { message: `Agregador: conectar ${slug}`, content, branch: c.branch };
  if (sha) body.sha = sha;
  const p = await fetch(api, { method: "PUT", headers: { ...H, "content-type": "application/json" }, body: JSON.stringify(body) });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
}

function slugify(v) {
  return String(v || "").trim().toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40);
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
