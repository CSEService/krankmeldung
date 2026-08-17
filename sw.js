// sw.js — Minimal-Hintergrunddienst.
// Zweck: (1) Das Handy erkennt die Seite als installierbare App.
//        (2) Die Huelle (Logo, Kopf) oeffnet auch ohne Netz mit klarer Meldung.
// Das Formular selbst wird NIE zwischengespeichert – es liegt auf cse-service.net
// und muss immer frisch geladen werden.

const CACHE = 'krankmeldung-v1';
const HUELLE = [
  './',
  './index.html',
  './manifest.json',
  './bilder/logo-quelle.png',
  './bilder/icon-192.png',
  './bilder/icon-512.png',
  './bilder/icon-180.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(HUELLE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((namen) => Promise.all(namen.filter((n) => n !== CACHE).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  // Nur eigene Dateien bedienen. Alles Richtung cse-service.net geht direkt ins Netz.
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== self.location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then((antwort) => {
        const kopie = antwort.clone();
        caches.open(CACHE).then((c) => c.put(e.request, kopie));
        return antwort;
      })
      .catch(() => caches.match(e.request).then((treffer) => treffer || caches.match('./index.html')))
  );
});
