# events/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Event(models.Model):
    LOCATION_CHOICES = [
        ('venue', 'Venue'),
        ('online', 'Online Event'),
        ('to_be_announced', 'To be Announced'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
<<<<<<< HEAD
    date = models.DateField()  # Use DateField for just the date
    start_time = models.TimeField()  # Separate field for start time
    end_time = models.TimeField()  # Separate field for end time
    location_type = models.CharField(max_length=50, choices=LOCATION_CHOICES)  # Choices for location type
    location = models.CharField(max_length=200, blank=True, null=True)  # Venue location (e.g., city or county)
    manual_location = models.CharField(max_length=200, blank=True, null=True)  # Manual location input
    venue_details = models.CharField(max_length=200, blank=True, null=True)  # Additional venue details (e.g., apartment/suite)
    region = models.CharField(max_length=100, blank=True, null=True)  # Region
    image = models.ImageField(upload_to='events/')
    audience_capacity = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
=======
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    # an event may have multiple marketing images
    # we need to upload and store images/banners
    image = models.ImageField(upload_to='events/')
    # specify audience capacity, ticket distribution
    audienceCapacity = models.IntegerField()
    # vendors/partners 
>>>>>>> origin/main

    def __str__(self):
        return self.name
    
<<<<<<< HEAD
=======
    @property
    def remaining_capacity(self):
        sold_tickets_count = Ticket.objects.filter(event=self).count()
        return max(0, self.audienceCapacity - sold_tickets_count)

class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Name of the ticket type
    description = models.TextField()  # Description of the ticket type
    quantity = models.IntegerField(default=0)  # Total quantity available for this type
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.event.name} - {self.name}"

  
    # Ticket is generated only after payment is confirmed 
>>>>>>> origin/main
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # make it optional
    ticketType = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.event.name} - {self.seat_number}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()

    def __str__(self):
        return f"Review for {self.event.name} by {self.user.username}"

    
class Sales(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Chat(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     message = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True)


