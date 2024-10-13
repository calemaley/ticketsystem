from django.urls import path
from . import views
from .views import past_events
from .views import search_suggestions
from .views import search_events
from .views import location_suggestions


urlpatterns = [
    path('', views.home, name='home'),
    path('eventpage/', views.event, name='event-page'),
    path('events/type/<str:event_type>/', views.event, name='events-by-type'),
    path('eventdetail/<int:pk>/',views.event_detail, name="event-detail"),
    path('book-tickets/<int:event_id>/', views.book_tickets, name='book_tickets'),
    path('search/', views.search_events, name='search_events'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('admindashboard/', views.admin_dashboard, name="admin"),
    path('eventlist/',views.event_list, name='event-list'),
    path('createevent/',views.create_event, name='create-event'),
    path('eventupdate/<int:pk>/', views.event_update, name="event-update"),
    path('eventdelete/<int:pk>/', views.event_delete, name="event-delete"),
    path('contact/', views.contact, name='contact'),
    path('featured/', views.featured_events, name='featured-events'),
    path('upcoming/', views.upcoming_events, name='upcoming-events'),
    path('giveaway/', views.giveaway_events, name='giveaway-events'),
    path('past-events/', past_events, name='past-events'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),
    path('location-suggestions/', location_suggestions, name='location_suggestions'),
    path('search-events/', search_events, name='search_events'),
    path('generate-ticket-pdf/<int:ticket_id>/', views.generate_ticket_pdf, name='generate-ticket-pdf'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('send-ticket-via-sms/<int:ticket_id>/', views.send_ticket_via_sms, name='send_ticket_via_sms'),
    path('enter-phone-number/<int:ticket_id>/', views.enter_phone_number, name='enter_phone_number'),
    

    
  
    #tickets urls
    path('createtickets/',views.create_ticket, name='create-ticket'),
    path('ticketlist/',views.ticket_list, name='ticket-list'),
    path('tickettupdate/<int:pk>/', views.ticket_update, name="ticket-update"),
    path('ticketdelete/<int:pk>/', views.ticket_delete, name="ticket-delete"),
    path('tickets-with-pdf/', views.list_tickets_with_pdf, name='tickets_with_pdf'),
    path('edit-ticket/<int:ticket_id>/', views.edit_ticket, name='edit-ticket'),
    path('delete-ticket-pdf/<int:ticket_id>/', views.delete_ticket_pdf, name='delete_ticket_pdf'),
    path('sales/', views.sales, name="ticket-sales"),   
    
    #admin code 
    path('adminevents/',views.admin_events, name='admin-events'),
    path('admintickets/',views.admin_tickets, name='admin-tickets'),
    path('dashboard/event/<int:id>/', views.admin_event_detail, name='admin-event-detail'),
    path('sales/', views.sales_analysis, name='sales'),
    path('otp/', views.otp_page, name='otp_page'),


   
    
]