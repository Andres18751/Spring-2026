# mycalendar/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_calendar, name='calendar-home'),
    path('<int:year>/<int:month>/', views.show_calendar, name='calendar-specific'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='mycalendar/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='mycalendar/login.html'), name='login'),
    # NEW PATH: Routes traffic when a specific day is clicked
    path('<int:year>/<int:month>/<int:day>/', views.daily_events, name='daily-events'),
]