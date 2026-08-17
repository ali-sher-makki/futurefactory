from django.contrib import admin
from .models import PushSubscription


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('endpoint_short', 'created_at')
    readonly_fields = ('endpoint', 'p256dh', 'auth', 'created_at')

    def endpoint_short(self, obj):
        return obj.endpoint[:60] + '...' if len(obj.endpoint) > 60 else obj.endpoint
    endpoint_short.short_description = 'Endpoint'