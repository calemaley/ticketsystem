# events/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Event, Ticket, Review, Chat, Notification
from .forms import EventForm, TicketForm, ReviewForm, ChatForm, RegistrationForm
from django.contrib.auth import logout, login
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django_daraja.mpesa.core import MpesaClient
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Sales, Event
from .models import Chat
from .forms import ChatForm
from django.utils import timezone




def splash_page(request):
    return render(request, 'splash.html')


def dashboard(request):
    # Fetch data for the dashboard
    events_count = Event.objects.count()  # Example for events count
    users_count = User.objects.count()    # Example for users count
    sales_data = Sales.objects.all()       # Example for fetching sales data
    
    # Calculate ticket purchases based on sales data
    ticket_purchases = sales_data.count()  
    
    context = {
        'events_count': events_count,
        'users_count': users_count,
        'sales_data': sales_data,
        'ticket_purchases': ticket_purchases,
    }
    return render(request, 'dashboard/dashboard.html', context)

def contact_us(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.timestamp = timezone.now()
            message.save()
            return JsonResponse({
                'success': True,
                'user': message.user.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    else:
        form = ChatForm()

    messages = Chat.objects.all().order_by('timestamp')
    return render(request, 'contact.html', {'messages': messages, 'form': form})

def admin_chat_view(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.timestamp = timezone.now()
            message.save()
            return JsonResponse({
                'success': True,
                'user': message.user.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    else:
        form = ChatForm()

    messages = Chat.objects.all().order_by('timestamp')
    return render(request, 'admin_chat.html', {'messages': messages, 'form': form})

@login_required
def delete_message(request, message_id):
    message = Chat.objects.get(id=message_id)
    if request.user == message.recipient or request.user.is_staff:
        message.delete()
    return redirect('admin_chat_view' if request.user.is_staff else 'contact_us')


logger = logging.getLogger(__name__)


def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info('Event created successfully')
            messages.success(request, 'Event created successfully!')
            return redirect('events_page')
        else:
            logger.error('Form errors: %s', form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

def dashboard_view(request):
    events = Event.objects.all()
    sales_data = Sales.objects.all()
    users = User.objects.all()  # Query to fetch all users

    context = {
        'events': events,
        'sales_data': sales_data,
        'users': users,  # Include users count in the context
    }
    return render(request, 'events/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('dashboard')
                else:
                    messages.info(request, 'You do not have permission to access the dashboard.')
                    return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_details.html', {'event': event})


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

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})

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


def contact(request):
    return render(request, 'contact.html')


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
@csrf_exempt  # Ensure CSRF exemption for testing purposes
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
        
        # Call STK push function from your MpesaClient or equivalent
        response = cl.stk_push(phone_number, amount, account_reference)
        
        # Handle response and redirect as needed
        if response.success:  # Adjust based on your MpesaClient response structure
            # Payment successful, update your database or process order
            return render(request, 'payment_success.html', {'message': 'Payment successful!'})
        else:
            # Payment failed or other error, handle appropriately
            return render(request, 'payment_failed.html', {'message': 'Payment failed. Please try again.'})
    
    # Handle GET request or invalid requests
    return HttpResponse('Invalid request')


@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        total_amount = request.POST.get('total_amount')  # Ensure you pass this value from the form

        # Implement STK push logic
        cl = MpesaClient(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET,
                         settings.MPESA_INITIATOR_NAME, settings.MPESA_INITIATOR_PASSWORD,
                         settings.MPESA_SHORTCODE, settings.MPESA_PASSKEY)

        amount = int(total_amount)  # Convert to integer (amount in cents)
        account_reference = 'Ticket Purchase'
        transaction_desc = 'Payment for event ticket'

        # Use the phone number from the form
        phone_number = str(phone)

        # Assuming callback URL for payment success/failure handling
        callback_url = 'https://your-callback-url-for-payment-status'

        # Initiate STK push
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        # Send email receipt
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


@csrf_exempt
def stk_push_callback(request):
    data = request.body.decode('utf-8')
    # Handle the callback data as needed (update transaction status, send confirmation, etc.)
    return HttpResponse("Payment processed successfully👋")



def sales(request):
    # Replace with actual logic to fetch sales data
    sales_data = [
        {'name': 'Jeremiah Samson', 'email': 'jere.sam@gmail.com', 'phone': '+1234567890', 'date': '2024-07-09 15:30', 'success': True},
        {'name': 'Jane walter', 'email': 'janew@yahoo.com', 'phone': '+1987654321', 'date': '2024-07-08 12:45', 'success': True},
        # Add more data as needed
    ]
    return render(request, 'sales.html', {'sales_data': sales_data})











