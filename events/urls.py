from django.urls import path
from . import views

urlpatterns = [
    path('', views.event, name='event-page'),
    path('eventdetail/<int:pk>/',views.event_detail, name="event-detail"),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('admindashboard/', views.admin_dashboard, name="admin"),
    path('eventlist/',views.event_list, name='event-list'),
    path('createevent/',views.create_event, name='create-event'),
    path('eventupdate/<int:pk>/', views.event_update, name="event-update"),
    path('eventdelete/<int:pk>/', views.event_delete, name="event-delete"),
    path('contact/', views.contact, name='contact'),
    #tickets urls
    path('createtickets/',views.create_ticket, name='create-ticket'),
    path('ticketlist/',views.ticket_list, name='ticket-list'),
    path('tickettupdate/<int:pk>/', views.ticket_update, name="ticket-update"),
    path('ticketdelete/<int:pk>/', views.ticket_delete, name="ticket-delete"),
    path('sales/', views.sales, name="ticket-sales"),
    #admin code 
    path('adminevents/',views.admin_events, name='admin-events'),
    path('admintickets/',views.admin_tickets, name='admin-tickets'),


   
    
]