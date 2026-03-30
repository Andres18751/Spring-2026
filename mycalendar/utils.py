# mycalendar/utils.py
from calendar import HTMLCalendar
from django.urls import reverse

class CustomCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    # Overriding the default formatday method
    def formatday(self, day, weekday):
        if day != 0:
            # We will create this 'daily-events' URL shortly
            url = reverse('daily-events', args=[self.year, self.month, day])
            # Wrap the day number in a clickable link
            return f"<td><a href='{url}' style='display:block; text-decoration:none; color:#007bff; font-weight:bold;'>{day}</a></td>"
        return "<td></td>"