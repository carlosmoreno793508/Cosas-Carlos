// Función serverless (Vercel) — Registro de COMIDA del app TID-MAX (agente de nutrición).
//
// El atleta toma una FOTO del plato (o lo describe en TEXTO) desde el teléfono; este
// endpoint estima el platillo y sus macros con la VISIÓN de Claude, usando el perfil de
// nutrición del atleta (nutricion-<slug>.json, incluyendo su estrategia de AYUNO si la
// tiene), y SUMA la comida al consumo del día en el repo ("repo como BD", igual que
// api/evento.js). El pipeline (tid_multi.py) copia ese consumo a la carpeta del atleta
// para que el reporte muestre "consumido vs meta".
//
// Espeja la lógica de software/tid_nutricion.py, pero servida por-usuario desde la app.
//
// Autenticación: token de sesión (HMAC, igual que /api/evento y /api/run).
//
// Env (Vercel → tid-max-app → Settings → Environment Variables):
//   ANTHROPIC_API_KEY — para la estimación por visión/texto (SIN ella, responde 503).
//   AUTH_SECRET       — la MISMA con que /api/login firma los tokens.
//   GH_TOKEN          — PAT fino con "Contents: Read and write".
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, CONSUMO_DIR, NUTRI_DIR, REPORTES_DIR, COMIDA_MODEL.

import crypto from "crypto";

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  consumoDir: process.env.CONSUMO_DIR || "tid-max/software/consumo",       // consumo del día por-atleta (lo escribe la app)
  nutriDir: process.env.NUTRI_DIR || "tid-max/software",                   // nutricion-<slug>.json
  reportesDir: process.env.REPORTES_DIR || "tid-max/software/reportes",    // reportes/<slug>.json (para la meta)
  model: process.env.COMIDA_MODEL || "claude-opus-5",
};

const PERSONA =
  "Eres el agente de nutrición de TID-MAX para atletas de rendimiento. Estimas, a partir de una foto o " +
  "una descripción, qué comió el atleta y sus macros aproximados. Las cantidades de una foto son " +
  "ESTIMADAS: da tu mejor número pero con confianza honesta, sin fingir precisión. Cuentas explícitamente " +
  "el aceite/salsas (suelen subestimarse) y, si el plato es mezclado, lo descompones por componentes antes " +
  "de sumar. Hablas español, claro y breve. NO das consejo médico.";

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    if (!process.env.GH_TOKEN) return res.status(500).json({ error: "Servidor sin GH_TOKEN." });
    if (!process.env.ANTHROPIC_API_KEY) return res.status(503).json({ error: "Servidor sin ANTHROPIC_API_KEY (falta configurar en Vercel)." });
    const secret = process.env.AUTH_SECRET || "";
    if (!secret) return res.status(500).json({ error: "Servidor sin AUTH_SECRET." });

    const body = req.body || {};
    const token = body.token ||
      ((req.headers.authorization || "").startsWith("Bearer ") ? req.headers.authorization.slice(7).trim() : "");
    const payload = token ? verify(token, secret) : null;
    if (!payload) return res.status(401).json({ error: "Necesitas iniciar sesión." });
    const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
    if (!slug) return res.status(400).json({ error: "Token sin atleta." });

    const texto = body.texto ? String(body.texto).slice(0, 500) : "";
    let media = null, data = null;
    if (body.foto) {
      const m = String(body.foto).match(/^data:(image\/[a-zA-Z0-9.+-]+);base64,(.*)$/s);
      if (m) { media = m[1]; data = m[2]; }
      else { media = body.media || "image/jpeg"; data = String(body.foto); }
    }
    if (!data && !texto) return res.status(400).json({ error: "Manda una foto o una descripción de la comida." });
    const hora = /^\d{1,2}:\d{2}$/.test(body.hora || "") ? body.hora : null;

    // Contexto por-atleta: perfil de nutrición (con AYUNO) + meta del día (del reporte).
    const perfil = await ghReadJson(`${CFG.nutriDir}/nutricion-${slug}.json`);
    const reporte = await ghReadJson(`${CFG.reportesDir}/${slug}.json`);
    const meta = metaDe(reporte && reporte.obj);
    const contexto = construirContexto(perfil && perfil.obj, meta);

    // --- Estimación con Claude (visión o texto) ---
    const est = await estimar({ media, data, texto, contexto });

    // --- Suma al consumo del día (repo como BD) ---
    const consumo = await registrarConsumo(slug, est, data ? "foto" : "texto", hora, meta);

    return res.status(200).json({ ok: true, estimacion: est, consumo });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

