// Función serverless (Vercel) — Receptor de WEBHOOKS de Junction (ex-Vital) · el "push".
//
// Junction EMPUJA un evento apenas descubre datos nuevos de un atleta (workout, sueño,
// recovery…). En vez de esperar al cron 2×/día, este endpoint recibe ese aviso y
// DISPARA el pipeline (workflow tid-max-daily) para que baje lo nuevo de Junction y
// regenere los reportes en minutos. Así el dato del atleta cae casi en vivo, sin que
// nadie corra nada a mano — el equivalente serverless de agregador_webhook.py.
//
// Seguridad: Junction firma con Svix. Verificamos la firma con JUNCTION_WEBHOOK_SECRET.
// Si ese secreto NO está configurado, respondemos 200 pero NO disparamos nada (para que
// un tercero no pueda provocar corridas del pipeline). Con el secreto puesto, solo los
// eventos con firma válida disparan.
//
// Env (Vercel → tid-max-app → Settings → Environment Variables):
//   JUNCTION_WEBHOOK_SECRET — el "Signing Secret" del webhook en el dashboard de Junction
//                             (formato whsec_...). Sin él, el endpoint es no-op seguro.
//   GH_ACTIONS_TOKEN        — PAT con permiso "Actions: write" para disparar el workflow.
//                             Si no está, cae a GH_PAT y luego a GH_TOKEN.
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, WORKFLOW_FILE.
//
// IMPORTANTE: necesitamos el cuerpo CRUDO para verificar la firma, así que apagamos el
// body parser de Vercel y lo leemos del stream nosotros mismos.

import crypto from "crypto";

export const config = { api: { bodyParser: false } };

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  workflow: process.env.WORKFLOW_FILE || "tid-max-daily.yml",
};

export default async function handler(req, res) {
  // Healthcheck simple (para probar que el endpoint responde desde el navegador).
  if (req.method === "GET") return res.status(200).json({ ok: true, servicio: "tidmax-webhook" });
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });

  try {
    const raw = await readRaw(req);
    const secret = (process.env.JUNCTION_WEBHOOK_SECRET || "").trim();

    // Sin secreto configurado: NO disparamos (evita abuso). Respondemos 200 para no
    // provocar reintentos infinitos de Junction mientras terminas de configurarlo.
    if (!secret) {
      console.warn("webhook: JUNCTION_WEBHOOK_SECRET no configurado — recibido pero IGNORADO.");
      return res.status(200).json({ received: true, dispatched: false, reason: "sin JUNCTION_WEBHOOK_SECRET" });
    }

    if (!verifySvix(secret, req.headers, raw)) {
      console.warn("webhook: firma Svix inválida — RECHAZADO.");
      return res.status(401).json({ error: "Firma inválida." });
    }

    let evento = {};
    try { evento = JSON.parse(raw.toString("utf8")); } catch { evento = {}; }
    const tipo = evento.event_type || evento.type || "evento";

    // Solo disparamos ante eventos que significan "hay datos nuevos" (o una conexión
    // recién hecha). Eventos de mero ciclo de vida no gatillan una corrida.
    if (!debeRefrescar(tipo)) {
      return res.status(200).json({ received: true, dispatched: false, tipo });
    }

    const dispatched = await dispararPipeline();
    return res.status(202).json({ received: true, dispatched, tipo });
  } catch (e) {
    console.error("webhook error:", (e && e.message) || e);
    // 200 para no desatar tormentas de reintentos; el cron diario es la red de seguridad.
    return res.status(200).json({ received: true, dispatched: false, error: String((e && e.message) || e) });
  }
}

// Lee el cuerpo crudo del request (necesario para verificar la firma).
async function readRaw(req) {
  const chunks = [];
  for await (const c of req) chunks.push(typeof c === "string" ? Buffer.from(c) : c);
  return Buffer.concat(chunks);
}

// ¿Este tipo de evento amerita re-sincronizar? Datos nuevos o una conexión recién hecha.
function debeRefrescar(tipo) {
  const t = String(tipo).toLowerCase();
  if (/(workout|sleep|activity|recovery|body|daily|historical|data)/.test(t)) return true;
  if (/(connection|connected)/.test(t)) return true;   // primera conexión → jala su histórico
  return false;
}

// Verificación de firma Svix (la que usa Junction). El header svix-signature trae una
// lista separada por espacios de "v1,<base64>". Se firma "<id>.<timestamp>.<body>" con
// HMAC-SHA256 usando la llave (el secreto whsec_ es base64 tras el prefijo).
function verifySvix(secret, headers, rawBody) {
  const h = lower(headers);
  const id = h["svix-id"] || h["webhook-id"] || "";
  const ts = h["svix-timestamp"] || h["webhook-timestamp"] || "";
  const sigHeader = h["svix-signature"] || h["webhook-signature"] || "";
  if (!id || !ts || !sigHeader) return false;

  // Tolerancia de reloj: rechaza timestamps de hace >5 min (anti-replay).
  const tsNum = Number(ts);
  if (!Number.isFinite(tsNum) || Math.abs(Date.now() / 1000 - tsNum) > 300) return false;

  const keyB64 = secret.startsWith("whsec_") ? secret.slice(6) : secret;
  let key;
  try { key = Buffer.from(keyB64, "base64"); } catch { return false; }

  const signed = `${id}.${ts}.${rawBody.toString("utf8")}`;
  const expected = crypto.createHmac("sha256", key).update(signed).digest("base64");
  const expBuf = Buffer.from(expected, "utf8");

  // El header puede traer varias firmas ("v1,xxx v1,yyy"); acepta si alguna cuadra.
  for (const part of sigHeader.split(" ")) {
    const comma = part.indexOf(",");
    const val = comma >= 0 ? part.slice(comma + 1) : part;
    const gotBuf = Buffer.from(val, "utf8");
    if (gotBuf.length === expBuf.length && crypto.timingSafeEqual(gotBuf, expBuf)) return true;
  }
  return false;
}

function lower(headers) {
  const out = {};
  for (const k of Object.keys(headers || {})) out[k.toLowerCase()] = headers[k];
  return out;
}

// Dispara el workflow tid-max-daily (workflow_dispatch) para bajar lo nuevo y regenerar.
async function dispararPipeline() {
  const tok = process.env.GH_ACTIONS_TOKEN || process.env.GH_PAT || process.env.GH_TOKEN;
  if (!tok) { console.warn("webhook: sin token para disparar el workflow (GH_ACTIONS_TOKEN)."); return false; }
  const url = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/actions/workflows/${CFG.workflow}/dispatches`;
  const r = await fetch(url, {
    method: "POST",
    headers: {
      authorization: `Bearer ${tok}`,
      "user-agent": "tid-max-webhook",
      accept: "application/vnd.github+json",
      "content-type": "application/json",
    },
    body: JSON.stringify({ ref: CFG.branch }),
  });
  if (r.status === 204) return true;
  console.warn("webhook: dispatch falló " + r.status + ": " + (await r.text()).slice(0, 160));
  return false;
}
