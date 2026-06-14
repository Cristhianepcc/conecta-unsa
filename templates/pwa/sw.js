/* Service Worker — CONECTA UNSA (PWA)
 * Estrategia conservadora pensada para una app institucional con datos en vivo:
 *  - El "app shell" (íconos, manifest) se precachea para permitir la instalación.
 *  - La navegación usa "network-first" con respaldo a caché si no hay conexión,
 *    de modo que el usuario nunca vea datos sensibles desactualizados estando online.
 */
const CACHE = "conecta-unsa-v1";
const APP_SHELL = [
  "/static/img/pwa/icon-192.png",
  "/static/img/pwa/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(APP_SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  // Solo GET; nunca interferir con POST/credenciales ni con otros orígenes.
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;

  // Navegaciones (páginas): red primero, caché como respaldo offline.
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((hit) => hit || caches.match("/")))
    );
    return;
  }

  // Estáticos: caché primero (rendimiento), con descarga en segundo plano.
  if (req.url.includes("/static/")) {
    event.respondWith(
      caches.match(req).then((hit) => hit || fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((cache) => cache.put(req, copy));
        return res;
      }))
    );
  }
});
