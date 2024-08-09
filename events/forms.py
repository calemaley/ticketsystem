# events/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Event, Ticket, Review, Chat, Notification, TicketType


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
        fields = ['ticket_type', 'seat_number']
        widgets = {
            'seat_number': forms.TextInput(attrs={'placeholder': 'Enter seat number'}),
        }

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        if event:
            self.fields['ticket_type'].queryset = TicketType.objects.filter(event=event)

class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['event', 'name', 'description', 'quantity', 'price']

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


