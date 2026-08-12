# reportes/ — reportes PRIVADOS por atleta

El pipeline multiusuario (`tid_multi.py`) escribe aquí **un reporte por atleta**:
`reportes/<slug>.json` (mismo formato que el `data.json` del dashboard) más un
`reportes/_index.json` no secreto (quién existe, para el login/app).

- Se **generan en la nube** (GitHub Actions) y se commitean, igual que `web/data.json`.
- El **login (Fase 2)** los servirá solo al atleta autenticado (`api/me` los lee del
  repo por atleta). Hasta entonces, el dashboard público sigue mostrando al atleta
  primario (Gael) vía `web/data.json` + `app/data.json`.
- No edites estos archivos a mano: los regenera el pipeline.
