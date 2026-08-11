// Función serverless (Vercel) — "mi reporte" (TID-MAX, Fase 2).
//
// Recibe el TOKEN que entregó /api/login, lo verifica (HMAC + expiración) y
// devuelve SOLO el reporte del atleta dueño de ese token (reportes/<slug>.json).
// Lee el archivo por la API de GitHub con GH_TOKEN, así que funciona aunque el
// repo sea PRIVADO — que es lo recomendado para privacidad real.
//
// Variables de entorno (Vercel → tid-max-app → Settings → Environment Variables):
//   AUTH_SECRET — la MISMA con que /api/login firma los tokens.
//   GH_TOKEN    — PAT fino con "Contents: Read" (el mismo de api/connect/evento).
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, REPORTES_DIR.

import crypto from "crypto";

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  dir: process.env.REPORTES_DIR || "tid-max/software/reportes",
};

export default async function handler(req, res) {
  if (req.method !== "POST" && req.method !== "GET")
    return res.status(405).json({ error: "Usa POST o GET." });
  try {
    const secret = process.env.AUTH_SECRET || "";
    if (!secret) return res.status(500).json({ error: "Servidor sin AUTH_SECRET." });

    const token = tokenDeLaPeticion(req);
    if (!token) return res.status(401).json({ error: "Falta el token." });

    const payload = verify(token, secret);
    if (!payload) return res.status(401).json({ error: "Sesión inválida o expirada. Entra de nuevo." });

    const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
    if (!slug) return res.status(400).json({ error: "Token sin atleta." });

    const reporte = await leerReporte(slug);
    if (reporte === null)
      return res.status(404).json({ error: "Aún no hay reporte para tu cuenta (falta que fluya tu fuente de datos)." });

    return res.status(200).json({ ok: true, slug, data: reporte });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

function tokenDeLaPeticion(req) {
  const h = req.headers.authorization || "";
  if (h.startsWith("Bearer ")) return h.slice(7).trim();
  return (req.body && req.body.token) || (req.query && req.query.token) || "";
}

// Verifica <body>.<sig>: recomputa el HMAC (tiempo-constante) y checa expiración.
function verify(token, secret) {
  const dot = token.lastIndexOf(".");
  if (dot < 1) return null;
  const body = token.slice(0, dot);
  const sig = token.slice(dot + 1);
  const esperado = b64url(crypto.createHmac("sha256", secret).update(body).digest());
  const a = Buffer.from(sig, "utf8");
  const b = Buffer.from(esperado, "utf8");
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let payload;
  try {
    payload = JSON.parse(Buffer.from(body.replace(/-/g, "+").replace(/_/g, "/"), "base64").toString("utf8"));
  } catch {
    return null;
  }
  if (!payload || typeof payload.exp !== "number" || payload.exp < Math.floor(Date.now() / 1000))
    return null;
  return payload;
}

async function leerReporte(slug) {
  const api = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${CFG.dir}/${slug}.json?ref=${CFG.branch}`;
  const r = await fetch(api, {
    headers: {
      authorization: `Bearer ${process.env.GH_TOKEN}`,
      "user-agent": "tid-max-me",
      accept: "application/vnd.github+json",
    },
  });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error("GitHub GET " + r.status + ": " + (await r.text()).slice(0, 160));
  const j = await r.json();
  return JSON.parse(Buffer.from(j.content, "base64").toString("utf8"));
}

function b64url(buf) {
  return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
