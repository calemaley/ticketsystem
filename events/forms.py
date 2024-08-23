from django import forms
from .models import Event, Ticket
from django.contrib.admin import widgets
from .models import  Sales
from .models import ContactMessage

class EventForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput( attrs={'type':'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = Event
        fields = ['name', 'description','date','start_time', 'end_time','location_type','location','region','venue_details','image','audience_capacity', 'event_type']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'ticket_type','ticket_price','amount']
        
        
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'message']

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['event', 'total_sales', 'sale_date']