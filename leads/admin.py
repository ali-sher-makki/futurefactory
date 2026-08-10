from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service_interested', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('created_at',)