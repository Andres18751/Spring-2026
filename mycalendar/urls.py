# mycalendar/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_calendar, name='calendar-home'),
    path('<int:year>/<int:month>/', views.show_calendar, name='calendar-specific'),
    
    # NEW PATH: Routes traffic when a specific day is clicked
    path('<int:year>/<int:month>/<int:day>/', views.daily_events, name='daily-events'),
]