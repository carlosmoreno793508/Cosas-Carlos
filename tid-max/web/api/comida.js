// Función serverless (Vercel) — Fase 3 del ecosistema TID-MAX.
// Recibe una FOTO o TEXTO de comida, la estima con Claude (visión) y la registra en el
// consumo del día dentro de web/data.json (commit al repo → Vercel redespliega → el
// tablero la muestra). Sin base de datos: reusa el "repo como base de datos".
//
// Variables de entorno (Vercel → Project → Settings → Environment Variables):
//   ANTHROPIC_API_KEY  — clave de Claude (Anthropic).
//   GH_TOKEN           — PAT fino con permiso "Contents: Read and write" en el repo (para commitear data.json).
//   UPLOAD_SECRET      — contraseña simple para que SOLO la familia pueda subir comidas.
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, DATA_PATH, TID_MODEL.

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  path: process.env.DATA_PATH || "tid-max/web/data.json",
  model: process.env.TID_MODEL || "claude-opus-5",
};

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const { secret, texto, imageBase64, mediaType } = req.body || {};
    if (!process.env.UPLOAD_SECRET || secret !== process.env.UPLOAD_SECRET)
      return res.status(401).json({ error: "Contraseña incorrecta." });
    if (!imageBase64 && !(texto && texto.trim()))
      return res.status(400).json({ error: "Manda una foto o una descripción de la comida." });

    const est = await estimarComida({ texto, imageBase64, mediaType });
    const { total, meta } = await registrarEnData(est);
    return res.status(200).json({ ok: true, estimacion: est, total, meta });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

// ---- 1) Estimación con Claude (visión o texto) ----
async function estimarComida({ texto, imageBase64, mediaType }) {
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
    headers: {
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: CFG.model,
      max_tokens: 500,
      system:
        "Eres el agente de nutrición de TID-MAX. Estimas macros de comidas (foto o texto) para un atleta " +
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
    kcal: Math.round(+m.kcal || 0),
    prot_g: Math.round(+m.prot_g || 0),
    carb_g: Math.round(+m.carb_g || 0),
    grasa_g: Math.round(+m.grasa_g || 0),
    confianza: m.confianza || "media",
  };
}

// ---- 2) Registrar en web/data.json (commit al repo) ----
async function registrarEnData(est) {
  const api = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${CFG.path}`;
  const H = { authorization: `Bearer ${process.env.GH_TOKEN}`, "user-agent": "tid-max-comida", accept: "application/vnd.github+json" };

  const g = await fetch(`${api}?ref=${CFG.branch}`, { headers: H });
  if (!g.ok) throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));
  const file = await g.json();
  const data = JSON.parse(Buffer.from(file.content, "base64").toString("utf8"));

  const nu = data.nutricion || (data.nutricion = { meta: 0, comidas: [] });
  nu.comidas = nu.comidas || [];
  const hora = new Date().toLocaleTimeString("es-MX", {
    hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "America/Mexico_City",
  });
  nu.comidas.push({ hora, nombre: est.platillo, kcal: est.kcal, prot_g: est.prot_g, carb_g: est.carb_g, grasa_g: est.grasa_g });
  nu.comidas.sort((a, b) => (a.hora || "").localeCompare(b.hora || ""));
  // Recalcular totales del día desde las comidas (idempotente).
  nu.consumido = nu.comidas.reduce((s, c) => s + (c.kcal || 0), 0);
  nu.c = nu.comidas.reduce((s, c) => s + (c.carb_g || 0), 0);
  nu.p = nu.comidas.reduce((s, c) => s + (c.prot_g || 0), 0);
  nu.g = nu.comidas.reduce((s, c) => s + (c.grasa_g || 0), 0);
  nu.pendiente = null;

  const nuevo = Buffer.from(JSON.stringify(data, null, 2) + "\n", "utf8").toString("base64");
  const p = await fetch(api, {
    method: "PUT",
    headers: { ...H, "content-type": "application/json" },
    body: JSON.stringify({
      message: `Comida registrada: ${est.platillo} (${est.kcal} kcal)`,
      content: nuevo,
      sha: file.sha,
      branch: CFG.branch,
    }),
  });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
  return { total: nu.consumido, meta: nu.meta };
}
