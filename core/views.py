import json
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from services.models import Service
from .models import PushSubscription


def home(request):
    services = Service.objects.filter(is_active=True)[:9]
    return render(request, 'core/home.html', {'services': services})


def about(request):
    service_count = Service.objects.filter(is_active=True).count()
    return render(request, 'core/about.html', {'service_count': service_count})


def leadership(request):
    return render(request, 'core/leadership.html')


def contact(request):
    services = Service.objects.filter(is_active=True)
    preselected_service = request.GET.get('service', '')
    return render(request, 'core/contact.html', {'services': services, 'preselected_service': preselected_service})


@staff_member_required
def notifications_page(request):
    return render(request, 'core/notifications.html', {'vapid_public_key': settings.VAPID_PUBLIC_KEY})


@staff_member_required
@require_POST
def push_subscribe(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    endpoint = data.get('endpoint')
    keys = data.get('keys', {})
    if not endpoint or not keys.get('p256dh') or not keys.get('auth'):
        return JsonResponse({'error': 'Invalid subscription'}, status=400)

    PushSubscription.objects.update_or_create(
        endpoint=endpoint,
        defaults={'p256dh': keys['p256dh'], 'auth': keys['auth']},
    )
    return JsonResponse({'success': True})


def service_worker(request):
    sw_path = settings.BASE_DIR / 'static' / 'js' / 'sw.js'
    with open(sw_path) as f:
        content = f.read()
    return HttpResponse(content, content_type='application/javascript')