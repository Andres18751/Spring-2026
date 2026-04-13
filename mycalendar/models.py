# Create your models here.
# mycalendar/models.py
from django.db import models
from django.contrib.auth.models import User

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
    bio = models.TextField(max_length=500, blank=True)
    favorite_games = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Loadout"