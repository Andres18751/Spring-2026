from django import forms
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from .models import Event, Profile, TAGS_CHOICES, MEETING_TIME_CHOICES, DAYS_AVAILABLE
from .twitch import extract_twitch_login


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'start_time', 'twitch_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Smash Singles Bracket or Pablo stream night'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Add rules, check-in time, stream plans, or anything players should know.'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'twitch_url': forms.URLInput(attrs={'placeholder': 'https://www.twitch.tv/yourchannel'}),
        }

    def clean_twitch_url(self):
        twitch_url = self.cleaned_data.get('twitch_url', '').strip()
        if not twitch_url:
            return twitch_url

        parsed_url = urlparse(twitch_url)
        hostname = parsed_url.netloc.lower().removeprefix('www.')

        if hostname != 'twitch.tv':
            raise ValidationError('Please enter a valid Twitch channel link, like https://www.twitch.tv/yourchannel.')

        channel_name = extract_twitch_login(twitch_url)
        if not channel_name:
            raise ValidationError('Please include the Twitch channel name in the link.')

        return f'https://www.twitch.tv/{channel_name}'

class ProfileForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        choices=TAGS_CHOICES, 
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="What are your interests?"
    )
    
    meeting_times = forms.MultipleChoiceField(
        choices=MEETING_TIME_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="What times are you available to meet?"
    )

    days_available = forms.MultipleChoiceField(
        choices=DAYS_AVAILABLE, 
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="What days are you available to meet?"
    )
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'fun_facts', 'favorite_games', 'tags', 'meeting_times', 'days_available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'fun_facts': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share a few fun facts about you...'}),
            'favorite_games': forms.TextInput(attrs={'placeholder': 'e.g., Smash, Mortal Kombat, Street Fighter'}),
            'profile_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tags'] = self._split_choices(self.instance.tags)
            self.initial['meeting_times'] = self._split_choices(self.instance.meeting_times)
            self.initial['days_available'] = self._split_choices(self.instance.days_available)

    def _split_choices(self, value):
        return [choice for choice in value.split(',') if choice] if value else []
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.tags = ','.join(self.cleaned_data.get('tags', []))
        profile.meeting_times = ','.join(self.cleaned_data.get('meeting_times', []))
        profile.days_available = ','.join(self.cleaned_data.get('days_available', []))
        
        if commit:
            profile.save()
            self.save_m2m()
        return profile