function metaDe(rep) {
  const n = (rep && rep.nutricion) || {};
  if (n.meta == null && n.c == null) return null;
  return { kcal: n.meta || null, carb_g: n.c || null, prot_g: n.p || null, grasa_g: n.g || null };
}

function construirContexto(perfil, meta) {
  let t = "";
  if (meta && meta.kcal) t += `Meta del día del atleta: ~${meta.kcal} kcal` +
    (meta.carb_g ? ` · C ${meta.carb_g} g` : "") + (meta.prot_g ? ` · P ${meta.prot_g} g` : "") + ". ";
  if (perfil) {
    const obj = perfil.objetivo_nutricional || {};
    if (obj.prioridad_1) t += `Objetivo nutricional: ${obj.prioridad_1} `;
    const ay = perfil.ayuno || {};
    if (ay.activo) {
      t += `\nAYUNO (estrategia de este atleta): ${ay.tipo || "ayuno intermitente"}`;
      if (ay.ventana_alimentacion) t += `, ventana ${ay.ventana_alimentacion}`;
      t += ". Comenta con tacto si la comida cae fuera de la ventana; nunca sugieras sub-alimentar una sesión clave.";
    }
    if (perfil.alimentos_preferidos) t += `\nSuele comer: ${JSON.stringify(perfil.alimentos_preferidos).slice(0, 500)}`;
  }
  return t;
}

const INSTR =
  "Estima el platillo, sus alimentos y macros. Responde SOLO con un objeto JSON válido (sin markdown, sin texto extra) " +
  "con EXACTAMENTE estas claves: {\"platillo\": string, \"alimentos\": string[], \"kcal\": number, \"prot_g\": number, " +
  "\"carb_g\": number, \"grasa_g\": number, \"confianza\": \"alta\"|\"media\"|\"baja\", \"cubre_demanda\": string (1 frase), " +
  "\"sugerencia\": string (1 frase, sin restringir)}. Números enteros. Cuenta aceite/salsas.";

async function estimar({ media, data, texto, contexto }) {
  const content = [];
  if (data) content.push({ type: "image", source: { type: "base64", media_type: media, data } });
  const userText = (contexto ? contexto + "\n\n" : "") +
    (texto ? `El atleta comió (descrito por el usuario): "${texto}".\n\n` : "") + INSTR;
  content.push({ type: "text", text: userText });

  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({ model: CFG.model, max_tokens: 900, system: PERSONA, messages: [{ role: "user", content }] }),
  });
  if (!r.ok) throw new Error("Claude " + r.status + ": " + (await r.text()).slice(0, 200));
  const j = await r.json();
  const txt = (j.content || []).filter((b) => b.type === "text").map((b) => b.text).join("").trim();
  return parseEst(txt);
}

