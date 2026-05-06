from django import forms
from .models import Event, Profile, TAGS_CHOICES, MEETING_TIME_CHOICES, DAYS_AVAILABLE


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Smash Singles Bracket'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Add rules, check-in time, prize info, or anything players should know.'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

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
