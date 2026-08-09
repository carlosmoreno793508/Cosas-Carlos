// Función serverless (Vercel) — Conexión "Evento objetivo" del app TID-MAX.
// Recibe el evento capturado en la app y lo commitea a tid-max/software/evento.json,
// que es la FUENTE DE VERDAD que el pipeline (build_evento en tid_data.py) ya lee para
// calcular días al evento y la fase (carga/taper/pico). Sin base de datos: "repo como BD",
// igual que api/comida.js.
//
// Variables de entorno (Vercel → Project → Settings → Environment Variables):
//   GH_TOKEN       — PAT fino con "Contents: Read and write" en el repo (para commitear).
//   UPLOAD_SECRET  — contraseña simple para que SOLO tú/la familia pueda escribir.
//   (opcionales) GH_OWNER, GH_REPO, GH_BRANCH, EVENTO_PATH.

const CFG = {
  owner: process.env.GH_OWNER || "carlosmoreno793508",
  repo: process.env.GH_REPO || "Cosas-Carlos",
  branch: process.env.GH_BRANCH || "main",
  path: process.env.EVENTO_PATH || "tid-max/software/evento.json",
};

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Usa POST." });
  try {
    const { secret, evento } = req.body || {};
    if (!process.env.UPLOAD_SECRET || secret !== process.env.UPLOAD_SECRET)
      return res.status(401).json({ error: "Contraseña incorrecta." });
    if (!evento || !evento.nombre || !String(evento.nombre).trim())
      return res.status(400).json({ error: "Falta el evento (al menos el nombre)." });

    const limpio = sanitize(evento);
    const commit = await commitEvento(limpio);
    return res.status(200).json({ ok: true, evento: limpio, commit });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}

// ---- Normaliza y valida el evento (no confiar en el cliente) ----
function sanitize(e) {
  const s = (v) => (v == null || v === "" ? null : String(v).slice(0, 200));
  const fecha = (v) => (/^\d{4}-\d{2}-\d{2}$/.test(v || "") ? v : null);
  return {
    nombre: s(e.nombre),
    tipo_deporte: s(e.tipo_deporte),
    prioridad: ["A", "B", "C"].includes(e.prioridad) ? e.prioridad : null,
    sede: s(e.sede),
    fecha_inicio: fecha(e.fecha_inicio),
    fecha_fin: fecha(e.fecha_fin),
    fecha_viaje: fecha(e.fecha_viaje),
    meta: s(e.meta),
    _nota:
      "Capturado desde la app TID-MAX (api/evento). Fuente de verdad del evento objetivo; " +
      "el pipeline calcula días y fase (carga/taper/pico).",
  };
}

// ---- Commit a software/evento.json vía GitHub API (crea o actualiza) ----
async function commitEvento(obj) {
  const api = `https://api.github.com/repos/${CFG.owner}/${CFG.repo}/contents/${CFG.path}`;
  const H = {
    authorization: `Bearer ${process.env.GH_TOKEN}`,
    "user-agent": "tid-max-evento",
    accept: "application/vnd.github+json",
  };

  // sha actual si el archivo ya existe (para actualizar). Si es 404, se crea nuevo.
  let sha;
  const g = await fetch(`${api}?ref=${CFG.branch}`, { headers: H });
  if (g.ok) sha = (await g.json()).sha;
  else if (g.status !== 404) throw new Error("GitHub GET " + g.status + ": " + (await g.text()).slice(0, 160));

  const content = Buffer.from(JSON.stringify(obj, null, 2) + "\n", "utf8").toString("base64");
  const body = { message: `Evento objetivo: ${obj.nombre}`, content, branch: CFG.branch };
  if (sha) body.sha = sha;

  const p = await fetch(api, {
    method: "PUT",
    headers: { ...H, "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!p.ok) throw new Error("GitHub PUT " + p.status + ": " + (await p.text()).slice(0, 160));
  const out = await p.json();
  return (out.commit && out.commit.sha) || null;
}
