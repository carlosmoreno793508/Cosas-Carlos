# Instalar en Samsung Smart TV (Crystal UHD / QLED — Tizen)

Los televisores **Samsung Crystal UHD** (y QLED / Neo QLED) corren **Tizen OS**.
La app web (`apps/web`) se empaqueta como un widget `.wgt` y se instala en el TV.
Para **uso personal** basta con el *modo desarrollador* del televisor.

## Requisitos

- [Tizen Studio](https://developer.tizen.org/development/tizen-studio/download) con el **TV Extension** (incluye el CLI `tizen`).
- Un **certificado de autor** (se crea una vez desde el Certificate Manager de Tizen Studio).
- Un `icon.png` (recomendado 512×512) en `apps/web/tizen/icon.png`.

## Activar modo desarrollador en el Samsung Crystal

1. En el TV, abre **Apps**.
2. Escribe **12345** con el control remoto para abrir *Developer Mode*.
3. Actívalo (**On**) y escribe la **IP de tu PC** (la que corre Tizen Studio).
4. Reinicia el TV.

## Empaquetar e instalar

```bash
cd "TV app"
npm install

# 1) Construye la web y prepara dist/ con el manifiesto Tizen
npm run prepare:tizen --workspace @tvapp/web

# 2) Empaqueta el .wgt (firmado con tu perfil de autor)
cd apps/web/dist
tizen package -t wgt -s <tu-perfil-de-firma>

# 3) Conecta con el TV e instala
sdb connect <IP-del-TV>
tizen install -n TVApp.wgt -t <nombre-del-TV>
```

La app aparecerá en la fila de apps del televisor. El control remoto ya está
soportado: flechas (D-pad), OK y la tecla **Return/Atrás** (keyCode `10009`,
mapeada en `src/remote.ts`).

## Notas

- Tizen usa un WebView con MSE, así que `hls.js` reproduce HLS sin problema; los
  `.ts`/`.mp4` directos los reproduce el `<video>` nativo.
- Para publicar en la tienda **Samsung Apps** (en vez de sideload) necesitas una
  cuenta de Samsung Seller y pasar su revisión — solo si quieres distribuirla.
- Este mismo `dist/` sirve, con su propio manifiesto, para **LG webOS**
  (ver `docs/PLATFORMS.md`).
