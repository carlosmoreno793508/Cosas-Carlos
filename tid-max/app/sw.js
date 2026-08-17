// TID-MAX PWA — service worker mínimo (instalable + cache básico del shell).
// v0: cachea el shell para que abra offline; los datos (data.json) van siempre a la red.
const CACHE = "tidmax-v0-17";
const SHELL = ["./index.html", "./health.js", "./reporte.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);
  // El SHELL de la app (navegación / index.html / .json / API) va SIEMPRE a la red
  // primero, con la caché solo de respaldo offline. Así un deploy nuevo se ve al
  // instante (antes el index.html cache-first dejaba código viejo pegado). Los assets
  // estáticos (iconos, etc.) sí van cache-first.
  const fresco = req.mode === "navigate" || url.pathname.endsWith(".json") ||
                 url.pathname.endsWith(".html") || url.pathname.endsWith("/") ||
                 url.pathname.startsWith("/api/");
  if (fresco) {
    e.respondWith(fetch(req).catch(() => caches.match(req).then((r) => r || caches.match("./index.html"))));
    return;
  }
  e.respondWith(caches.match(req).then((r) => r || fetch(req)));
});
