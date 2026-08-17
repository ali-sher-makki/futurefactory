function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function enablePushNotifications(vapidPublicKey) {
    const statusEl = document.getElementById('push-status');
    const btn = document.getElementById('enable-push-btn');

    if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        statusEl.textContent = 'Push notifications are not supported in this browser.';
        statusEl.className = 'ff-form-status ff-form-error';
        return;
    }

    if (!vapidPublicKey) {
        statusEl.textContent = 'VAPID key is missing. Check server configuration.';
        statusEl.className = 'ff-form-status ff-form-error';
        console.error('VAPID public key is empty or undefined');
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Enabling...';
    statusEl.textContent = '';
    statusEl.className = 'ff-form-status';

    try {
        /* 1. Register the service worker */
        console.log('[Push] Registering service worker...');
        const registration = await navigator.serviceWorker.register('/sw.js');
        console.log('[Push] Service worker registered, waiting for it to be ready...');

        /* Wait until the SW is active — subscribe can fail on a freshly installed SW */
        await navigator.serviceWorker.ready;
        console.log('[Push] Service worker is ready');

        /* 2. Ask for notification permission */
        const permission = await Notification.requestPermission();
        console.log('[Push] Permission result:', permission);

        if (permission !== 'granted') {
            statusEl.textContent = 'Notification permission was not granted.';
            statusEl.className = 'ff-form-status ff-form-error';
            return;
        }

        /* 3. Unsubscribe any existing subscription in browser (handles VAPID key changes cleanly) */
        const existingSubscription = await registration.pushManager.getSubscription();
        if (existingSubscription) {
            console.log('[Push] Existing subscription found in browser, unsubscribing to use current key...');
            await existingSubscription.unsubscribe();
        }

        console.log('[Push] Subscribing to push manager...');
        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
        });
        console.log('[Push] Browser subscription obtained:', JSON.stringify(subscription));

        /* 4. Send subscription to our server — credentials:'same-origin' is
              CRITICAL so the session cookie is included, otherwise Django's
              @staff_member_required decorator sees an anonymous user and
              redirects to the login page (302). */
        const response = await fetch('/push/subscribe/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(subscription),
        });

        console.log('[Push] Server response status:', response.status);

        if (response.ok) {
            const result = await response.json();
            console.log('[Push] Server response body:', result);
            statusEl.textContent = "Notifications enabled! You'll get an alert for every new lead.";
            statusEl.className = 'ff-form-status ff-form-success';
        } else {
            const errorText = await response.text();
            console.error('[Push] Server error:', response.status, errorText);
            statusEl.textContent = `Failed to save subscription (HTTP ${response.status}). Are you logged in as admin?`;
            statusEl.className = 'ff-form-status ff-form-error';
        }
    } catch (err) {
        console.error('[Push] Error during push setup:', err);
        statusEl.textContent = 'Error enabling notifications: ' + err.message;
        statusEl.className = 'ff-form-status ff-form-error';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Enable notifications';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('enable-push-btn');
    if (btn) {
        btn.addEventListener('click', function () {
            enablePushNotifications(btn.dataset.vapidKey);
        });
    }
});