from django.db import models
from ckeditor.fields import RichTextField
import datetime

county_choice = ( 
    ('Mombasa','Mombasa'),
    ('Kwale','Kwale'),
    ('Kilifi','Kilifi'),
    ('Tana River','Tana River'),
    ('Lamu','Lamu'),
    ('Taita Taveta','Taita Taveta'),
    ('Garissa','Garissa'),
    ('Wajir','Wajir'),
    ('Mandera','Mandera'),
    ('Marsabit','Marsabit'),
    ('Isiolo','Isiolo'),
    ('Meru','Meru'),
    ('Tharaka-Nithi','Tharaka-Nithi'),
    ('Embu','Embu'),
    ('Kitui','Kitui'),
    ('Machakos','Machakos'),
    ('Makueni','Makueni'),
    ('Nyandarua','Nyandarua'),
    ('Nyeri','Nyeri'),
    ('Kirinyaga','Kirinyaga'),
    ('Muranga','Muranga'),
    ('Kiambu','Kiambu'),
    ('Turkana','Turkana'),
    ('West Pokot','West Pokot'),
    ('Samburu','Samburu'),
    ('Trans Nzoia','Trans Nzoia'),
    ('Uasin Gishu','Uasin Gishu'),
    ('Elgeyo-Marakwet','Elgeyo-Marakwet'),
    ('Nandi','Nandi'),
    ('Baringo','Baringo'),
    ('Laikipia','Laikipia'),
    ('Nakuru','Nakuru'),
    ('Narok','Narok'),
    ('Kajiado','Kajiado'),
    ('Kericho','Kericho'),
    ('Bomet','Bomet'),
    ('Kakamega','Kakamega'),
    ('Vihiga','Vihiga'),
    ('Bungoma','Bungoma'),
    ('Busia','Busia'),
    ('Siaya','Siaya'),
    ('Kisumu','Kisumu'),
    ('Homa Bay','Homa Bay'),
    ('Migori','Migori'),
    ('Kisii','Kisii'),
    ('Nyamira','Nyamira'),
    ('Nairobi','Nairobi'),
    )


LOCATION_CHOICES = [
        ('venue', 'Venue'),
        ('online', 'Online Event'),
        ('to_be_announced', 'To be Announced'),
    ]
ticket_type = [
    ('VIP','VIP'),
    ('early bird','early bird'),
    ('giveaway', 'giveaway'),
    ('regular','regular'),
]

# Create your models here.
class Event(models.Model):
   
    name = models.CharField(max_length=200)
    description = RichTextField()
    date = models.DateField()  # Use DateField for just the date
    start_time = models.TimeField(default=datetime.time(0, 0)) # Separate field for start time
    end_time = models.TimeField(default=datetime.time(23, 59))  # Separate field for end time
    location_type = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='TBA') 
    location = models.CharField(max_length=200,choices=county_choice)  # Venue location (e.g., city or county)
    region = models.CharField(max_length=100, blank=True, null=True)  # Region
    venue_details = models.CharField(max_length=200, blank=True, null=True)  # Additional venue details (e.g., apartment/suite)
    image = models.ImageField(upload_to='events/')
    audience_capacity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ticket_type = models.CharField(max_length=50, choices=ticket_type)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.event} tickets'
