# events/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Event, Ticket, Review, Chat, Notification
from .forms import EventForm, TicketForm, ReviewForm, ChatForm, RegistrationForm
from django.contrib.auth import logout, login
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
import logging



@login_required
def customer_dashboard(request):
    available_events = Event.objects.all()
    purchased_tickets = Ticket.objects.filter(user=request.user)
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'dashboard/customerdashboard.html', {
        'available_events': available_events,
        'purchased_tickets': purchased_tickets,
        'notifications': notifications,
    })

@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_details.html', {'event': event})

@login_required
def purchase_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        # Assume there's logic here to handle payment
        ticket = Ticket.objects.create(
            event=event,
            user=request.user,
            seat_number="A1",  # This should be generated dynamically
            price=event.price
        )
        
        # Send confirmation email
        send_mail(
            'Ticket Purchase Confirmation',
            f'Thank you for purchasing a ticket to {event.name}. Your seat number is {ticket.seat_number}.',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )
        
        return redirect('customer-dashboard')
    return render(request, 'events/purchase_ticket.html', {'event': event})

@login_required
def manage_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST' and 'cancel' in request.POST:
        ticket.delete()
        return redirect('customer-dashboard')
    return render(request, 'tickets/manage_ticket.html', {'ticket': ticket})

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('customer-dashboard')
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form})


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_details.html', {'event': event})
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:  # Admin user
                return HttpResponseRedirect(reverse('admin:index'))
            else:  # Customer user
                return HttpResponseRedirect(reverse('dashboard'))
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
    

def homepage(request):
    return render(request, 'dashboard/homepage.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data here (e.g., send an email)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the same contact page
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

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

logger = logging.getLogger(__name__)

def event_manage(request):
    events = Event.objects.all()
    logger.debug(f"Retrieved events: {events}")
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard-eventmanage'))
    else:
        form = EventForm()
    return render(request, 'dashboard/event_management.html', {'form': form, 'events': events})


def event_delete(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('dashboard-eventmanage')
    context = {
        'event': event
    }
    return render(request, 'dashboard/event_delete.html', context)

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

def book_ticket(request):
    tickets = Ticket.objects.all()
    context = {
        'tickets': tickets,
    }
    return render(request, 'dashboard/book_ticket.html', context)


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
                'youremail@example.com',  # Replace with your email
                [email],
            )
            return redirect('dashboard-bookingtickets')
    else:
        form = TicketForm(instance=ticket)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/ticket_update.html', context)

def ticket_delete(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('dashboard-bookingtickets')
    context = {
        'ticket': ticket,
    }
    return render(request, 'dashboard/ticket_delete.html', context)

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

def review_list(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'dashboard/review_list.html', context)


def review_delete(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('dashboard-reviewlist')
    context = {
        'review': review,
    }
    return render(request, 'dashboard/review_delete.html', context)

def logout_user(request):
    logout(request)
    return render(request, 'user/logout.html')

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
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_staff:
                return redirect('admin-dashboard')
            else:
                return redirect('customer-dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})


def customer_dashboard(request):
    return render(request, 'dashboard/customer_dashboard.html')

def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

def contact(request):
    return render(request, 'dashboard/contact.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')



