from django import forms
from .models import Event, Ticket
from django.contrib.admin import widgets
from .models import  Sales
from .models import ContactMessage, Review
from .models import User 

class EventForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput( attrs={'type':'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = Event
        fields = ['name', 'description','date','start_time', 'end_time','location_type','location','region','venue_details','image','audience_capacity', 'event_type', 'price']

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
        
class BookingForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    
    vip_ticket_qty = forms.IntegerField(min_value=0, required=False)
    vvip_ticket_qty = forms.IntegerField(min_value=0, required=False)
    early_bird_ticket_qty = forms.IntegerField(min_value=0, required=False)
    regular_ticket_qty = forms.IntegerField(min_value=0, required=False)
    giveaway_ticket_qty = forms.IntegerField(min_value=0, required=False)
    
    agree_terms = forms.BooleanField(required=True)
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        
class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']  # Add any other fields you want to include in the form
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'})
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Add phone number validation logic if needed
        return phone_number