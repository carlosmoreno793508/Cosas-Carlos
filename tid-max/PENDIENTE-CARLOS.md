# Pendiente de Carlos — para cerrar "todo por la app" 🌅

Buenos días. Anoche dejamos **funcionando** el flujo *"conectar una fuente desde la app,
cero Mac"* (probado en tu iPhone → "Success"). Faltan 2-3 pasos que **solo tú puedes hacer**
porque llevan tus llaves. Cada uno es de ~2-5 min.

---

## 1) Que el "Continue" regrese a la app  ✅ (ya lo dejé cableado)
Anoche el botón "Continue" del widget se congelaba. Ya le puse un `redirect_url`: ahora el
widget **regresa solo a la app** con un aviso "✅ Marca conectada". No tienes que hacer nada —
solo pruébalo de nuevo (Datos → Conectar → conecta → Continue → te regresa).

---

## 2) Persistir QUIÉN conectó (para el sync automático)  ← **tú, ~3 min**
Hoy el connect funciona pero **no guarda** el mapeo atleta→usuario (falta un token de GitHub).

**Qué hacer:**
1. Crea un **GitHub Personal Access Token (fine-grained)**:
   github.com → Settings → Developer settings → *Fine-grained tokens* → *Generate new token*
   - Repo: `carlosmoreno793508/Cosas-Carlos`
   - Permiso: **Contents → Read and write**
   - Copia el token (`github_pat_...`)
2. En **Vercel → tid-max-app → Environment Variables → Add**:
   - `GH_TOKEN` = (el token) · **All Environments** · Save
3. Avísame y redeployeo. Con esto, cada "Conectar" guarda el mapeo en
   `software/agregador_users.json` (no lleva secretos, solo el id del usuario).

---

## 3) Prender el sync automático en la nube  ← **tú, ~3 min**  (Paso 2)
El cron de GitHub Actions ya **está listo** para bajar del agregador — solo necesita las llaves
como *secrets* del repo (los secrets de Vercel NO los ve GitHub Actions, son aparte).

**Qué hacer:** GitHub → repo `Cosas-Carlos` → **Settings → Secrets and variables → Actions →
New repository secret**, y agrega estos 4 (los mismos valores de Vercel):
- `JUNCTION_API_KEY`  = `sk_us_...`
- `JUNCTION_API_BASE` = `https://api.sandbox.us.junction.com`
- `JUNCTION_ENV`      = `sandbox`
- `JUNCTION_REGION`   = `us`

Luego pruébalo a mano: pestaña **Actions → "TID-MAX · reporte diario" → Run workflow**.
Si no hay atletas conectados todavía, se omite sin romper nada.

---

## 4) Cuando quieras datos REALES de un reloj  ← después
Ahora estás en **sandbox** (datos simulados). Para dato real de tu WHOOP/Polar:
- En Junction: crea llaves de **Production** (mismo dashboard, pestaña Production).
- Cambia en Vercel (y en los secrets de Actions): `JUNCTION_ENV=production` y las llaves/base de prod.
- Reconecta la fuente desde la app (esta vez conecta tu cuenta real).

---

## Estado del PR
Todo va en el **PR #9** (rama `claude/smartwatch-analysis-9eua05`). Cuando validemos el sync
end-to-end, lo mergeamos a `main` y queda en producción (`tid-max-app.vercel.app`).

**Orden sugerido:** 2 → 3 → probar Run workflow. Cualquier cosa, me dices y seguimos. 💪
