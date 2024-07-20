# events/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    # an event may have multiple marketing images
    # we need to upload and store images/banners
    image = models.ImageField(upload_to='events/')
    # specify audience capacity, ticket distribution
    audienceCapacity = models.IntegerField()
    # vendors/partners 

    def __str__(self):
        return self.name
    
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


