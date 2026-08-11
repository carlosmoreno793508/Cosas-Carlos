// Función serverless (Vercel) — Conectar una FUENTE desde la app TID-MAX.
// Reemplaza el paso de la Mac (polar_auth.py / agregador_connect.py): el atleta
// pica "Conectar" en el teléfono -> esta función crea (o reusa) su usuario en
// Junction (ex-Vital), genera un "link token" y devuelve la URL del widget
// "Conéctate" (con logos). El atleta hace login en SU marca ahí mismo.
//
// Guarda el mapeo atleta -> user_id en tid-max/software/agregador_users.json
// ("repo como BD", igual que api/evento.js) para que el sync en la nube (paso 2)
// sepa a quién bajarle datos. Ese archivo NO lleva tokens secretos (los tokens
// viven en Junction); solo el user_id/client_user_id, que sin la API key no sirven.
//
// Variables de entorno (Vercel → Project → Settings → Environment Variables):
//   JUNCTION_API_KEY   — de tu dashboard https://app.junction.com > API Keys.
//   JUNCTION_API_BASE  — la base EXACTA de tu dashboard (default sandbox US).
//   JUNCTION_LINK_BASE — base del widget (default https://link.junction.com).
//   JUNCTION_ENV       — sandbox | production (default sandbox).
//   JUNCTION_REGION    — us | eu (default us).
//   GH_TOKEN           — PAT fino con "Contents: Read and write" (para el mapeo).
//   UPLOAD_SECRET      — la MISMA clave de sincronización de la familia.
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, AGREGADOR_USERS_PATH.

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  path: process.env.AGREGADOR_USERS_PATH || "tid-max/software/agregador_users.json",
};

const JCFG = {
  apiKey: process.env.JUNCTION_API_KEY || "",
  apiBase: (process.env.JUNCTION_API_BASE || "https://api.sandbox.us.junction.com").replace(/\/+$/, ""),
  linkBase: (process.env.JUNCTION_LINK_BASE || "https://link.tryvital.io").replace(/\/+$/, ""),
  env: process.env.JUNCTION_ENV || "sandbox",
  region: process.env.JUNCTION_REGION || "us",
};

const PROVIDERS = ["whoop", "polar", "strava", "garmin", "oura", "fitbit"];

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const { secret, atleta, provider } = req.body || {};
    if (!process.env.UPLOAD_SECRET)
      return res.status(401).json({ error: "Servidor sin UPLOAD_SECRET (variable no cargada en este deploy)." });
    if (secret !== process.env.UPLOAD_SECRET)
      return res.status(401).json({ error: "Clave de sincronización incorrecta (no coincide con UPLOAD_SECRET)." });
    if (!JCFG.apiKey)
      return res.status(500).json({ error: "Falta JUNCTION_API_KEY en las variables de entorno de Vercel." });

    const slug = slugify(atleta);
    if (!slug) return res.status(400).json({ error: "Falta el atleta." });
    const prov = provider && PROVIDERS.includes(String(provider).toLowerCase())
      ? String(provider).toLowerCase() : null;

    const userId = await junctionUser(slug);
    // A dónde regresa el widget al terminar ("Continue"): de vuelta a la app.
    const origin = req.headers.origin || (req.headers.host ? `https://${req.headers.host}` : "");
    const redirectUrl = origin ? `${origin}/?connected=${encodeURIComponent(prov || "ok")}` : null;
    const link = await junctionLinkToken(userId, prov, redirectUrl);
    // Junction devuelve la URL lista del widget (link_web_url). La usamos tal cual
    // (a prueba de rebrands/dominios). Solo si no viene, la armamos como respaldo.
    const widgetUrl = link.link_web_url
      || `${JCFG.linkBase}/?token=${encodeURIComponent(link.link_token)}&env=${JCFG.env}&region=${JCFG.region}`;

    // Guardar el mapeo es "mejor esfuerzo": si falta GH_TOKEN o falla el commit,
    // NO bloqueamos la conexion (el widget se abre igual). El mapeo se necesita
    // para el sync en la nube (paso 2), no para conectar.
    let mappingSaved = false;
    try {
      await guardarMapeo(slug, userId);
      mappingSaved = true;
    } catch (e) {
      console.error("guardarMapeo (no fatal):", (e && e.message) || e);
    }

    return res.status(200).json({ ok: true, atleta: slug, provider: prov, user_id: userId, widget_url: widgetUrl, mapping_saved: mappingSaved });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

function slugify(v) {
  return String(v || "").trim().toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40);
}

function jhdr() {
  return { "x-vital-api-key": JCFG.apiKey, "content-type": "application/json", accept: "application/json" };
}

// Crea (o reusa) el usuario en Junction; devuelve su user_id.
async function junctionUser(slug) {
  const clientUserId = `tidmax-${slug}`;
  const r = await fetch(`${JCFG.apiBase}/v2/user`, {
    method: "POST", headers: jhdr(), body: JSON.stringify({ client_user_id: clientUserId }),
  });
  if (r.ok) return (await r.json()).user_id;
  if (r.status === 400 || r.status === 409) {
    // Ya existe: resolver por client_user_id.
    const g = await fetch(`${JCFG.apiBase}/v2/user/resolve/${encodeURIComponent(clientUserId)}`, { headers: jhdr() });
    if (g.ok) return (await g.json()).user_id;
  }
  throw new Error("Junction /v2/user " + r.status + ": " + (await r.text()).slice(0, 160));
}

// Genera el link token para abrir el widget "Conéctate".
// Intenta con redirect_url (para que "Continue" regrese a la app); si la API lo
// rechaza, reintenta SIN el, para nunca romper el flujo que ya funciona.
async function junctionLinkToken(userId, provider, redirectUrl) {
  const base = { user_id: userId };
  if (provider) base.provider = provider;
  const intentos = redirectUrl ? [{ ...base, redirect_url: redirectUrl }, base] : [base];
  let lastErr = "";
  for (const body of intentos) {
    const r = await fetch(`${JCFG.apiBase}/v2/link/token`, {
      method: "POST", headers: jhdr(), body: JSON.stringify(body),
    });
    if (r.ok) return await r.json();  // { link_token, link_web_url? }
    lastErr = r.status + ": " + (await r.text()).slice(0, 160);
  }
  throw new Error("Junction /v2/link/token " + lastErr);
}

// Commit del mapeo atleta -> user_id a agregador_users.json (crea o actualiza, merge).
async function guardarMapeo(slug, userId) {
  const api = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${CFG.path}`;
  const H = { authorization: `Bearer ${process.env.GH_TOKEN}`, "user-agent": "tid-max-connect", accept: "application/vnd.github+json" };

  let sha, store = {};
  const g = await fetch(`${api}?ref=${CFG.branch}`, { headers: H });
  if (g.ok) {
    const j = await g.json();
    sha = j.sha;
    try { store = JSON.parse(Buffer.from(j.content, "base64").toString("utf8")) || {}; } catch { store = {}; }
  } else if (g.status !== 404) {
    throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));
  }

  store[slug] = { user_id: userId, client_user_id: `tidmax-${slug}`, env: JCFG.env };
  const content = Buffer.from(JSON.stringify(store, null, 2) + "\n", "utf8").toString("base64");
  const body = { message: `Agregador: conectar ${slug}`, content, branch: CFG.branch };
  if (sha) body.sha = sha;

  const p = await fetch(api, { method: "PUT", headers: { ...H, "content-type": "application/json" }, body: JSON.stringify(body) });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
}
