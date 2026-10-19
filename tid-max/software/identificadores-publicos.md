# Identificadores públicos de TID-MAX

> **Solo IDs PÚBLICOS** (no secretos). Un *Client ID* de OAuth es público por diseño
> (va en las URLs de autorización). Los **secretos** — *client secrets*, *refresh/access
> tokens*, PINs, API keys (`ANTHROPIC_API_KEY`, `GH_TOKEN`, `AUTH_SECRET`, etc.) — **NUNCA
> van aquí**: viven en `.env` (local, git-ignorado) o en los secretos del host
> (Cloudflare Pages → Environment variables, GitHub Actions → Secrets).

## WHOOP — app "GAEL SYNC"
Portal: `developer-dashboard.whoop.com` → app **GAEL SYNC** → Credentials.

| Dato | Valor | Dónde se usa |
|---|---|---|
| **Client ID** | `b491045e-84aa-4ac1-8781-df2961a6cf6b` | `WHOOP_CLIENT_ID` (`.env` de `software/`) |
| Client Secret | *(secreto — en `.env`, no aquí)* | `WHOOP_CLIENT_SECRET` |
| Refresh token | *(secreto — lo rota `whoop_auth.py`)* | `WHOOP_REFRESH_TOKEN` |

- Código: `software/whoop_auth.py` (OAuth una vez) + `software/whoop_sync.py` (descarga).
- **Nota de estado:** para Gael el camino vigente es **NOOP (BLE, gratis)**; la API directa
  de WHOOP (GAEL SYNC) quedó como respaldo — WHOOP no expone PPG/R-R crudo por API.
