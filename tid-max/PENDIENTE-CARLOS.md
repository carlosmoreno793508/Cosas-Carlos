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

## 2) Persistir QUIÉN conectó  ✅ HECHO (2026-08-11)
Ya creaste el `GH_TOKEN` y lo pusiste en Vercel. **Confirmado funcionando:** el mapeo se
guardó en `software/agregador_users.json` (atleta `carlos-gael-moreno-sarmiento` → user_id).

## 2b) Habilitar WHOOP (es "Bring Your Own OAuth")  ← **tú, ~10 min**  (opcional)
WHOOP abrió en blanco porque **exige TU propia app de desarrollador de WHOOP** (no la da
Junction). Polar sí conectó porque no es BYOO. Ya cambié el flujo para que **conectar abra el
picker de Junction** (elige tu marca ahí) y no salga en blanco — pero para que WHOOP aparezca y
funcione, hay que configurarlo una vez:

1. Crea una app en el **WHOOP Developer Dashboard** (developer.whoop.com) → crea un *Team* → una *App*.
   - Redirect URI: el que te indique Junction en el paso siguiente.
   - Copia el **Client ID** y **Client Secret**.
2. En **Junction Dashboard → Config → Custom Credentials → WHOOP V2 → Setup** → pega esas credenciales.
3. Listo: WHOOP aparecerá en el picker y conectará (límite de 10 miembros hasta que WHOOP apruebe la app).

> Si por ahora no quieres WHOOP, **Polar ya funciona** — con eso validamos el ciclo completo.

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
