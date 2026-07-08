# Marca — MoreTV

Identidad visual de la app.

## Concepto

Una pantalla de TV con botón de **play** y una insignia **"+" (More)**: "más TV".
Paleta azul de la app (`#4c6fff → #6b8bff`) sobre fondo oscuro `#0f1116`.

## Archivos

| Archivo               | Uso                                                      |
| --------------------- | ------------------------------------------------------- |
| `moretv-icon.svg`     | Ícono maestro (vector, editable). Fuente de todo lo demás. |
| `moretv-1024.png`     | Ícono 1024×1024 (App Store / Google Play).              |
| `moretv-512.png`      | Ícono 512×512.                                          |
| `moretv-logo.svg/png` | Logo horizontal (ícono + wordmark "MoreTV").            |
| `moretv-banner.png`   | Banner sobre fondo oscuro para README/splash.           |

Derivados generados también en:
- `../tizen/icon.png` (512) — empaquetado Samsung Crystal / Tizen.
- `../public/moretv-192.png`, `favicon-64.png`, `favicon-32.png` — app web / PWA.

## Regenerar los PNG

Desde el SVG maestro con [sharp](https://sharp.pixelplumbing.com/):

```bash
npm i -g sharp-cli
sharp -i branding/moretv-icon.svg -o branding/moretv-512.png resize 512 512
```

O edita `moretv-icon.svg` (es vector puro) y vuelve a exportar los tamaños.

## Wordmark

**More** en blanco `#f4f6fb` + **TV** en azul `#6b8bff`, tipografía sans-serif
bold. En la app web el encabezado usa el mismo criterio (`.brand__accent`).
