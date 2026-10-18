// Pages Function (Cloudflare) — Registro de COMIDA (agente de nutrición, TID-MAX).
//
// Foto o texto -> estima platillo y macros con la VISIÓN de Claude usando el perfil de
// nutrición del atleta (nutricion-<slug>.json, incl. AYUNO) y SUMA al consumo del día
// ("repo como BD"). Portado de Vercel; misma lógica, envoltorio Cloudflare.
//
// Env: ANTHROPIC_API_KEY (sin ella -> 503), AUTH_SECRET, GH_TOKEN,
//   (opc) GH_OWNER/GH_REPO/GH_BRANCH/CONSUMO_DIR/NUTRI_DIR/REPORTES_DIR/COMIDA_MODEL.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

const PERSONA =
  "Eres el agente de nutrición de TID-MAX para atletas de rendimiento. Estimas, a partir de una foto o " +
  "una descripción, qué comió el atleta y sus macros aproximados. Las cantidades de una foto son " +
  "ESTIMADAS: da tu mejor número pero con confianza honesta, sin fingir precisión. Cuentas explícitamente " +
  "el aceite/salsas (suelen subestimarse) y, si el plato es mezclado, lo descompones por componentes antes " +
  "de sumar. Hablas español, claro y breve. NO das consejo médico.";

const INSTR =
  "Estima el platillo, sus alimentos y macros. Responde SOLO con un objeto JSON válido (sin markdown, sin texto extra) " +
  "con EXACTAMENTE estas claves: {\"platillo\": string, \"alimentos\": string[], \"kcal\": number, \"prot_g\": number, " +
  "\"carb_g\": number, \"grasa_g\": number, \"confianza\": \"alta\"|\"media\"|\"baja\", \"cubre_demanda\": string (1 frase), " +
  "\"sugerencia\": string (1 frase, sin restringir)}. Números enteros. Cuenta aceite/salsas.";

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    if (!env.GH_TOKEN) return J({ error: "Servidor sin GH_TOKEN." }, 500);
    if (!env.ANTHROPIC_API_KEY) return J({ error: "Servidor sin ANTHROPIC_API_KEY (falta configurar en Cloudflare)." }, 503);
    const secret = env.AUTH_SECRET || "";
    if (!secret) return J({ error: "Servidor sin AUTH_SECRET." }, 500);

    const body = await readJson(request);
    const token = tokenFrom(request, body);
    const payload = token ? verify(token, secret) : null;
    if (!payload) return J({ error: "Necesitas iniciar sesión." }, 401);
    const slug = String(payload.slug || "").replace(/[^a-z0-9-]/g, "");
    if (!slug) return J({ error: "Token sin atleta." }, 400);

    const texto = body.texto ? String(body.texto).slice(0, 500) : "";
    let media = null, data = null;
    if (body.foto) {
      const m = String(body.foto).match(/^data:(image\/[a-zA-Z0-9.+-]+);base64,(.*)$/s);
      if (m) { media = m[1]; data = m[2]; }
      else { media = body.media || "image/jpeg"; data = String(body.foto); }
    }
    if (!data && !texto) return J({ error: "Manda una foto o una descripción de la comida." }, 400);
    const hora = /^\d{1,2}:\d{2}$/.test(body.hora || "") ? body.hora : null;

    const nutriDir = env.NUTRI_DIR || "tid-max/software";
    const reportesDir = env.REPORTES_DIR || "tid-max/software/reportes";
    const consumoDir = env.CONSUMO_DIR || "tid-max/software/consumo";
    const model = env.COMIDA_MODEL || "claude-opus-5";

    const perfil = await ghReadJson(env, `${nutriDir}/nutricion-${slug}.json`);
    const reporte = await ghReadJson(env, `${reportesDir}/${slug}.json`);
    const meta = metaDe(reporte && reporte.obj);
    const contexto = construirContexto(perfil && perfil.obj, meta);

    const est = await estimar(env, { media, data, texto, contexto, model });
    const consumo = await registrarConsumo(env, consumoDir, slug, est, data ? "foto" : "texto", hora, meta);

    return J({ ok: true, estimacion: est, consumo });
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
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

async function estimar(env, { media, data, texto, contexto, model }) {
  const content = [];
  if (data) content.push({ type: "image", source: { type: "base64", media_type: media, data } });
  const userText = (contexto ? contexto + "\n\n" : "") +
    (texto ? `El atleta comió (descrito por el usuario): "${texto}".\n\n` : "") + INSTR;
  content.push({ type: "text", text: userText });

  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model, max_tokens: 900, system: PERSONA, messages: [{ role: "user", content }] }),
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

async function registrarConsumo(env, consumoDir, slug, est, origen, hora, meta) {
  const path = `${consumoDir}/${slug}.json`;
  const hoy = new Date().toISOString().slice(0, 10);
  const cur = await ghReadJson(env, path);
  let doc = (cur && cur.obj) || {};
  if (doc.fecha !== hoy) doc = { fecha: hoy, comidas: [] };
  if (!Array.isArray(doc.comidas)) doc.comidas = [];
  doc.comidas.push({
    hora: hora || new Date().toISOString().slice(11, 16),
    platillo: est.platillo, kcal: est.kcal, prot_g: est.prot_g, carb_g: est.carb_g, grasa_g: est.grasa_g, origen,
  });
  doc.comidas.sort((a, b) => (a.hora || "").localeCompare(b.hora || ""));
  const tot = { kcal: 0, prot_g: 0, carb_g: 0, grasa_g: 0 };
  for (const c of doc.comidas) for (const k of Object.keys(tot)) tot[k] += c[k] || 0;
  doc.totales = tot;
  if (meta) doc.meta = meta;
  doc.slug = slug;
  await ghWriteJson(env, path, doc, `Comida de ${slug}: ${est.platillo} (${est.kcal} kcal)`, cur && cur.sha);
  return doc;
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
function ghHeaders(env) {
  return { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": "tid-max-comida", accept: "application/vnd.github+json" };
}
async function ghReadJson(env, path) {
  const c = cfg(env);
  const g = await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/${path}?ref=${c.branch}`, { headers: ghHeaders(env) });
  if (g.status === 404) return null;
  if (!g.ok) throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));
  const j = await g.json();
  try { return { obj: JSON.parse(Buffer.from(j.content, "base64").toString("utf8")), sha: j.sha }; }
  catch { return { obj: null, sha: j.sha }; }
}
async function ghWriteJson(env, path, obj, message, sha) {
  const c = cfg(env);
  const content = Buffer.from(JSON.stringify(obj, null, 2) + "\n", "utf8").toString("base64");
  const reqBody = { message, content, branch: c.branch };
  if (sha) reqBody.sha = sha;
  const p = await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/${path}`, {
    method: "PUT", headers: { ...ghHeaders(env), "content-type": "application/json" }, body: JSON.stringify(reqBody),
  });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
  return ((await p.json()).commit || {}).sha || null;
}
