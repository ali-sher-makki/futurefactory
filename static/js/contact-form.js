function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('ff-lead-form');
    const statusEl = document.getElementById('ff-form-status');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
        statusEl.textContent = '';
        statusEl.className = 'ff-form-status';

        const data = {
            name: form.name.value.trim(),
            email: form.email.value.trim(),
            phone: form.phone.value.trim(),
            company: form.company.value.trim(),
            service_interested: form.service_interested.value,
            message: form.message.value.trim(),
        };

        try {
            const response = await fetch('/api/leads/submit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') || '',
                },
                body: JSON.stringify(data),
            });
            const result = await response.json();

            if (response.ok) {
                statusEl.textContent = result.message || "Thanks! We'll be in touch soon.";
                statusEl.classList.add('ff-form-success');
                form.reset();
            } else {
                const firstError = Object.values(result)[0];
                statusEl.textContent = Array.isArray(firstError) ? firstError[0] : (result.detail || 'Something went wrong. Please try again.');
                statusEl.classList.add('ff-form-error');
            }
        } catch (err) {
            statusEl.textContent = 'Network error. Please try again.';
            statusEl.classList.add('ff-form-error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Send message';
        }
    });
});