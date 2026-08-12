// Función serverless (Vercel) — LOGIN privado por persona (TID-MAX, Fase 2).
//
// El atleta entra con su USUARIO + PIN. Si coinciden, se le entrega un TOKEN
// firmado (HMAC-SHA256, sin estado en el servidor) que la app guarda y presenta
// a /api/me para leer SOLO su reporte. Los PINs viven como SECRETO del servidor
// (variable de entorno TID_LOGINS), nunca en el repo ni en el cliente.
//
// Dos fuentes de cuentas:
//   1) TID_LOGINS (env) — cuentas "semilla"/admin, PIN en claro en la variable.
//   2) usuarios.json (repo) — las que se dan de alta desde la app (api/registro),
//      con PIN hasheado (scrypt+salt). Se buscan por CORREO.
//
// Variables de entorno (Vercel → tid-max-app → Settings → Environment Variables):
//   AUTH_SECRET — cadena larga y aleatoria para firmar los tokens (mínimo 16).
//   TID_LOGINS  — (opcional) JSON de cuentas semilla. Ejemplo (una línea):
//       [{"user":"gaelmoreno@icloud.com","pin":"1234","slug":"gael-moreno"}]
//   GH_TOKEN    — (para leer usuarios.json del repo) PAT con "Contents: Read".
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, USUARIOS_PATH.
//
// Seguridad: comparación en tiempo ~constante; token con expiración (30 d).

import crypto from "crypto";

const TOKEN_TTL_S = 60 * 60 * 24 * 30; // 30 días

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  usuarios: process.env.USUARIOS_PATH || "tid-max/software/usuarios.json",
};

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const secret = process.env.AUTH_SECRET || "";
    if (!secret || secret.length < 16)
      return res.status(500).json({ error: "Servidor sin AUTH_SECRET (config faltante)." });

    const { user, pin } = req.body || {};
    const u = norm(user);
    const p = String(pin == null ? "" : pin);
    if (!u || !p) return res.status(400).json({ error: "Faltan correo o PIN." });

    // 1) Cuentas semilla (env TID_LOGINS) — PIN en claro, compare tiempo-constante.
    let match = null;
    let logins = [];
    try { logins = JSON.parse(process.env.TID_LOGINS || "[]"); } catch { logins = []; }
    if (Array.isArray(logins)) {
      const cuenta = logins.find((c) => norm(c.user) === u);
      if (cuenta && safeEqual(p, String(cuenta.pin == null ? "" : cuenta.pin)))
        match = { slug: String(cuenta.slug || "").trim(), nombre: cuenta.nombre || null };
    }

    // 2) Cuentas dadas de alta desde la app (usuarios.json, repo) — PIN con scrypt.
    if (!match) {
      const usuarios = await leerUsuarios();
      const cuenta = usuarios && Object.values(usuarios).find((c) => norm(c.email) === u);
      if (cuenta && scryptVerify(p, cuenta.salt, cuenta.hash))
        match = { slug: String(cuenta.slug || "").trim(), nombre: cuenta.nombre || null };
    }

    if (!match || !match.slug)
      return res.status(401).json({ error: "Correo o PIN incorrectos." });

    const exp = nowS() + TOKEN_TTL_S;
    const token = sign({ slug: match.slug, exp }, secret);
    return res.status(200).json({ ok: true, token, slug: match.slug, nombre: match.nombre, exp });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

function norm(v) {
  return String(v == null ? "" : v).trim().toLowerCase();
}

// Lee usuarios.json del repo (cuentas dadas de alta). {} si no existe o sin GH_TOKEN.
async function leerUsuarios() {
  if (!process.env.GH_TOKEN) return {};
  try {
    const r = await fetch(`https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${CFG.usuarios}?ref=${CFG.branch}`, {
      headers: { authorization: `Bearer ${process.env.GH_TOKEN}`, "user-agent": "tid-max-login", accept: "application/vnd.github+json" },
    });
    if (!r.ok) return {};
    const j = await r.json();
    return JSON.parse(Buffer.from(j.content, "base64").toString("utf8")) || {};
  } catch {
    return {};
  }
}

// Verifica un PIN contra su hash scrypt (tiempo-constante).
function scryptVerify(pin, salt, hashHex) {
  if (!salt || !hashHex) return false;
  try {
    const calc = crypto.scryptSync(String(pin), String(salt), 64);
    const ref = Buffer.from(String(hashHex), "hex");
    return calc.length === ref.length && crypto.timingSafeEqual(calc, ref);
  } catch {
    return false;
  }
}

function nowS() {
  return Math.floor(Date.now() / 1000);
}

// Firma un payload como <base64url(json)>.<base64url(hmac)>.
function sign(payload, secret) {
  const body = b64url(Buffer.from(JSON.stringify(payload), "utf8"));
  const sig = b64url(crypto.createHmac("sha256", secret).update(body).digest());
  return `${body}.${sig}`;
}

function b64url(buf) {
  return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

// Comparación de longitud-segura y tiempo-constante.
function safeEqual(a, b) {
  const ba = Buffer.from(a, "utf8");
  const bb = Buffer.from(b, "utf8");
  if (ba.length !== bb.length) {
    // Compara contra sí mismo para no revelar longitud por timing; siempre false.
    crypto.timingSafeEqual(ba, ba);
    return false;
  }
  return crypto.timingSafeEqual(ba, bb);
}
