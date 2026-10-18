// Pages Function (Cloudflare) — "Evento objetivo" por-atleta (TID-MAX).
//
// Guarda el evento objetivo del atleta EN SU CUENTA: tid-max/software/eventos/<slug>.json
// ("repo como BD"). Autenticado con el token de sesión (HMAC); camino LEGACY por
// UPLOAD_SECRET escribe el evento.json global. Mandar evento null/{} limpia la cuenta.
// Portado de Vercel; misma lógica, envoltorio Cloudflare.
//
// Env: AUTH_SECRET, GH_TOKEN, (opc) GH_OWNER/GH_REPO/GH_BRANCH/EVENTOS_DIR/EVENTO_PATH/UPLOAD_SECRET.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    if (!env.GH_TOKEN) return J({ error: "Servidor sin GH_TOKEN." }, 500);

    const body = await readJson(request);
    const evento = body.evento;             // puede venir null/{} para limpiar
    const limpio = sanitize(evento);        // null si no hay nombre válido

    const dir = env.EVENTOS_DIR || "tid-max/software/eventos";
    const globalPath = env.EVENTO_PATH || "tid-max/software/evento.json";

    // --- Camino nuevo: token de sesión -> evento por-atleta ---
    const secret = env.AUTH_SECRET || "";
    const token = tokenFrom(request, body);
    if (token) {
      if (!secret) return J({ error: "Servidor sin AUTH_SECRET." }, 500);
      const payload = verify(token, secret);
      if (!payload) return J({ error: "Sesión inválida o expirada." }, 401);
      const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
      if (!slug) return J({ error: "Token sin atleta." }, 400);

      const path = `${dir}/${slug}.json`;
      const doc = limpio
        ? { slug, ...limpio, actualizado: new Date().toISOString() }
        : { slug, _vaciado: true, actualizado: new Date().toISOString(),
            _nota: "Sin evento objetivo activo (limpiado desde la app)." };
      const message = limpio ? `Evento de ${slug}: ${limpio.nombre}` : `Evento de ${slug}: (sin evento)`;
      const commit = await ghPut(env, path, doc, message, "tid-max-evento");
      return J({ ok: true, evento: limpio, cleared: !limpio, commit });
    }

    // --- Camino LEGACY: contraseña compartida -> evento global ---
    if (env.UPLOAD_SECRET && body.secret === env.UPLOAD_SECRET) {
      if (!limpio) return J({ error: "Falta el evento (al menos el nombre)." }, 400);
      const doc = { ...limpio, _nota: "Capturado desde la app TID-MAX (api/evento, legacy global). El camino nuevo es por-atleta." };
      const commit = await ghPut(env, globalPath, doc, `Evento objetivo: ${limpio.nombre}`, "tid-max-evento");
      return J({ ok: true, evento: limpio, commit });
    }

    return J({ error: "Necesitas iniciar sesión (o clave válida)." }, 401);
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
  }
}

function sanitize(e) {
  if (!e || typeof e !== "object") return null;
  const s = (v) => (v == null || v === "" ? null : String(v).slice(0, 200));
  const fecha = (v) => (/^\d{4}-\d{2}-\d{2}$/.test(v || "") ? v : null);
  const nombre = s(e.nombre);
  if (!nombre || !nombre.trim()) return null;
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
async function ghPut(env, path, obj, message, ua) {
  const c = cfg(env);
  const api = `https://api.github.com/repos/${c.owner}/${c.repo}/contents/${path}`;
  const H = { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": ua, accept: "application/vnd.github+json" };
  let sha;
  const g = await fetch(`${api}?ref=${c.branch}`, { headers: H });
  if (g.ok) sha = (await g.json()).sha;
  else if (g.status !== 404) throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));
  const content = Buffer.from(JSON.stringify(obj, null, 2) + "\n", "utf8").toString("base64");
  const reqBody = { message, content, branch: c.branch };
  if (sha) reqBody.sha = sha;
  const p = await fetch(api, { method: "PUT", headers: { ...H, "content-type": "application/json" }, body: JSON.stringify(reqBody) });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
  const out = await p.json();
  return (out.commit && out.commit.sha) || null;
}
