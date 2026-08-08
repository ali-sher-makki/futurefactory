from django.shortcuts import render
from services.models import Service


def home(request):
    services = Service.objects.filter(is_active=True)[:9]
    return render(request, 'core/home.html', {'services': services})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')