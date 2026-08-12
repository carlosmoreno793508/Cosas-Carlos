// Función serverless (Vercel) — ALTA de usuario real desde la app (TID-MAX).
//
// El atleta se da de alta él mismo: nombre, correo y PIN + la CLAVE DE LA FAMILIA
// (para que no se registre cualquiera). Se crea su cuenta y queda logueado.
//
// "Repo como BD" (igual que api/connect / api/evento): la cuenta se guarda en
// tid-max/software/usuarios.json (PIN con hash scrypt + salt, NUNCA en claro) y se
// agrega al registro tid-max/software/atletas.json para que el pipeline lo procese.
//
// Variables de entorno (Vercel → tid-max-app → Settings → Environment Variables):
//   UPLOAD_SECRET — la clave de la familia (verja del alta). Ya existe.
//   AUTH_SECRET   — la MISMA con que /api/login firma los tokens.
//   GH_TOKEN      — PAT fino con "Contents: Read and write".
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, USUARIOS_PATH, ROSTER_PATH.
//
// Nota de privacidad: el repo es PÚBLICO hoy, así que usuarios.json (con hashes)
// queda visible. Los PINs son de baja entropía: para seguridad real, poner el repo
// en PRIVADO. Los hashes usan scrypt+salt para no guardar el PIN en claro.

import crypto from "crypto";

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  usuarios: process.env.USUARIOS_PATH || "tid-max/software/usuarios.json",
  roster: process.env.ROSTER_PATH || "tid-max/software/atletas.json",
};

