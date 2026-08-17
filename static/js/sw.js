/* Activate immediately — don't wait for old tabs to close */
self.addEventListener('install', function (event) {
    self.skipWaiting();
});

self.addEventListener('activate', function (event) {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('push', function (event) {
    let data = {};
    try {
        data = event.data ? event.data.json() : {};
    } catch (e) {
        data = { title: 'Future Factory', body: 'New notification' };
    }

    event.waitUntil(
        self.registration.showNotification(data.title || 'Future Factory', {
            body: data.body || 'You have a new update.',
            icon: '/static/img/logo-icon.png',
            badge: '/static/img/logo-icon.png',
            data: { url: data.url || '/admin/' },
        })
    );
});

self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    event.waitUntil(clients.openWindow(event.notification.data.url || '/'));
});