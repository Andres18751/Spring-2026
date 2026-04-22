from django import forms
from .models import Profile, TAGS_CHOICES, MEETING_TIME_CHOICES, DAYS_AVAILABLE

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
        fields = ['bio', 'favorite_games', 'tags', 'meeting_times', 'days_available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'favorite_games': forms.TextInput(attrs={'placeholder': 'e.g., Smash, Mortal Kombat, Street Fighter'}),
        }
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        if commit:
            profile.save()
        if self.cleaned_data.get('tags'):
            profile.tags = ','.join(self.cleaned_data['tags'])
        if self.cleaned_data.get('meeting_times'):
            profile.meeting_times = ','.join(self.cleaned_data['meeting_times'])
        if self.cleaned_data.get('days_available'):
            profile.days_available = ','.join(self.cleaned_data['days_available'])
        profile.save()
        return profile