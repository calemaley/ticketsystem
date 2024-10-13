from django.shortcuts import render,redirect, get_object_or_404
from .models import Event, Ticket, Sales, Ticket, Profile
from .forms import EventForm, TicketForm, SalesForm, BookingForm, ReviewForm, PhoneNumberForm
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
from django.db.models import Sum
from django.http import JsonResponse
from django.http import FileResponse
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import qrcode
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django_daraja.mpesa.core import MpesaClient
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
import logging




def generate_ticket_pdf(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    event = ticket.event  # Get the event associated with the ticket

    if ticket.ticket_pdf:
        messages.warning(request, 'PDF already exists for this ticket.')
        return redirect('dashboard')  # Replace with the correct URL name for your admin dashboard

    # Generate the PDF manually
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add event image if available
    if event.image:
        event_image_path = event.image.path  # Get the path to the event image
        event_image = ImageReader(event_image_path)
        p.drawImage(event_image, 50, 600, width=200, height=150)  # Draw event image at the top left

    # Add event name and details
    p.setFont("Helvetica-Bold", 16)
    p.drawString(300, 750, f"Ticket for {event.name}")
    
    p.setFont("Helvetica", 12)
    p.drawString(300, 730, f"Date: {event.date}")
    p.drawString(300, 710, f"Time: {event.start_time.strftime('%I:%M %p')} - {event.end_time.strftime('%I:%M %p')}")
    p.drawString(300, 690, f"Location: {event.location} ({event.venue_details})")
    p.drawString(300, 670, f"Price: KSH {event.price}")
    p.drawString(300, 650, f"Event Type: {event.event_type}")
    p.drawString(300, 630, f"Capacity: {event.audience_capacity}")

    # Add event description
    p.setFont("Helvetica", 10)
    p.drawString(50, 570, "Event Description:")
    p.setFont("Helvetica-Oblique", 10)
    text = p.beginText(50, 550)
    text.setTextOrigin(50, 550)
    text.setFont("Helvetica-Oblique", 10)
    text.textLines(event.description)
    p.drawText(text)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Ticket ID: {ticket.id}, Event: {event.name}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert the QR code to an image
    img_io = BytesIO()
    qr_img.save(img_io, format="PNG")
    img_io.seek(0)
    qr_image = ImageReader(img_io)

    # Add the QR code with a colorful border
    p.setFillColor(colors.red)  # Set color for QR code border
    p.rect(400, 500, 150, 150, stroke=1, fill=1)  # Add colorful border around QR code
    p.drawImage(qr_image, 405, 505, width=140, height=140)  # Add QR code inside the border

    # Finalize the PDF
    p.showPage()
    p.save()

    # Save the PDF to the ticket's `ticket_pdf` field
    buffer.seek(0)  # Move the cursor to the beginning of the buffer
    pdf_name = f'ticket_{ticket.id}.pdf'  # Generate a unique name for the PDF
    ticket.ticket_pdf.save(pdf_name, ContentFile(buffer.read()), save=True)

    messages.success(request, 'PDF has been generated successfully.')
    return redirect('dashboard')  # Replace with the correct URL name for your admin dashboard



    
    
def validate_qr_code(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        # Add any additional validation logic
        return JsonResponse({'status': 'valid', 'message': 'Ticket is valid.'})
    except Ticket.DoesNotExist:
        return JsonResponse({'status': 'invalid', 'message': 'Invalid ticket.'})


def list_tickets_with_pdf(request):
    # Get all tickets where ticket_pdf is not empty
    tickets_with_pdf = Ticket.objects.filter(ticket_pdf__isnull=False)
    
    context = {
        'tickets_with_pdf': tickets_with_pdf,
    }
    return render(request, 'superusers/tickets_with_pdf.html', context)

def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        # Handle file upload if a new PDF is uploaded
        if 'ticket_pdf' in request.FILES:
            if ticket.ticket_pdf:
                # Delete the existing PDF if present
                if default_storage.exists(ticket.ticket_pdf.path):
                    default_storage.delete(ticket.ticket_pdf.path)
            
            # Save the new PDF
            ticket.ticket_pdf = request.FILES['ticket_pdf']
            ticket.save()
            return redirect('tickets_with_pdf')  # Redirect to tickets with PDF page

    return render(request, 'superusers/edit_ticket.html', {'ticket': ticket})

def delete_ticket_pdf(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if ticket.ticket_pdf:
        # Delete the PDF file
        if os.path.isfile(ticket.ticket_pdf.path):
            os.remove(ticket.ticket_pdf.path)
        
        # Clear the PDF field in the database
        ticket.ticket_pdf = None
        ticket.save()
        
        messages.success(request, "The PDF has been deleted successfully.")
    else:
        messages.warning(request, "No PDF found to delete.")
    
    return redirect('tickets_with_pdf')  # Redirect back to the list of tickets with PDFs


def home(request):
    # Get search and filter parameters from the request
    search_query = request.GET.get('search', '')
    location_filter = request.GET.get('location')
    date_filter = request.GET.get('date')
    
    # Get the filtered events (you may have a custom filtering function)
    event_data = get_filtered_events(search_query, location_filter, date_filter)

    # Prepare the context
    context = {
        'upcoming_events': event_data['upcoming_events'],
        'featured_events': event_data['featured_events'],
        'giveaway_events': event_data['giveaway_events'],
        'search_query': search_query,
        'location_filter': location_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'events/home.html', context)


from django.utils import timezone

def get_filtered_events(search_query='', location_filter='', date_filter='', event_type_filter=''):
    # Base query for approved and published events
    events = Event.objects.filter(is_published=True, is_approved=True, date__gte=timezone.now())

    # Filter for specific event types
    upcoming_events = events.filter(upcoming_events=True).order_by('date')
    featured_events = events.filter(is_featured=True).order_by('date')
    giveaway_events = events.filter(giveaway=True).order_by('date')

    # Apply search query filter
    if search_query:
        upcoming_events = upcoming_events.filter(name__icontains=search_query)
        featured_events = featured_events.filter(name__icontains=search_query)
        giveaway_events = giveaway_events.filter(name__icontains=search_query)

    # Apply location filter
    if location_filter:
        upcoming_events = upcoming_events.filter(location__icontains=location_filter)
        featured_events = featured_events.filter(location__icontains=location_filter)
        giveaway_events = giveaway_events.filter(location__icontains=location_filter)

    # Apply date filter
    if date_filter:
        upcoming_events = upcoming_events.filter(date=date_filter)
        featured_events = featured_events.filter(date=date_filter)
        giveaway_events = giveaway_events.filter(date=date_filter)

    # Apply event type filter
    if event_type_filter:
        upcoming_events = upcoming_events.filter(event_type=event_type_filter)
        featured_events = featured_events.filter(event_type=event_type_filter)
        giveaway_events = giveaway_events.filter(event_type=event_type_filter)

    return {
        'upcoming_events': upcoming_events,
        'featured_events': featured_events,
        'giveaway_events': giveaway_events,
    }

    
def search_events(request):
    search_query = request.GET.get('search', '')
    location_filter = request.GET.get('location', '')

    events = Event.objects.all()

    if search_query:
        events = events.filter(name__icontains=search_query)

    if location_filter:
        events = events.filter(location__icontains=location_filter)

    context = {
        'events': events,
        'search_query': search_query,
        'location_filter': location_filter,
    }

    return render(request, 'events/search_results.html', context)


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
            try:
                send_mail(subject, message_body, 'calemale360@gmail.com', ['calemale360@gmail.com'])
                print("Email sent successfully") 
            except Exception as e:
                print(f"Error sending email: {str(e)}")  

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'events/contact.html', {'form': form})

def event(request):
    # Capture filter inputs
    search_query = request.GET.get('search', '')
    event_type_filter = request.GET.get('event_type', '')
    location_filter = request.GET.get('location', '')  # Capture location filter

    # Start with all approved and published events
    event_data = Event.objects.filter(is_approved=True, is_published=True)

    # Apply filters
    if search_query:
        event_data = event_data.filter(name__icontains=search_query)
    if event_type_filter:
        event_data = event_data.filter(event_type=event_type_filter)
    if location_filter:
        event_data = event_data.filter(location__icontains=location_filter)

    # Get distinct event types for the dropdown
    event_types = Event.objects.values('event_type').distinct()

    context = {
        'events': event_data,  # Filtered events
        'event_types': event_types,
        'event_type_filter': event_type_filter,
        'search_query': search_query,
        'location_filter': location_filter,  # Pass the location filter to the template
    }

    return render(request, 'events/events.html', context)




def past_events(request):
    # Get current date
    current_time = timezone.now()

    # Fetch events that have already happened
    events = Event.objects.filter(date__lt=current_time.date(), is_published=False)

    return render(request, 'events/past_events.html', {'events': events})

#code for viewing each event in detail

def event_detail(request, pk):
    # Fetch the event by its primary key
    item = get_object_or_404(Event, id=pk)
    
    # Fetch all tickets related to the event
    tickets = Ticket.objects.filter(event=item)
    
    # Filter specific ticket types and get the price
    ticket_types = {
        'vip_ticket': tickets.filter(ticket_type='VIP').first(),
        'vvip_ticket': tickets.filter(ticket_type='VVIP').first(),
        'early_bird_ticket': tickets.filter(ticket_type='early bird').first(),
        'regular_ticket': tickets.filter(ticket_type='regular').first(),
        'giveaway_ticket': tickets.filter(ticket_type='giveaway').first(),
    }

    # Star rating range (assuming a rating system is present)
    star_range = range(5)

    # Prepare the context for rendering the template
    context = {
        'item': item,
        'star_range': star_range,
        **ticket_types,  # Unpack ticket types into the context
    }

    return render(request, 'events/event_detail.html', context)

def admin_event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    context = {
        'event': event
    }
    return render(request, 'superusers/event_detail.html', context)

#code for event organiser dashboard
def dashboard(request):
    return render(request, 'superusers/dashboard.html')

#Code for event listing in event organizer dashboard
from django.utils import timezone
from .models import Event

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
            ticket = form.save(commit=False)  # Save ticket but don’t commit to the database yet
            ticket.user = request.user  # Assign the user who created the ticket
            ticket.save()  # Save the ticket to the database
            messages.success(request, 'Ticket has been created.')
            return redirect('ticket-list')  # Redirect to the ticket list page
    else:
        form = TicketForm()

    context = {
        'form': form,
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



def sales(request):
    # Calculate total sales
    total_sales = Sales.objects.aggregate(total=Sum('total_sales'))['total'] or 0

    # Count total number of events
    total_events = Event.objects.filter(is_published=True).count()

    # Total tickets sold
    total_tickets_sold = Sales.objects.aggregate(total=Sum('tickets_sold'))['total'] or 0

    # Highest sales event
    highest_sale_event = Sales.objects.order_by('-total_sales').first()

    # Fetch sales data for chart and table
    sales_data = Sales.objects.select_related('event').values('event__name', 'sale_date', 'tickets_sold', 'total_sales')

    context = {
        'total_sales': total_sales,
        'total_events': total_events,
        'total_tickets_sold': total_tickets_sold,
        'highest_sale_event': highest_sale_event.event.name if highest_sale_event else 'No sales yet',
        'sales_data': sales_data,
    }

    return render(request, 'superusers/sales.html', context)

def admin_dashboard(request):
    return render(request, 'superusers/admin_dashboard.html')


def admin_events(request):
    event_items = Event.objects.all()
    context = {
        'event_items':event_items,
    }
    return render(request, 'superusers/admin_events.html', context)

def admin_tickets(request):
    tickets = Ticket.objects.all().order_by('ticket_type')
    ticket_types = ["Early Bird", "VIP", "VVIP", "Giveaway"]

    context = {
        'tickets': tickets,
        'ticket_types': ticket_types,
    }
    return render(request, 'superusers/admin_tickets.html', context)


def logout_user(request):
    logout(request)
    redirect('event-page')
    return render(request,'users/logout.html')

def leave_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            return redirect('event-detail', event_id=event.id)
    else:
        form = ReviewForm()
    return render(request, 'events/leave_review.html', {'form': form, 'event': event})



def sales_analysis(request):
    # Aggregate sales data
    sales_data = Sales.objects.values('event__name').annotate(total_sales=Sum('total_sales')).order_by('-total_sales')
    total_sales = Sales.objects.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0
    total_events = Event.objects.count()
    total_tickets_sold = Sales.objects.aggregate(total_tickets=Sum('event__ticket__amount'))['total_tickets'] or 0
    
    context = {
        'sales_data': sales_data,
        'total_sales': total_sales,
        'total_events': total_events,
        'total_tickets_sold': total_tickets_sold,
    }
    return render(request, 'superusers/salesanalysis.html', context)

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

def search_suggestions(request):
    query = request.GET.get('query', '')
    suggestions = []
    
    if query:
       
        events = Event.objects.filter(name__icontains=query, is_published=True)[:20]  
        suggestions = [
            {
                'id': event.id,
                'name': event.name,
                'image_url': event.image.url if event.image else '/path/to/default/image.jpg'  
            } for event in events
        ]

    return JsonResponse({'suggestions': suggestions})
def location_suggestions(request):
    query = request.GET.get('query', '')
    suggestions = []
    
    if query:
        
        locations = Event.objects.filter(location__icontains=query, is_published=True).values('location').distinct()[:20]
        suggestions = [
            {
                'location': location['location']
            } for location in locations
        ]

    return JsonResponse({'suggestions': suggestions})

import logging

logger = logging.getLogger(__name__)

def book_tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            # Get form data
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            # Get ticket quantities
            vip_qty = int(request.POST.get('vip_ticket_qty', 0))
            vvip_qty = int(request.POST.get('vvip_ticket_qty', 0))
            early_bird_qty = int(request.POST.get('early_bird_ticket_qty', 0))
            regular_qty = int(request.POST.get('regular_ticket_qty', 0))

            # Check if at least one ticket is selected
            if vip_qty == 0 and vvip_qty == 0 and early_bird_qty == 0 and regular_qty == 0:
                messages.error(request, "Please select at least one valid ticket.")
                return redirect('event-detail', pk=event.id)

            # Calculate the total price and convert to integer
            total_price = int(
                (vip_qty * event.vip_price) + (vvip_qty * event.vvip_price) + \
                (early_bird_qty * event.early_bird_price) + (regular_qty * event.regular_price)
            )

            # Initialize MpesaClient and initiate payment
            mpesa_client = MpesaClient()
            phone_number = phone  # Phone number from the form
            amount = total_price
            account_reference = f"Booking for {event.name}"
            transaction_desc = "Payment for event tickets"
            callback_url = 'https://e2cd-105-163-158-85.ngrok-free.app'  # Replace with actual callback URL

            try:
                # Initiate M-Pesa STK Push Payment
                response = mpesa_client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
                response_data = response.json()

                logger.info(f"M-Pesa Response: {response_data}")  # Log the full response for debugging

                if response_data.get('ResponseCode') == '0':
                    messages.success(request, "Payment initiated. Please check your phone to complete the payment.")
                    return redirect('event-detail', pk=event.id)
                else:
                    error_description = response_data.get('ResponseDescription', 'Unknown error occurred')
                    messages.error(request, f"Payment initiation failed: {error_description}")
                    return redirect('event-detail', pk=event.id)
            except Exception as e:
                logger.error(f"Error during M-Pesa payment: {str(e)}")
                messages.error(request, f"An error occurred during payment initiation: {str(e)}")
                return redirect('event-detail', pk=event.id)
        else:
            messages.error(request, "Form submission failed. Please correct the errors and try again.")
            return render(request, 'events/event_detail.html', {'item': event, 'form': form})

    else:
        form = BookingForm()

    return render(request, 'events/event_detail.html', {'item': event, 'form': form})



# Payment callback view to update payment status after payment completion
def payment_callback(request):
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body)
            
            if callback_data.get('ResultCode') == 0:  # Success
                messages.success(request, "Payment was successful. You will receive an email with your ticket shortly.")
                return JsonResponse({"message": "Payment successful"})
            else:
                messages.error(request, "Payment failed. Please try again.")
                return JsonResponse({"message": "Payment failed"}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid callback data"}, status=400)
    return JsonResponse({"message": "Only POST requests allowed"}, status=405)



def send_ticket_via_sms(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if the user already has a profile, if not create one
    user_profile, created = Profile.objects.get_or_create(user=ticket.user)
    
    # Ensure the user has a valid phone number
    if not user_profile.phone_number:
        messages.error(request, "No phone number found. Please provide a valid phone number.")
        return redirect('enter_phone_number', ticket_id=ticket.id)

    # Proceed to send the SMS if the PDF is available
    if ticket.ticket_pdf:
        sms_api_url = "https://api2.tiaraconnect.io/api/messaging/sendsms"
        bearer_token = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI0MDYiLCJvaWQiOjQwNiwidWlkIjoiZGE4M2M0M2ItYjhhNC00NTBkLThiYzktMmY2YmEwMzhlMjEyIiwiYXBpZCI6MzIzLCJpYXQiOjE3MTg5OTcyNDAsImV4cCI6MjA1ODk5NzI0MH0.FREAPyL9ZZhy-Wo7rV6q3bu-2Kv657xp48NxJTmBkug1SzpgSDKAfH5vu7VGYjuT_F_97nWwaL65q5-Pst83ww"  

        # Message to send
        message = f"Hey {ticket.user.first_name}! 🎉 Your golden ticket to {ticket.event.name} is hot off the press and waiting just for you! Ready to rock? Grab it here: {request.build_absolute_uri(ticket.ticket_pdf.url)}. Don’t keep the fun waiting, champ – see you there!"


        # Prepare the payload
        payload = {
            'from': 'TECHVOYAGE',
            'to': user_profile.phone_number,
            'message': message,
            'refId': '09wiwu088xu'
        }

        headers = {
            'Authorization': bearer_token,
            'Content-Type': 'application/json',
        }
        
        response = requests.post(sms_api_url, json=payload, headers=headers)

        # Check if the SMS was sent successfully
        if response.status_code == 200:
            messages.success(request, f"Ticket has been successfully sent to {user_profile.phone_number} via SMS.")
        else:
            messages.error(request, "Failed to send the SMS. Please try again.")
    else:
        messages.error(request, "Ticket PDF not available.")

    return redirect('admin-tickets')  # Redirect back to the tickets page

def enter_phone_number(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if the user already has a profile and create one if not
    user_profile, created = Profile.objects.get_or_create(user=ticket.user)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number:
            # Save the phone number in the user's profile
            user_profile.phone_number = phone_number
            user_profile.save()

            # Redirect to the view that sends the SMS
            return redirect('send_ticket_via_sms', ticket_id=ticket.id)

    return render(request, 'events/enter_phone_number.html', {'ticket': ticket, 'user_profile': user_profile})

def otp_page(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        custom_message = request.POST.get('custom_message')

        if phone_number and custom_message:
            # Use the phone number and message to send an OTP
            sms_api_url = "https://api2.tiaraconnect.io/api/messaging/sendsms"
            bearer_token = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI0MDYiLCJvaWQiOjQwNiwidWlkIjoiZGE4M2M0M2ItYjhhNC00NTBkLThiYzktMmY2YmEwMzhlMjEyIiwiYXBpZCI6MzIzLCJpYXQiOjE3MTg5OTcyNDAsImV4cCI6MjA1ODk5NzI0MH0.FREAPyL9ZZhy-Wo7rV6q3bu-2Kv657xp48NxJTmBkug1SzpgSDKAfH5vu7VGYjuT_F_97nWwaL65q5-Pst83ww"  

            # Prepare the payload for sending the OTP via SMS
            payload = {
                'from': 'TECHVOYAGE',
                'to': phone_number,
                'message': custom_message,
                'refId': '09wiwu088xu'
            }

            headers = {
                'Authorization': bearer_token,
                'Content-Type': 'application/json',
            }
            
            response = requests.post(sms_api_url, json=payload, headers=headers)

            # Check if the SMS was sent successfully
            if response.status_code == 200:
                messages.success(request, f"OTP has been successfully sent to {phone_number}.")
            else:
                messages.error(request, "Failed to send the OTP. Please try again.")

        else:
            messages.error(request, "Please provide both phone number and message.")

    return render(request, 'superusers/otp_page.html')