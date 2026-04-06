# mycalendar/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, date, timedelta
from .utils import CustomCalendar
from .models import Event

def show_calendar(request, year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month
    else:
        year = int(year)
        month = int(month)

    # Logic for Previous and Next buttons
    current_date = date(year, month, 1)
    prev_month = current_date - timedelta(days=1)
    next_month = current_date + timedelta(days=32) # Jumps to next month

    cal = CustomCalendar(year, month)
    html_calendar = cal.formatmonth(year, month)

    context = {
        'calendar': html_calendar,
        'year': year,
        'month': month,
        'prev_year': prev_month.year,   
        'prev_month': prev_month.month,
        'next_year': next_month.year,
        'next_month': next_month.month,
    }
    return render(request, 'mycalendar/calendar.html', context)

# NEW VIEW: Handles the specific day's events
def daily_events(request, year, month, day):
    # Fetch all events from the database that match this exact date
    events = Event.objects.filter(date__year=year, date__month=month, date__day=day)
    
    # Format a nice date string for the template
    date_obj = datetime(year, month, day)
    formatted_date = date_obj.strftime('%B %d, %Y')

    context = {
        'events': events,
        'date': formatted_date,
    }
    return render(request, 'mycalendar/events.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # creates the new user in the database
            return redirect('login') # Send them to the login page after they sign up
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})