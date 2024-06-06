from django import forms
from .models import Event, Ticket, Review, Chat

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'price']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'quantity', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['event', 'rating', 'comment']

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['message']
