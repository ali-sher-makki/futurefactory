from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('notifications/', views.notifications_page, name='notifications'),
    path('push/subscribe/', views.push_subscribe, name='push-subscribe'),
]