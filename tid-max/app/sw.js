// TID-MAX PWA — service worker mínimo (instalable + cache básico del shell).
// v0: cachea el shell para que abra offline; los datos (data.json) van siempre a la red.
const CACHE = "tidmax-v0-4";
const SHELL = ["./index.html", "./health.js", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png"];

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
  const url = new URL(e.request.url);
  // data.json siempre fresco (network-first); el resto: cache-first con respaldo de red.
  if (url.pathname.endsWith("data.json")) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    return;
  }
  e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
});
