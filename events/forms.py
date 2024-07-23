# events/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Event, Ticket, Review, Chat, Notification



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'start_time', 'end_time', 'location', 'manual_location', 'venue_details', 'region', 'location_type', 'image', 'audience_capacity', 'ticket_price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['event', 'rating', 'review']

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['message']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField()


