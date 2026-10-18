// Pages Function (Cloudflare) — LOGIN privado por persona (TID-MAX).
//
// Portado de la función serverless de Vercel. MISMA lógica: usuario + PIN -> token
// firmado (HMAC-SHA256, sin estado). Cuentas semilla en TID_LOGINS (PIN en claro) y
// cuentas de la app en usuarios.json (PIN con scrypt+salt). Solo cambia el envoltorio:
// Vercel (req,res) -> Cloudflare Pages (onRequestPost, Request/Response) y process.env -> env.
//
// Env (Cloudflare Pages -> Settings -> Environment variables):
//   AUTH_SECRET, TID_LOGINS (opcional), GH_TOKEN, (opc) GH_OWNER/GH_REPO/GH_BRANCH/USUARIOS_PATH.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

const TOKEN_TTL_S = 60 * 60 * 24 * 30; // 30 días

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const secret = env.AUTH_SECRET || "";
    if (!secret || secret.length < 16)
      return J({ error: "Servidor sin AUTH_SECRET (config faltante)." }, 500);

    const body = await readJson(request);
    const u = norm(body.user);
    const p = String(body.pin == null ? "" : body.pin);
    if (!u || !p) return J({ error: "Faltan correo o PIN." }, 400);

    // 1) Cuentas semilla (TID_LOGINS) — PIN en claro, compare tiempo-constante.
    let match = null;
    let logins = [];
    try { logins = JSON.parse(env.TID_LOGINS || "[]"); } catch { logins = []; }
    if (Array.isArray(logins)) {
      const cuenta = logins.find((c) => norm(c.user) === u);
      if (cuenta && safeEqual(p, String(cuenta.pin == null ? "" : cuenta.pin)))
        match = { slug: String(cuenta.slug || "").trim(), nombre: cuenta.nombre || null };
    }

    // 2) Cuentas dadas de alta desde la app (usuarios.json, repo) — PIN con scrypt.
    if (!match) {
      const usuarios = await leerUsuarios(env);
      const cuenta = usuarios && Object.values(usuarios).find((c) => norm(c.email) === u);
      if (cuenta && scryptVerify(p, cuenta.salt, cuenta.hash))
        match = { slug: String(cuenta.slug || "").trim(), nombre: cuenta.nombre || null };
    }

    if (!match || !match.slug) return J({ error: "Correo o PIN incorrectos." }, 401);

    const exp = nowS() + TOKEN_TTL_S;
    const token = sign({ slug: match.slug, exp }, secret);
    return J({ ok: true, token, slug: match.slug, nombre: match.nombre, exp });
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
  }
}

function norm(v) { return String(v == null ? "" : v).trim().toLowerCase(); }
function nowS() { return Math.floor(Date.now() / 1000); }

async function leerUsuarios(env) {
  if (!env.GH_TOKEN) return {};
  try {
    const c = { owner: env.GH_OWNER || "carlosmoreno793508", repo: env.GH_REPO || "Cosas-Carlos", branch: env.GH_BRANCH || "main", usuarios: env.USUARIOS_PATH || "tid-max/software/usuarios.json" };
    const r = await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/${c.usuarios}?ref=${c.branch}`, {
      headers: { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": "tid-max-login", accept: "application/vnd.github+json" },
    });
    if (!r.ok) return {};
    const j = await r.json();
    return JSON.parse(Buffer.from(j.content, "base64").toString("utf8")) || {};
  } catch { return {}; }
}

function scryptVerify(pin, salt, hashHex) {
  if (!salt || !hashHex) return false;
  try {
    const calc = crypto.scryptSync(String(pin), String(salt), 64);
    const ref = Buffer.from(String(hashHex), "hex");
    return calc.length === ref.length && crypto.timingSafeEqual(calc, ref);
  } catch { return false; }
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
function sign(payload, secret) {
  const body = b64url(Buffer.from(JSON.stringify(payload), "utf8"));
  const sig = b64url(crypto.createHmac("sha256", secret).update(body).digest());
  return `${body}.${sig}`;
}
function b64url(buf) { return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }
function safeEqual(a, b) {
  const ba = Buffer.from(a, "utf8");
  const bb = Buffer.from(b, "utf8");
  if (ba.length !== bb.length) { crypto.timingSafeEqual(ba, ba); return false; }
  return crypto.timingSafeEqual(ba, bb);
}
