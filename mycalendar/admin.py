# mycalendar/admin.py
from django.contrib import admin
from .models import Event, Profile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_by')
    list_filter = ('date', 'created_by')
    search_fields = ('title', 'description', 'created_by__username')


admin.site.register(Profile)
