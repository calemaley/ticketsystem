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
from django_daraja.mpesa.core import MpesaClient
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


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})

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

def events_page(request):
    events = Event.objects.all()
    query = request.GET.get('q')
    print(f"Search query: {query}")  
    if query:
        events = events.filter(name__icontains=query)

    context = {
        'events': events
    }
    return render(request, 'events_page.html', context)


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
    return render(request, 'contact.html')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def noughty_by_nature_view(request):
    context = {
        'title': 'Noughty By Nature - 2000s Party',
        'description': 'Don’t miss out on the event of the year – it’s going to be noughty but oh-so-nice!',
        'date': 'Aug 09, 2024\n Time: 06:00 PM - 04:00 AM\n Location: Carnivore Simba Saloon\n Host : Capital Group Limited',
        'image_url': 'https://i.ibb.co/4Sh28WM/event1.jpg'
    }
    return render(request, 'noughty_by_nature_detail.html', context)

def clean_energy_view(request):
    context = {
        'title': 'The Clean Energy Conference Australia Africa 2024',
        'description': 'The Clean Energy Conference has grown to become one of the most anticipated events in the field of clean and sustainable energy for the last seven years. In line with this, the theme of this year’s conference is “Clean Energy: The transition to a sustainable future”. It is a two-day program that will give participants the opportunity to share your expertise as well as hear from other experts and like-minded professionals and engage in discussions and opportunities in the clean energy sector.',
        'date': 'Friday, August 04, 2024\n Time: 08:00 AM - 05:00 PM\n Location: TBC\n Host: Australia Africa Energy and Minerals Institute',
        'image_url': 'https://i.ibb.co/GT6QyzR/event7.jpg'
    }
    return render(request, 'clean_energy_detail.html', context)


def africa_festival_view(request):
    context = {
        'title': 'FESTAC AFRICA FESTIVAL 2024',
        'description': 'The journey of FESTAC AFRICA Festival from Arusha to Kisumu marks a significant milestone in the festivals history, demonstrating its commitment to promoting African culture, unity, and artistic expression. This journey has been characterized by its growth, impact, and the revitalization of the festival on the African continent.',
        'date': 'Aug 18, 2024\n Time: 12:00 AM - 11:59 PM\n Location: KIsumu,Kenya\n Host : FESTAC AFRICA',
        'image_url': 'https://i.ibb.co/ByvCycY/event10.jpg'
    }
    return render(request, 'africa_festival_detail.html', context)

def music_gala_view(request):
    context = {
        'title': 'MUSIC Gala Event',
        'description': 'ANNUAL ADVENTIST MUSIC AWARDS CONCERT AND MUSIC Gala Event',
        'date': 'Aug 24, 2024\n Time: 09:00 AM - 06:00 PM\n Location: KICC\n Host : AMAC AWARDS',
        'image_url': 'https://i.ibb.co/7SppxWm/event3.jpg'
    }
    return render(request, 'music_gala_detail.html', context)

def nairobi_kingdom_view(request):
    context = {
        'title': 'Nairobi Kingdom World-Tour',
        'description': 'Kingdom Tour 2024 with Maverick City Music and Kirk Franklin is coming to Africa, Europe and Asia. Get ready for unforgetable experiences and to encounter God like never before. For Thine is the Kingdom. The Power and Glory. Forever and Ever. AMEN',
        'date': 'Aug 30, 2024\n Time: 05:00 PM - 10:00 PM\n Location: Uhuru Gardens\n Host : Lifession Publishing ',
        'image_url': 'https://i.ibb.co/tmFT817/event9.jpg'
    }
    return render(request, 'nairobi_kingdom_detail.html', context)

def biking_fest_view(request):
    context = {
        'title': 'HELLS GATE BIKING FEST 2024',
        'description': 'Have you ever imagined cycling or walking with your besties in the wild alongside zebras and giraffes, under towering rock cliffs, and then unwinding at a vibrant festival village!? Thats exactly what awaits you at the Hells Gate Biking Fest, Africas most unique cycling festival! This two-day annual extravaganza happening on the 10th & 11th of August 2024 isnt just for cyclists. Its a weekend adventure designed for everyone Picture this: You spend your day in a stunning national park with your pals - walking or cycling on a leisurely exploration.',
        'date': 'Sept 07, 2024\n Time: 07:00 AM - 06:00 PM\n Location: Hells Gate National Park\n Host : Whistle Africa Tours and Events',
        'image_url': 'https://i.ibb.co/mtknn2S/event8.jpg'
    }
    return render(request, 'biking_fest_detail.html', context)

def l_boogie_view(request):
    context = {
        'title': 'L Boogie',
        'description': ' Nairobi\'s Biggest Old Skool Party',
        'date': 'Sept 13, 2024\n Time: 05:00 PM - 06:00 AM\n Location: Carnivore Simba Saloon\n Host : DJ ADRIAN',
        'image_url': 'https://i.ibb.co/PrMDXL2/event6.jpg'
    }
    return render(request, 'clean_energy_detail.html', context)

def yakeyake_view(request):
    context = {
        'title': 'YAKE YAKE- Festival',
        'description': 'A night with the stars',
        'date': 'Sept 21, 2024\n Time: 10:00 AM - 12:00 AM\n Location: Millenium Park-Lugogo\n Host : AFRICAN SACRED IBIS ADVENTURES TOURS AND TRAVEL',
        'image_url': 'https://i.ibb.co/Dr5LT1d/event5.jpg'
    }
    return render(request, 'yakeyake_detail.html', context)

