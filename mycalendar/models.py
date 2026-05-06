# Create your models here.
# mycalendar/models.py
from django.db import models
from django.contrib.auth.models import User


TAGS_CHOICES = [
    ('ssbu','Super Smash Bros. Ultimate'),
    ('sf6','Street Fighter 6'),
    ('ow','Overwatch'),
    ('mk','Mortal Kombat'),
    ('dbfz','Dragon Ball Fighterz'),
]

MEETING_TIME_CHOICES = [
    ('morning', 'Morning (8 AM - 11 AM)'),
    ('afternoon', ' Afternoon (12 PM - 4 PM)'),
    ('evening', ' Evening (4 PM - 8 PM)'),
]

DAYS_AVAILABLE =[
    ('mon','Monday'),
    ('tue','Tuesday'),
    ('wed','Wednesday'),
    ('thu','Thursday'),
    ('fri','Friday')
]
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title

# NEW MODEL: The User Profile
class Profile(models.Model):
    # This links exactly one Profile to exactly one User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # The fields they can fill out
    profile_picture = models.FileField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    fun_facts = models.TextField(max_length=500, blank=True)
    favorite_games = models.CharField(max_length=100, blank=True)

    tags = models.CharField(
        max_length=200, 
        blank=True, 
    )
    
    meeting_times = models.CharField(
        max_length=200, 
        blank=True, 
    )
    days_available = models.CharField(
        max_length=200, 
        blank=True, 
    )

    def __str__(self):
        return f"{self.user.username}'s Loadout"

    def _labels_for(self, stored_values, choices):
        selected = stored_values.split(',') if stored_values else []
        labels = dict(choices)
        return [labels[value] for value in selected if value in labels]

    @property
    def tag_labels(self):
        return self._labels_for(self.tags, TAGS_CHOICES)

    @property
    def meeting_time_labels(self):
        return self._labels_for(self.meeting_times, MEETING_TIME_CHOICES)

    @property
    def day_available_labels(self):
        return self._labels_for(self.days_available, DAYS_AVAILABLE)