function parseEst(txt) {
  let s = txt.replace(/^```(?:json)?/i, "").replace(/```$/, "").trim();
  const a = s.indexOf("{"), b = s.lastIndexOf("}");
  if (a >= 0 && b > a) s = s.slice(a, b + 1);
  let o;
  try { o = JSON.parse(s); } catch { throw new Error("No pude leer la estimación del modelo."); }
  const num = (v) => Math.max(0, Math.round(Number(v) || 0));
  return {
    platillo: String(o.platillo || "Comida").slice(0, 120),
    alimentos: Array.isArray(o.alimentos) ? o.alimentos.slice(0, 12).map((x) => String(x).slice(0, 80)) : [],
    kcal: num(o.kcal), prot_g: num(o.prot_g), carb_g: num(o.carb_g), grasa_g: num(o.grasa_g),
    confianza: ["alta", "media", "baja"].includes(o.confianza) ? o.confianza : "media",
    cubre_demanda: String(o.cubre_demanda || "").slice(0, 240),
    sugerencia: String(o.sugerencia || "").slice(0, 240),
  };
}

async function registrarConsumo(slug, est, origen, hora, meta) {
  const path = `${CFG.consumoDir}/${slug}.json`;
  const hoy = new Date().toISOString().slice(0, 10);
  const cur = await ghReadJson(path);
  let doc = (cur && cur.obj) || {};
  if (doc.fecha !== hoy) doc = { fecha: hoy, comidas: [] };
  if (!Array.isArray(doc.comidas)) doc.comidas = [];
  doc.comidas.push({
    hora: hora || new Date().toISOString().slice(11, 16),
    platillo: est.platillo, kcal: est.kcal, prot_g: est.prot_g, carb_g: est.carb_g, grasa_g: est.grasa_g,
    origen,
  });
  doc.comidas.sort((a, b) => (a.hora || "").localeCompare(b.hora || ""));
  const tot = { kcal: 0, prot_g: 0, carb_g: 0, grasa_g: 0 };
  for (const c of doc.comidas) for (const k of Object.keys(tot)) tot[k] += c[k] || 0;
  doc.totales = tot;
  if (meta) doc.meta = meta;
  doc.slug = slug;
  await ghWriteJson(path, doc, `Comida de ${slug}: ${est.platillo} (${est.kcal} kcal)`, cur && cur.sha);
  return doc;
}

// ---- Token HMAC (igual que /api/evento) ----
function verify(token, secret) {
  if (!token) return null;
  const dot = token.lastIndexOf(".");
  if (dot < 1) return null;
  const bodyB = token.slice(0, dot), sig = token.slice(dot + 1);
  const esperado = b64url(crypto.createHmac("sha256", secret).update(bodyB).digest());
  const a = Buffer.from(sig, "utf8"), b = Buffer.from(esperado, "utf8");
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let payload;
  try { payload = JSON.parse(Buffer.from(bodyB.replace(/-/g, "+").replace(/_/g, "/"), "base64").toString("utf8")); }
  catch { return null; }
  if (!payload || typeof payload.exp !== "number" || payload.exp < Math.floor(Date.now() / 1000)) return null;
  return payload;
}
function b64url(buf) { return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }

// ---- GitHub helpers ----
function ghHeaders() {
  return { authorization: `Bearer ${process.env.GH_TOKEN}`, "user-agent": "tid-max-comida", accept: "application/vnd.github+json" };
}
async function ghReadJson(path) {
  const api = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${path}?ref=${CFG.branch}`;
  const g = await fetch(api, { headers: ghHeaders() });
  if (g.status === 404) return null;
  if (!g.ok) throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));
  const j = await g.json();
  try { return { obj: JSON.parse(Buffer.from(j.content, "base64").toString("utf8")), sha: j.sha }; }
  catch { return { obj: null, sha: j.sha }; }
}
async function ghWriteJson(path, obj, message, sha) {
  const api = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${path}`;
  const content = Buffer.from(JSON.stringify(obj, null, 2) + "\n", "utf8").toString("base64");
  const reqBody = { message, content, branch: CFG.branch };
  if (sha) reqBody.sha = sha;
  const p = await fetch(api, { method: "PUT", headers: { ...ghHeaders(), "content-type": "application/json" }, body: JSON.stringify(reqBody) });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
  return ((await p.json()).commit || {}).sha || null;
}
