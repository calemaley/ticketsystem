from django.shortcuts import render,redirect, get_object_or_404
from .models import Event, Ticket, Sales, Ticket
from .forms import EventForm, TicketForm
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
import matplotlib.pyplot as plt
import io
import urllib, base64
import requests
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm
# Create your views here.


def home(request):
    # Get search and filter parameters from the request
    search_query = request.GET.get('search', '')
    location_filter = request.GET.get('location')
    date_filter = request.GET.get('date')
    
    # Base query for each event type
    upcoming_events = Event.objects.filter(
        upcoming_events=True,
        date__gte=timezone.now()
    ).order_by('date')

    featured_events = Event.objects.filter(
        is_featured=True,
        date__gte=timezone.now()
    ).order_by('date')

    giveaway_events = Event.objects.filter(
        giveaway=True,
        date__gte=timezone.now()
    ).order_by('date')
    
    # Apply filters and search to each query set
    if search_query:
        upcoming_events = upcoming_events.filter(name__icontains=search_query)
        featured_events = featured_events.filter(name__icontains=search_query)
        giveaway_events = giveaway_events.filter(name__icontains=search_query)

    if location_filter:
        upcoming_events = upcoming_events.filter(location=location_filter)
        featured_events = featured_events.filter(location=location_filter)
        giveaway_events = giveaway_events.filter(location=location_filter)

    if date_filter:
        upcoming_events = upcoming_events.filter(date=date_filter)
        featured_events = featured_events.filter(date=date_filter)
        giveaway_events = giveaway_events.filter(date=date_filter)
    
    context = {
        'upcoming_events': upcoming_events,
        'featured_events': featured_events,
        'giveaway_events': giveaway_events,  
        'search_query': search_query,
        'location_filter': location_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'events/home.html', context)

def search_events(request):
    query = request.GET.get('search')
    location = request.GET.get('location')
    
    events = Event.objects.all()
    
    if query:
        events = events.filter(name__icontains=query)
    
    if location:
        events = events.filter(location__icontains=location)
    
    # Passing only the filtered events to the template
    return render(request, 'events/search_results.html', {'events': events})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            subject = f"New contact message from {first_name} {last_name}"
            message_body = f"Message from {first_name} {last_name} <{email}>:\n\n{message}"
            send_mail(subject, message_body, 'calemale360@gmail.com', ['calemale360@gmail.com'])

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'events/contact.html', {'form': form})


def event(request):
    search_query = request.GET.get('search', '')
    event_type_filter = request.GET.get('event_type', '')

    events = Event.objects.all()

    if search_query:
        events = events.filter(name__icontains=search_query)
    
    if event_type_filter:
        events = events.filter(event_type=event_type_filter)

    event_types = Event.objects.values('event_type').distinct()

    context = {
        'events': events,
        'event_types': event_types,
        'event_type_filter': event_type_filter,
        'search_query': search_query,
    }

    return render(request, 'events/events.html', context)

#code for viewing each event in detail
def event_detail(request,pk):
   item = get_object_or_404(Event, id=pk)
   tickets = Ticket.objects.filter(event=item)
   context = {
        'item':item,
        'tickets':tickets,
    }
   return render(request, 'events/event_detail.html',context)

#code for event organiser dashboard
def dashboard(request):
    return render(request, 'superusers/dashboard.html')

#Code for event listing in event organizer dashboard
def event_list(request):
    event_items = Event.objects.all()
    context = {
        'event_items':event_items,
    }
    return render(request, 'superusers/eventlist.html', context)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            event_name = form.cleaned_data.get('name')
            messages.success(request, f'{event_name} event has been added.')
            return redirect('event-list')
    else:
        form = EventForm()
        
    context = {
            'form':form,
        }
    return render(request, 'superusers/createevents.html', context)

def event_update(request,pk):
    item = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES,instance=item)
        if form.is_valid():
            form.save()
            event_name = form.cleaned_data.get('name')
            messages.success(request, f'{event_name} has been updated.')
            return redirect('event-list')
    else:
        form = EventForm(instance=item)
        
    context = {
            'form':form,
        }
    return render(request, "superusers/eventupdate.html", context)

def event_delete(request, pk):
    item = Event.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('event-list')
    return render(request, 'superusers/eventdelete.html')

def create_ticket(request):
     if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket has been created.')
            return redirect('ticket-list')
     else:
        form = TicketForm()
        
     context = {
            'form':form,
        }
     return render(request, 'superusers/createtickets.html', context)

def ticket_list(request):
    tickets = Ticket.objects.all()
    context = {
        'tickets':tickets
    }
    return render(request,"superusers/ticketslist.html", context)

def ticket_update(request,pk):
    item = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket has been updated.')
            return redirect('ticket-list')
    else:
        form = TicketForm(instance=item)
        
    context = {
            'form':form,
        }
    return render(request, "superusers/ticketupdate.html", context)

def ticket_delete(request, pk):
    item = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('ticket-list')
    return render(request, 'superusers/ticketdelete.html')

#code for customer to contact admin
def contact(request):
    return render(request, 'events/contact.html')

def sales(request):
    return render(request, "superusers/sales.html")

def admin_dashboard(request):
    return render(request, 'superusers/admin_dashboard.html')


def admin_events(request):
    event_items = Event.objects.all()
    context = {
        'event_items':event_items,
    }
    return render(request, 'superusers/admin_events.html', context)

def admin_tickets(request):
    tickets = Ticket.objects.all()
    context = {
        'tickets':tickets
    }
    return render(request, 'superusers/admin_tickets.html', context)

def logout_user(request):
    logout(request)
    redirect('event-page')
    return render(request,'users/logout.html')



def sales_analysis(request):
    sales_data = Sales.objects.all()

    # Generate chart
    fig, ax = plt.subplots()
    ax.bar([sale.event.name for sale in sales_data], [sale.total_sales for sale in sales_data])
    ax.set_xlabel('Events')
    ax.set_ylabel('Total Sales')
    ax.set_title('Sales Analysis')

    # Convert chart to base64 for embedding in HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, 'superusers/sales.html', {'chart': image_base64})

def featured_events(request):
    # Filter events based on the 'is_featured' field
    events = Event.objects.filter(is_featured=True, date__gte=timezone.now()).order_by('date')
    return render(request, 'events/featured_events.html', {'events': events})

def upcoming_events(request):
    # Filter events based on the 'upcoming_events' field
    events = Event.objects.filter(upcoming_events=True, date__gte=timezone.now()).order_by('date')
    return render(request, 'events/upcoming_events.html', {'events': events})

def giveaway_events(request):
    # Filter events based on the 'giveaway' field
    events = Event.objects.filter(giveaway=True, date__gte=timezone.now()).order_by('date')
    return render(request, 'events/giveaway_events.html', {'events': events})