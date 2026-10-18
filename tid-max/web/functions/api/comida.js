// Pages Function (Cloudflare) — subir comida al dashboard de la familia (TID-MAX web).
//
// Recibe foto o texto, la estima con la visión de Claude y la registra en web/data.json
// (commit al repo -> Pages redespliega -> el tablero la muestra). "Repo como BD".
// Portado de la función serverless de Vercel; misma lógica, envoltorio Cloudflare.
//
// Env (Cloudflare Pages -> Settings -> Environment variables):
//   ANTHROPIC_API_KEY, GH_TOKEN, UPLOAD_SECRET, (opc) GH_OWNER/GH_REPO/GH_BRANCH/DATA_PATH/TID_MODEL.
// Requiere el compatibility flag: nodejs_compat (para Buffer).

import { Buffer } from "node:buffer";

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const body = await readJson(request);
    const { secret, texto, imageBase64, mediaType } = body;
    if (!env.UPLOAD_SECRET || secret !== env.UPLOAD_SECRET)
      return J({ error: "Contraseña incorrecta." }, 401);
    if (!imageBase64 && !(texto && texto.trim()))
      return J({ error: "Manda una foto o una descripción de la comida." }, 400);
    if (!env.ANTHROPIC_API_KEY) return J({ error: "Servidor sin ANTHROPIC_API_KEY." }, 503);
    if (!env.GH_TOKEN) return J({ error: "Servidor sin GH_TOKEN." }, 500);

    const est = await estimarComida(env, { texto, imageBase64, mediaType });
    const { total, meta } = await registrarEnData(env, est);
    return J({ ok: true, estimacion: est, total, meta });
  } catch (e) {
    return J({ error: String((e && e.message) || e) }, 500);
  }
}

async function estimarComida(env, { texto, imageBase64, mediaType }) {
  const model = env.TID_MODEL || "claude-opus-5";
  const content = [];
  if (imageBase64)
    content.push({ type: "image", source: { type: "base64", media_type: mediaType || "image/jpeg", data: imageBase64 } });
  content.push({
    type: "text",
    text:
      (texto && texto.trim() ? `El usuario describe la comida: "${texto.trim()}".\n` : "") +
      "Estima el platillo y sus macros. Responde SOLO un objeto JSON válido (sin texto extra, sin ```), con esta forma exacta:\n" +
      '{"platillo":"...","kcal":0,"prot_g":0,"carb_g":0,"grasa_g":0,"confianza":"alta|media|baja"}\n' +
      "Son estimaciones aproximadas para un atleta de rendimiento; usa enteros.",
  });

  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({
      model, max_tokens: 500,
      system: "Eres el agente de nutrición de TID-MAX. Estimas macros de comidas (foto o texto) para un atleta " +
        "de rendimiento con gasto alto. Nunca sugieres restringir. Respondes SOLO JSON.",
      messages: [{ role: "user", content }],
    }),
  });
  if (!r.ok) throw new Error("Claude " + r.status + ": " + (await r.text()).slice(0, 200));
  const data = await r.json();
  const txt = (data.content || []).map((c) => c.text || "").join("").trim();
  const json = txt.slice(txt.indexOf("{"), txt.lastIndexOf("}") + 1);
  const m = JSON.parse(json);
  return {
    platillo: String(m.platillo || "Comida"),
    kcal: Math.round(+m.kcal || 0), prot_g: Math.round(+m.prot_g || 0),
    carb_g: Math.round(+m.carb_g || 0), grasa_g: Math.round(+m.grasa_g || 0),
    confianza: m.confianza || "media",
  };
}

async function registrarEnData(env, est) {
  const c = { owner: env.GH_OWNER || "carlosmoreno793508", repo: env.GH_REPO || "Cosas-Carlos", branch: env.GH_BRANCH || "main", path: env.DATA_PATH || "tid-max/web/data.json" };
  const api = `https://api.github.com/repos/${c.owner}/${c.repo}/contents/${c.path}`;
  const H = { authorization: `Bearer ${env.GH_TOKEN}`, "user-agent": "tid-max-comida", accept: "application/vnd.github+json" };

  const g = await fetch(`${api}?ref=${c.branch}`, { headers: H });
  if (!g.ok) throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));
  const file = await g.json();
  const data = JSON.parse(Buffer.from(file.content, "base64").toString("utf8"));

  const nu = data.nutricion || (data.nutricion = { meta: 0, comidas: [] });
  nu.comidas = nu.comidas || [];
  const hora = new Date().toLocaleTimeString("es-MX", { hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "America/Mexico_City" });
  nu.comidas.push({ hora, nombre: est.platillo, kcal: est.kcal, prot_g: est.prot_g, carb_g: est.carb_g, grasa_g: est.grasa_g });
  nu.comidas.sort((a, b) => (a.hora || "").localeCompare(b.hora || ""));
  nu.consumido = nu.comidas.reduce((s, x) => s + (x.kcal || 0), 0);
  nu.c = nu.comidas.reduce((s, x) => s + (x.carb_g || 0), 0);
  nu.p = nu.comidas.reduce((s, x) => s + (x.prot_g || 0), 0);
  nu.g = nu.comidas.reduce((s, x) => s + (x.grasa_g || 0), 0);
  nu.pendiente = null;

  const nuevo = Buffer.from(JSON.stringify(data, null, 2) + "\n", "utf8").toString("base64");
  const p = await fetch(api, {
    method: "PUT", headers: { ...H, "content-type": "application/json" },
    body: JSON.stringify({ message: `Comida registrada: ${est.platillo} (${est.kcal} kcal)`, content: nuevo, sha: file.sha, branch: c.branch }),
  });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
  return { total: nu.consumido, meta: nu.meta };
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
