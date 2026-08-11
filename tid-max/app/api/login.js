// Función serverless (Vercel) — LOGIN privado por persona (TID-MAX, Fase 2).
//
// El atleta entra con su USUARIO + PIN. Si coinciden, se le entrega un TOKEN
// firmado (HMAC-SHA256, sin estado en el servidor) que la app guarda y presenta
// a /api/me para leer SOLO su reporte. Los PINs viven como SECRETO del servidor
// (variable de entorno TID_LOGINS), nunca en el repo ni en el cliente.
//
// Variables de entorno (Vercel → tid-max-app → Settings → Environment Variables):
//   TID_LOGINS  — JSON con las cuentas. Ejemplo (una sola línea):
//       [{"user":"gael","pin":"1234","slug":"gael-moreno"},
//        {"user":"carlos","pin":"5678","slug":"carlos-moreno"}]
//     'user' es lo que teclea el atleta (insensible a mayúsculas/espacios),
//     'pin' su clave, 'slug' su carpeta de reporte (reportes/<slug>.json).
//   AUTH_SECRET — cadena larga y aleatoria para firmar los tokens (mínimo 16).
//
// Seguridad: comparación de PIN en tiempo ~constante; token con expiración (30 d).
// No es banca — es un candado honesto para una app familiar/equipo; endurecer
// (hash de PIN, rate-limit) cuando entren clientes externos.

import crypto from "crypto";

const TOKEN_TTL_S = 60 * 60 * 24 * 30; // 30 días

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const secret = process.env.AUTH_SECRET || "";
    if (!secret || secret.length < 16)
      return res.status(500).json({ error: "Servidor sin AUTH_SECRET (config faltante)." });

    let logins;
    try {
      logins = JSON.parse(process.env.TID_LOGINS || "[]");
    } catch {
      return res.status(500).json({ error: "TID_LOGINS mal formado (no es JSON)." });
    }
    if (!Array.isArray(logins) || !logins.length)
      return res.status(500).json({ error: "Servidor sin cuentas (TID_LOGINS vacío)." });

    const { user, pin } = req.body || {};
    const u = norm(user);
    const p = String(pin == null ? "" : pin);
    if (!u || !p) return res.status(400).json({ error: "Faltan usuario o PIN." });

    // Busca la cuenta y compara el PIN en tiempo ~constante (evita fugas por timing).
    const cuenta = logins.find((c) => norm(c.user) === u);
    const okUser = !!cuenta;
    const pinRef = okUser ? String(cuenta.pin == null ? "" : cuenta.pin) : "";
    const okPin = safeEqual(p, pinRef);
    if (!okUser || !okPin)
      return res.status(401).json({ error: "Usuario o PIN incorrectos." });

    const slug = String(cuenta.slug || "").trim();
    if (!slug) return res.status(500).json({ error: "Cuenta sin 'slug' configurado." });

    const exp = nowS() + TOKEN_TTL_S;
    const token = sign({ slug, exp }, secret);
    return res.status(200).json({ ok: true, token, slug, nombre: cuenta.nombre || null, exp });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

function norm(v) {
  return String(v == null ? "" : v).trim().toLowerCase();
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
