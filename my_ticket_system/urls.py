from django.contrib import admin
from django.urls import path, include
from events import views as event_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_views.homepage, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', event_views.custom_login, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('events/', event_views.events_page, name='events_page'),
    path('dashboard/', event_views.dashboard, name='dashboard'),
    path('contact/', event_views.contact, name='contact'),
    path('events/<int:event_id>/', event_views.event_detail, name='event_detail'),
    path('buy_ticket/', event_views.buy_ticket, name='buy_ticket'),
    path('payment/', event_views.payment, name='payment'),
    path('process_payment/', event_views.process_payment, name='process_payment'),
    path('stk_push_callback/', event_views.stk_push_callback, name='stk_push_callback'),

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
