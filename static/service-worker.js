self.addEventListener('install', (event) => {
  console.log('Service Worker installing.');
  self.skipWaiting(); // Activates the new service worker immediately
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker activating.');
  event.waitUntil(clients.claim()); // Takes control of all clients
});

self.addEventListener('fetch', (event) => {
  // You can add caching strategies here later
  // For now, simply fetch the request
  event.respondWith(fetch(event.request));
});