const TOKEN_TTL_S = 60 * 60 * 24 * 30; // 30 días

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const authSecret = process.env.AUTH_SECRET || "";
    if (!authSecret || authSecret.length < 16)
      return res.status(500).json({ error: "Servidor sin AUTH_SECRET." });
    if (!process.env.GH_TOKEN)
      return res.status(500).json({ error: "Servidor sin GH_TOKEN (no puedo guardar la cuenta)." });

    const { nombre, email, pin, deporte, reloj, code, hp, t, nacimiento } = req.body || {};

    // --- Anti-bot (siempre activo, sin setup) ---
    // 1) Honeypot: un campo invisible que solo los bots llenan.
    if (String(hp || "").trim())
      return res.status(400).json({ error: "No pude crear la cuenta." });
    // 2) Tiempo: un humano tarda segundos en llenar el formulario; los bots, milisegundos.
    const ms = Number(t);
    if (Number.isFinite(ms) && ms < 1500)
      return res.status(400).json({ error: "Fue demasiado rápido; intenta de nuevo." });

    // --- Verja del alta ---
    // Por defecto se pide la clave de la familia. Con SIGNUP_OPEN="true" el registro
    // queda ABIERTO (sin clave): el anti-bot de arriba es la única barrera.
    const abierto = process.env.SIGNUP_OPEN === "true";
    if (!abierto) {
      if (!process.env.UPLOAD_SECRET)
        return res.status(500).json({ error: "Servidor sin UPLOAD_SECRET (verja del alta). O pon SIGNUP_OPEN=true para abrir el registro." });
      if (String(code || "") !== process.env.UPLOAD_SECRET)
        return res.status(401).json({ error: "Clave de la familia incorrecta." });
    }

    const nom = String(nombre || "").trim();
    const mail = String(email || "").trim().toLowerCase();
    const p = String(pin == null ? "" : pin);
    if (!nom) return res.status(400).json({ error: "Falta tu nombre." });
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)) return res.status(400).json({ error: "Correo no válido." });
    if (p.length < 4) return res.status(400).json({ error: "El PIN debe tener al menos 4 caracteres." });

    // Fecha de nacimiento — para calibrar las zonas de FC (FC máx estimada por edad).
    const nac = String(nacimiento || "").trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(nac)) return res.status(400).json({ error: "Fecha de nacimiento no válida." });
    const edad = edadDesde(nac);
    if (edad == null || edad < 5 || edad > 100) return res.status(400).json({ error: "Revisa tu fecha de nacimiento." });

    const slug = slugify(nom);
    if (!slug) return res.status(400).json({ error: "Nombre no válido." });

    // 1) usuarios.json — dedup por slug/correo, agrega la cuenta con hash.
    const uFile = await ghGet(CFG.usuarios);
    const usuarios = uFile.json && typeof uFile.json === "object" ? uFile.json : {};
    if (usuarios[slug]) return res.status(409).json({ error: "Ya existe una cuenta con ese nombre." });
    if (Object.values(usuarios).some((u) => u && String(u.email).toLowerCase() === mail))
      return res.status(409).json({ error: "Ese correo ya tiene cuenta. Entra con tu PIN." });

    const salt = crypto.randomBytes(16).toString("hex");
    const hash = crypto.scryptSync(p, salt, 64).toString("hex");
    usuarios[slug] = {
      slug, email: mail, nombre: nom, salt, hash,
      nacimiento: nac, edad,
      created: new Date().toISOString(),
    };
    await ghPut(CFG.usuarios, usuarios, uFile.sha, `Alta de usuario: ${slug}`);

    // 2) atletas.json — agrega al registro para que el pipeline genere su reporte.
    const rFile = await ghGet(CFG.roster);
    const roster = rFile.json && typeof rFile.json === "object" ? rFile.json : { atletas: [] };
    if (!Array.isArray(roster.atletas)) roster.atletas = [];
    if (!roster.atletas.some((a) => a && a.slug === slug)) {
      roster.atletas.push({
        slug, nombre: nom,
        deporte: String(deporte || "").trim() || "otro",
        reloj: String(reloj || "").trim() || undefined,
        fuente: "agregador",
        perfil: `perfil-${slug}.json`,
        activo: true,
      });
      await ghPut(CFG.roster, roster, rFile.sha, `Registro: alta de ${slug}`);
    }

    // 2b) perfil-<slug>.json — arranca el perfil con la fecha de nacimiento (edad → FC máx
    //     estimada). Solo si aún no existe, para no pisar un perfil ya afinado a mano.
    const perfilPath = `tid-max/software/perfil-${slug}.json`;
    const pFile = await ghGet(perfilPath);
    if (!pFile.json) {
      const perfil = {
        _fuente: `Perfil de ${nom} — creado desde el alta en la app.`,
        atleta: nom,
        deporte: String(deporte || "").trim() || "otro",
        reloj: String(reloj || "").trim() || undefined,
        perfil: {
          fecha_nacimiento: nac,
          edad,
          fc_max_estimada: 220 - edad,
          sexo: null, peso_kg: null, altura_cm: null,
          fc_reposo: null, fc_max_carrera: null,
          vt1_fc: null, vt2_fc: null, fatmax_fc: null,
          _nota: "Zonas provisionales por edad (FC máx ≈ 220 − edad). Se recalibran con FC en reposo y una FC máx real medida.",
        },
        objetivos: [],
      };
      await ghPut(perfilPath, perfil, pFile.sha, `Perfil inicial de ${slug}`);
    }

    // 3) Token (auto-login).
    const exp = Math.floor(Date.now() / 1000) + TOKEN_TTL_S;
    const token = sign({ slug, exp }, authSecret);
    return res.status(200).json({ ok: true, token, slug, nombre: nom, exp });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
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

function sign(payload, secret) {
  const body = b64url(Buffer.from(JSON.stringify(payload), "utf8"));
  const sig = b64url(crypto.createHmac("sha256", secret).update(body).digest());
  return `${body}.${sig}`;
}

function b64url(buf) {
  return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

// --- GitHub "repo como BD" ---
function ghHeaders() {
  return {
    authorization: `Bearer ${process.env.GH_TOKEN}`,
    "user-agent": "tid-max-registro",
    accept: "application/vnd.github+json",
  };
}

async function ghGet(path) {
  const r = await fetch(`https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${path}?ref=${CFG.branch}`, {
    headers: ghHeaders(),
  });
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
    method: "PUT",
    headers: { ...ghHeaders(), "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("GitHub PUT " + r.status + ": " + (await r.text()).slice(0, 160));
}
