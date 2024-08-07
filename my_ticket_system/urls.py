from django.contrib import admin
from django.urls import path, include
from events import views as event_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_views.homepage, name='homepage'),
    path('splash/', event_views.splash_page, name='splash_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('events/', event_views.events_page, name='events_page'),
    path('dashboard/', event_views.dashboard, name='dashboard'),
    path('register/', event_views.register, name='register'),
     path('login/', event_views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('contact/', event_views.contact, name='contact'),
    path('admin_chat_view', event_views.admin_chat_view, name='admin_chat_view'),
    path('delete_message/<int:message_id>/',event_views.delete_message, name='delete_message'),
    path('events/<int:event_id>/', event_views.event_detail, name='event_detail'),
    path('buy_ticket/', event_views.buy_ticket, name='buy_ticket'),
    path('payment/', event_views.payment, name='payment'),
    path('process_payment/', event_views.process_payment, name='process_payment'),
    path('stk_push_callback/', event_views.stk_push_callback, name='stk_push_callback'),
    path('sales/', event_views.sales, name='sales'),
    path('create/', event_views.create_event_view, name='create_event'),
    path('events/', event_views.events_page_view, name='events_page'),
    path('admin/events/update/<int:event_id>/', event_views.update_event_view, name='update_event'),
    path('admin/events/delete/<int:event_id>/', event_views.delete_event_view, name='delete_event'),
    path('create_ticket_type', event_views.create_ticket_type_view, name='create_ticket_type'),
    path('update_ticket_type', event_views.update_ticket_type_view, name='update_ticket_type'),
    path('ticket_type_list', event_views.ticket_type_list, name='ticket_type_list'),
    path('delete_ticket_type', event_views.delete_ticket_type_view, name='delete_ticket_type'),   

    

    # Event-specific views
    path('noughty_by_nature/', event_views.noughty_by_nature_view, name='noughty_by_nature_view'),
    path('clean_energy/', event_views.clean_energy_view, name='clean_energy_view'),
    path('africa_festival/', event_views.africa_festival_view, name='africa_festival_view'),
    path('music_gala/', event_views.music_gala_view, name='music_gala_view'),
    path('nairobi_kingdom/', event_views.nairobi_kingdom_view, name='nairobi_kingdom_view'),
    path('biking_fest/', event_views.biking_fest_view, name='biking_fest_view'),
    path('l_boogie/', event_views.l_boogie_view, name='l_boogie_view'),
    path('yakeyake/', event_views.yakeyake_view, name='yakeyake_view'),
    path('nakuru_edition/', event_views.nakuru_edition_view, name='nakuru_edition_view'),
    path('sports_tournament/', event_views.sports_tournament_view, name='sports_tournament_view'),
    path('music_festival/', event_views.music_festival_view, name='music_festival_view'),
    path('art_expo/', event_views.art_expo_view, name='art_expo_view'),
    path('dance_mania/', event_views.dance_mania_view, name='dance_mania_view'),
    path('film_festival/', event_views.film_festival_view, name='film_festival_view'),
    path('food_fest/', event_views.food_fest_view, name='food_fest_view'),
]
