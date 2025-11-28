const CACHE_NAME = 'aabb-reservas-v1';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './Logo AABB 2025.png',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});