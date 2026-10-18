// Pages Function (Cloudflare) — Receptor de WEBHOOKS de Junction (el "push").
//
// Junction empuja un evento al descubrir datos nuevos; verificamos la firma Svix con
// JUNCTION_WEBHOOK_SECRET y disparamos el workflow tid-max-daily (workflow_dispatch).
// Sin secreto configurado, responde 200 pero NO dispara (no-op seguro). Portado de Vercel.
//
// Env: JUNCTION_WEBHOOK_SECRET (whsec_...), GH_ACTIONS_TOKEN (o GH_PAT/GH_TOKEN),
//   (opc) GH_OWNER/GH_REPO/GH_BRANCH/WORKFLOW_FILE.
// Requiere el compatibility flag: nodejs_compat.

import crypto from "node:crypto";
import { Buffer } from "node:buffer";

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method === "GET") return J({ ok: true, servicio: "tidmax-webhook" });
  if (request.method !== "POST") return J({ error: "Usa POST." }, 405);

  try {
    const raw = Buffer.from(await request.arrayBuffer());
    const secret = (env.JUNCTION_WEBHOOK_SECRET || "").trim();

    if (!secret) {
      console.warn("webhook: JUNCTION_WEBHOOK_SECRET no configurado — recibido pero IGNORADO.");
      return J({ received: true, dispatched: false, reason: "sin JUNCTION_WEBHOOK_SECRET" });
    }
    if (!verifySvix(secret, request.headers, raw)) {
      console.warn("webhook: firma Svix inválida — RECHAZADO.");
      return J({ error: "Firma inválida." }, 401);
    }

    let evento = {};
    try { evento = JSON.parse(raw.toString("utf8")); } catch { evento = {}; }
    const tipo = evento.event_type || evento.type || "evento";

    if (!debeRefrescar(tipo)) return J({ received: true, dispatched: false, tipo });

    const dispatched = await dispararPipeline(env);
    return J({ received: true, dispatched, tipo }, 202);
  } catch (e) {
    console.error("webhook error:", (e && e.message) || e);
    return J({ received: true, dispatched: false, error: String((e && e.message) || e) });
  }
}

function debeRefrescar(tipo) {
  const t = String(tipo).toLowerCase();
  if (/(workout|sleep|activity|recovery|body|daily|historical|data)/.test(t)) return true;
  if (/(connection|connected)/.test(t)) return true;
  return false;
}

// Verificación Svix. headers es un objeto Headers (get() es case-insensitive).
function verifySvix(secret, headers, rawBody) {
  const id = headers.get("svix-id") || headers.get("webhook-id") || "";
  const ts = headers.get("svix-timestamp") || headers.get("webhook-timestamp") || "";
  const sigHeader = headers.get("svix-signature") || headers.get("webhook-signature") || "";
  if (!id || !ts || !sigHeader) return false;

  const tsNum = Number(ts);
  if (!Number.isFinite(tsNum) || Math.abs(Date.now() / 1000 - tsNum) > 300) return false;

  const keyB64 = secret.startsWith("whsec_") ? secret.slice(6) : secret;
  let key;
  try { key = Buffer.from(keyB64, "base64"); } catch { return false; }

  const signed = `${id}.${ts}.${rawBody.toString("utf8")}`;
  const expected = crypto.createHmac("sha256", key).update(signed).digest("base64");
  const expBuf = Buffer.from(expected, "utf8");

  for (const part of sigHeader.split(" ")) {
    const comma = part.indexOf(",");
    const val = comma >= 0 ? part.slice(comma + 1) : part;
    const gotBuf = Buffer.from(val, "utf8");
    if (gotBuf.length === expBuf.length && crypto.timingSafeEqual(gotBuf, expBuf)) return true;
  }
  return false;
}

async function dispararPipeline(env) {
  const tok = env.GH_ACTIONS_TOKEN || env.GH_PAT || env.GH_TOKEN;
  if (!tok) { console.warn("webhook: sin token para disparar el workflow (GH_ACTIONS_TOKEN)."); return false; }
  const c = { owner: env.GH_OWNER || "carlosmoreno793508", repo: env.GH_REPO || "Cosas-Carlos", branch: env.GH_BRANCH || "main", workflow: env.WORKFLOW_FILE || "tid-max-daily.yml" };
  const url = `https://api.github.com/repos/${c.owner}/${c.repo}/actions/workflows/${c.workflow}/dispatches`;
  const r = await fetch(url, {
    method: "POST",
    headers: { authorization: `Bearer ${tok}`, "user-agent": "tid-max-webhook", accept: "application/vnd.github+json", "content-type": "application/json" },
    body: JSON.stringify({ ref: c.branch }),
  });
  if (r.status === 204) return true;
  console.warn("webhook: dispatch falló " + r.status + ": " + (await r.text()).slice(0, 160));
  return false;
}

function J(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "x-content-type-options": "nosniff" },
  });
}
