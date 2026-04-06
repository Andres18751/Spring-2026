"""
URL configuration for test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from mycalendar import views as my_views

def home(request):
    return HttpResponse("""
        <h1>Welcome to my new Django site!</h1>
        <a href="/calendar/">Go to Calendar</a> |
        <a href="/accounts/login/">Login</a> | <a href="/signup/">Sign Up</a>
    """)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Added a trailing slash to 'calendar/' to follow Django's convention for URL patterns
    path('calendar/', include('mycalendar.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', my_views.signup, name='signup'),
    path('', home, name='home'),  
]