def nakuru_edition_view(request):
    context = {
        'title': 'NAKURU Edition',
        'description': 'The Maze Out of Town',
        'date': 'Sept 29, 2024\n Time: 08:00 AM - 06:00 PM\n Location: The Beam Grill and Lounge.\n Host : Saka Siri',
        'image_url': 'https://i.ibb.co/RvxQ6h6/event4.jpg'
    }
    return render(request, 'nakuru_edition_detail.html', context)

def sports_tournament_view(request):
    context = {
        'title': 'Motokhana Circuit Racing',
        'description': 'Head To Head: Motokhana Circuit Racing(KNTC ROUND 3)',
        'date': 'Sept 30, 2024\n Time: 08:00 AM - 04:00 PM\n Location: WRC Service Park\n Host : Delta Motorsports',
        'image_url': 'https://i.ibb.co/8Y4FP2X/event2.jpg'
    }
    return render(request, 'sports_tournament_detail.html', context)

def music_festival_view(request):
    context = {
        'title': 'The Clean Energy Conference Australia Africa 2024',
        'description': 'The Clean Energy Conference has grown to become one of the most anticipated events in the field of clean and sustainable energy for the last seven years. In line with this, the theme of this year’s conference is “Clean Energy: The transition to a sustainable future”. It is a two-day program that will give participants the opportunity to share your expertise as well as hear from other experts and like-minded professionals and engage in discussions and opportunities in the clean energy sector.',
        'date': 'Friday, Oct 5, 2024\n Time: 08:00 AM - 05:00 PM\n Location: TBC\n Host: Australia Africa Energy and Minerals Institute',
        'image_url': 'https://i.ibb.co/GT6QyzR/event7.jpg'
    }
    return render(request, 'music_festival_detail.html', context)

def dance_mania_view(request):
    context = {
        'title': 'Noughty By Nature - 2000s Party',
        'description': 'Don’t miss out on the event of the year – it’s going to be noughty but oh-so-nice!',
        'date': 'Oct 12, 2024\n Time: 06:00 PM - 04:00 AM\n Location: Carnivore Simba Saloon\n Host : Capital Group Limited',
        'image_url': 'https://i.ibb.co/4Sh28WM/event1.jpg'
    }
    return render(request, 'dance_mania_detail.html', context)

def art_expo_view(request):
    context = {
        'title': 'FESTAC AFRICA FESTIVAL 2024',
        'description': 'The journey of FESTAC AFRICA Festival from Arusha to Kisumu marks a significant milestone in the festivals history, demonstrating its commitment to promoting African culture, unity, and artistic expression. This journey has been characterized by its growth, impact, and the revitalization of the festival on the African continent.',
        'date': 'Aug 18, 2024\n Time: 12:00 AM - 11:59 PM\n Location: KIsumu,Kenya\n Host : FESTAC AFRICA',
        'image_url': 'https://i.ibb.co/ByvCycY/event10.jpg'
    }
    return render(request, 'art_expo_detail.html', context)

def film_festival_view(request):
    context = {
        'title': 'MUSIC Gala Event',
        'description': 'ANNUAL ADVENTIST MUSIC AWARDS CONCERT AND MUSIC Gala Event',
        'date': 'Aug 24, 2024\n Time: 09:00 AM - 06:00 PM\n Location: KICC\n Host : AMAC AWARDS',
        'image_url': 'https://i.ibb.co/7SppxWm/event3.jpg'
    }
    return render(request, 'film_festival_detail.html', context)

def food_fest_view(request):
    context = {
        'title': 'Nairobi Kingdom World-Tour',
        'description': 'Kingdom Tour 2024 with Maverick City Music and Kirk Franklin is coming to Africa, Europe and Asia. Get ready for unforgetable experiences and to encounter God like never before. For Thine is the Kingdom. The Power and Glory. Forever and Ever. AMEN',
        'date': 'Aug 30, 2024\n Time: 05:00 PM - 10:00 PM\n Location: Uhuru Gardens\n Host : Lifession Publishing ',
        'image_url': 'https://i.ibb.co/tmFT817/event9.jpg'
    }
    return render(request, 'food_fest_detail.html', context)





def buy_ticket(request):
    return render(request, 'buy_ticket.html')

def payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Implement STK push logic here (integration with Safaricom API)
        # Example: Use a service like Safaricom's Daraja API for STK push
        
        # Replace with actual integration code
        # Example: Assuming you have a MpesaClient class for STK push
        cl = MpesaClient()
        phone_number = str(phone)  # Ensure phone number is a string
        amount = 3000  # Replace with actual amount based on your ticket price logic
        account_reference = 'reference'  # Replace with a unique reference for each transaction
        transaction_desc = 'Ticket Purchase'  # Replace with a meaningful description
        
        # URL for callback from Safaricom API after payment
        callback_url = request.build_absolute_uri(reverse('stk_push_callback'))
        
        # Initiate STK push
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        
        # Assuming successful payment initiation, send email receipt
        send_mail(
            'Ticket Purchase Receipt',
            'Thank you for purchasing your ticket!',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
        # Redirect to a success page or display a success message
        return render(request, 'payment_success.html', {'name': name, 'phone': phone})
    
    return render(request, 'payment.html')

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_payment(request):
    # This function handles the actual payment processing logic
    # Example: Integrating with Safaricom's Daraja API for STK push
    # Placeholder for demonstration
    
    # For demo purposes, just returning a success message
    return HttpResponse('Payment processed successfully')

@csrf_exempt
def stk_push_callback(request):
    # Handle the callback data from Safaricom's API
    data = request.body  # This will contain the payload sent by Safaricom
    # Process the callback data as per your integration requirements
    
    # Respond with a success message to Safaricom
    return HttpResponse("Payment processed successfully👋")









