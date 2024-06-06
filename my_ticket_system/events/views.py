from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Event, Ticket, Review, Chat
from .forms import EventForm, TicketForm, ReviewForm, ChatForm
from django.contrib.auth import logout
from django.contrib import messages

def homepage(request):
    return render(request, 'dashboard/homepage.html')

def index(request):
    event_count = Event.objects.all().count()
    ticket_count = Ticket.objects.all().count()
    review_count = Review.objects.all().count()
    tickets = Ticket.objects.all()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            event_name = form.cleaned_data.get('event')
            messages.success(request, f'Ticket for {event_name} has been booked')
            return redirect('dashboard-index')
    else:
        form = TicketForm()
    context = {
        'event_count': event_count,
        'ticket_count': ticket_count,
        'review_count': review_count,
        'form': form,
        'tickets': tickets,
    }
    return render(request, 'dashboard/dashboard.html', context)

# Define other view functions similarly

# Function for managing events
def event_manage(request):
    events = Event.objects.all()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            event_name = form.cleaned_data.get('name')
            messages.success(request, f'Event {event_name} has been added')
            return redirect('dashboard-eventmanage')
    else:
        form = EventForm()
    context = {
        'form': form,
        'events': events,
    }
    return render(request, 'dashboard/event_management.html', context)

# Function to delete an event
def event_delete(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('dashboard-eventmanage')
    context = {
        'event': event
    }
    return render(request, 'dashboard/event_delete.html', context)

# Function to update an event
def event_update(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard-eventmanage')
    else:
        form = EventForm(instance=event)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/event_update.html', context)

# Function for booking tickets
def book_ticket(request):
    tickets = Ticket.objects.all()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-bookingtickets')
    else:
        form = TicketForm()
    context = {
        'form': form,
        'tickets': tickets,
    }
    return render(request, 'dashboard/ticket_booking.html', context)

# Function for updating a ticket booking
def ticket_update(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            email_content = f"Dear Customer, Your ticket for the event has been updated. Thank you for booking with us!"
            send_mail(
                'Event Ticket Booking Update',
                email_content,
                'youremail@example.com',  
                [email],
            )
            return redirect('dashboard-bookingtickets')
    else:
        form = TicketForm(instance=ticket)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/ticket_update.html', context)

# Function to delete a ticket booking
def ticket_delete(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('dashboard-bookingtickets')
    context = {
        'ticket': ticket,
    }
    return render(request, 'dashboard/ticket_delete.html', context)

# Function for adding a review
def add_review(request):
    reviews = Review.objects.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-index')
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'reviews': reviews,
    }
    return render(request, 'dashboard/add_review.html', context)

# Function for displaying reviews
def review_list(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'dashboard/review_list.html', context)

# Function to delete a review
def review_delete(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('dashboard-reviewlist')
    context = {
        'review': review,
    }
    return render(request, 'dashboard/review_delete.html', context)

# Logout function
def logout_user(request):
    logout(request)
    return render(request, 'user/logout.html')

# Chat function for customer support
def chat_view(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.save()
    else:
        form = ChatForm()
    messages = Chat.objects.all()
    return render(request, 'chat.html', {'form': form, 'messages': messages})

# Admin chat page
def admin_chat_view(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.save()
    else:
        form = ChatForm()
    messages = Chat.objects.all()
    return render(request, 'admin_chat.html', {'form': form, 'messages': messages})
