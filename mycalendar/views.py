# mycalendar/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, date, timedelta
from .utils import CustomCalendar
from .models import Event, Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

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

    # --- NEW CODE STARTS HERE --- 
    # ADDING EVENT HIGHLIGHTING
    # Fetch all events for this specific month and year
    events_this_month = Event.objects.filter(date__year=year, date__month=month)
    event_days = list(events_this_month.values_list('date__day', flat=True))
    # --- NEW CODE ENDS HERE ---

    context = {
        'calendar': html_calendar,
        'year': year,
        'month': month,
        'prev_year': prev_month.year,   
        'prev_month': prev_month.month,
        'next_year': next_month.year,
        'next_month': next_month.month,
        'event_days': event_days,  # Pass the list of event days to the template
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

#Handles the homepage and upcoming events
def home(request):
    # Get today's date
    today = date.today()
    
    # Fetch events where the date is greater than or equal to today, 
    # order them chronologically, and grab the first 5
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:5]
    
    context = {
        'events': upcoming_events
    }
    return render(request, 'home.html', context)

# NEW VIEW: The User Profile Page
@login_required
def profile(request):
    # This safely gets the user's profile, or creates a blank one if they just signed up
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    
    return render(request, 'profile.html', {'profile': user_profile})

@login_required
def edit_profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    # If they hit the "Save" button
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile') # Send them back to their loadout card
            
    # If they are just loading the page to type
    else:
        form = ProfileForm(instance=user_profile)
        
    return render(request, 'edit_profile.html', {'form': form})