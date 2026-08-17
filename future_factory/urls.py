from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', core_views.service_worker, name='service-worker'),
    path('', include('core.urls')),
    path('services/', include('services.urls')),
    path('api/leads/', include('leads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)