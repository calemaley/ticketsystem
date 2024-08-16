from django.shortcuts import render,redirect, get_object_or_404
from .models import Event, Ticket
from .forms import EventForm, TicketForm
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
def event(request):
    events = Event.objects.all()
    context = {
        'events':events
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
