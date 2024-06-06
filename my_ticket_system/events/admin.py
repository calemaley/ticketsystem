from django.contrib import admin
from .models import Event, Ticket, Review, Chat

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(Chat)
