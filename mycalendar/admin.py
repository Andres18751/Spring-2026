# mycalendar/admin.py
from django.contrib import admin
from .models import Event, Profile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'twitch_login', 'twitch_live_status', 'created_by')
    list_filter = ('date', 'created_by')
    readonly_fields = ('twitch_last_checked_at',)
    search_fields = ('title', 'description', 'twitch_url', 'twitch_login', 'created_by__username')


admin.site.register(Profile)
