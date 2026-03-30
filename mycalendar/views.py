# mycalendar/views.py
from django.shortcuts import render
from datetime import datetime
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

    # Use your new custom calendar instead!
    cal = CustomCalendar(year, month)
    html_calendar = cal.formatmonth(year, month)

    context = {
        'calendar': html_calendar,
        'year': year,
        'month': month
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