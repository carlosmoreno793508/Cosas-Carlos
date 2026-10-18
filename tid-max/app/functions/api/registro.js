// Pages Function (Cloudflare) — ALTA de usuario real desde la app (TID-MAX).
//
// El atleta se da de alta (nombre, correo, PIN + clave de la familia). Se guarda en
// usuarios.json (PIN con hash scrypt+salt), se agrega a atletas.json y se crea un
// perfil-<slug>.json inicial. Devuelve token (auto-login). Portado de Vercel.
//
// Env: UPLOAD_SECRET (o SIGNUP_OPEN="true"), AUTH_SECRET, GH_TOKEN,
//   (opc) GH_OWNER/GH_REPO/GH_BRANCH/USUARIOS_PATH/ROSTER_PATH.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

const TOKEN_TTL_S = 60 * 60 * 24 * 30; // 30 días

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const authSecret = env.AUTH_SECRET || "";
    if (!authSecret || authSecret.length < 16) return J({ error: "Servidor sin AUTH_SECRET." }, 500);
    if (!env.GH_TOKEN) return J({ error: "Servidor sin GH_TOKEN (no puedo guardar la cuenta)." }, 500);

    const body = await readJson(request);
    const { nombre, email, pin, deporte, reloj, code, hp, t, nacimiento, peso } = body;

    // Anti-bot: honeypot + tiempo mínimo.
    if (String(hp || "").trim()) return J({ error: "No pude crear la cuenta." }, 400);
    const ms = Number(t);
    if (Number.isFinite(ms) && ms < 1500) return J({ error: "Fue demasiado rápido; intenta de nuevo." }, 400);

    const abierto = env.SIGNUP_OPEN === "true";
    if (!abierto) {
      if (!env.UPLOAD_SECRET) return J({ error: "Servidor sin UPLOAD_SECRET (verja del alta). O pon SIGNUP_OPEN=true para abrir el registro." }, 500);
      if (String(code || "") !== env.UPLOAD_SECRET) return J({ error: "Clave de la familia incorrecta." }, 401);
    }

    const nom = String(nombre || "").trim();
    const mail = String(email || "").trim().toLowerCase();
    const p = String(pin == null ? "" : pin);
    if (!nom) return J({ error: "Falta tu nombre." }, 400);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)) return J({ error: "Correo no válido." }, 400);
    if (p.length < 4) return J({ error: "El PIN debe tener al menos 4 caracteres." }, 400);

    const nac = String(nacimiento || "").trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(nac)) return J({ error: "Fecha de nacimiento no válida." }, 400);
    const edad = edadDesde(nac);
    if (edad == null || edad < 5 || edad > 100) return J({ error: "Revisa tu fecha de nacimiento." }, 400);

    let pesoKg = null;
    if (peso != null && String(peso).trim() !== "") {
      const n = Number(peso);
      if (!Number.isFinite(n) || n < 20 || n > 300) return J({ error: "Revisa el peso (20–300 kg)." }, 400);
      pesoKg = Math.round(n * 10) / 10;
    }

    const slug = slugify(nom);
    if (!slug) return J({ error: "Nombre no válido." }, 400);

    const usuariosPath = env.USUARIOS_PATH || "tid-max/software/usuarios.json";
    const rosterPath = env.ROSTER_PATH || "tid-max/software/atletas.json";

    // 1) usuarios.json
    const uFile = await ghGet(env, usuariosPath);
    const usuarios = uFile.json && typeof uFile.json === "object" ? uFile.json : {};
    if (usuarios[slug]) return J({ error: "Ya existe una cuenta con ese nombre." }, 409);
    if (Object.values(usuarios).some((u) => u && String(u.email).toLowerCase() === mail))
      return J({ error: "Ese correo ya tiene cuenta. Entra con tu PIN." }, 409);

    const salt = crypto.randomBytes(16).toString("hex");
    const hash = crypto.scryptSync(p, salt, 64).toString("hex");
    usuarios[slug] = { slug, email: mail, nombre: nom, salt, hash, nacimiento: nac, edad, peso_kg: pesoKg, created: new Date().toISOString() };
    await ghPut(env, usuariosPath, usuarios, uFile.sha, `Alta de usuario: ${slug}`);

    // 2) atletas.json
    const rFile = await ghGet(env, rosterPath);
    const roster = rFile.json && typeof rFile.json === "object" ? rFile.json : { atletas: [] };
    if (!Array.isArray(roster.atletas)) roster.atletas = [];
    if (!roster.atletas.some((a) => a && a.slug === slug)) {
      roster.atletas.push({ slug, nombre: nom, deporte: String(deporte || "").trim() || "otro", reloj: String(reloj || "").trim() || undefined, fuente: "agregador", perfil: `perfil-${slug}.json`, activo: true });
      await ghPut(env, rosterPath, roster, rFile.sha, `Registro: alta de ${slug}`);
    }

    // 2b) perfil-<slug>.json (solo si no existe)
    const perfilPath = `tid-max/software/perfil-${slug}.json`;
    const pFile = await ghGet(env, perfilPath);
    if (!pFile.json) {
      const perfil = {
        _fuente: `Perfil de ${nom} — creado desde el alta en la app.`,
        atleta: nom, deporte: String(deporte || "").trim() || "otro", reloj: String(reloj || "").trim() || undefined,
        perfil: {
          fecha_nacimiento: nac, edad, fc_max_estimada: 220 - edad,
          sexo: null, peso_kg: pesoKg, altura_cm: null, fc_reposo: null, fc_max_carrera: null,
          vt1_fc: null, vt2_fc: null, fatmax_fc: null,
          _nota: "Zonas provisionales por edad (FC máx ≈ 220 − edad). Se recalibran con FC en reposo y una FC máx real medida.",
        },
        objetivos: [],
      };
      await ghPut(env, perfilPath, perfil, pFile.sha, `Perfil inicial de ${slug}`);
    }

    const exp = Math.floor(Date.now() / 1000) + TOKEN_TTL_S;
    const token = sign({ slug, exp }, authSecret);
    return J({ ok: true, token, slug, nombre: nom, exp });
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
  }
}

function edadDesde(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!m) return null;
  const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const nac = new Date(Date.UTC(y, mo - 1, d));
  if (nac.getUTCFullYear() !== y || nac.getUTCMonth() !== mo - 1 || nac.getUTCDate() !== d) return null;
  const hoy = new Date();
  let e = hoy.getUTCFullYear() - y;
  const cumpleDespues = (hoy.getUTCMonth() + 1 < mo) || (hoy.getUTCMonth() + 1 === mo && hoy.getUTCDate() < d);
  if (cumpleDespues) e -= 1;
  return e;
}
function slugify(v) {
  return String(v || "").trim().toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40);
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
function cfg(env) {
  return { owner: env.GH_OWNER || "carlosmoreno793508", repo: env.GH_REPO || "Cosas-Carlos", branch: env.GH_BRANCH || "main" };
}
function ghHeaders(env) {
  return { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": "tid-max-registro", accept: "application/vnd.github+json" };
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
