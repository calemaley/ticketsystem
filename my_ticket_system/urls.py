from django.contrib import admin
from django.urls import path, include
from events import views as event_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', event_views.custom_login, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', event_views.homepage, name='homepage'),
    path('dashboard/', event_views.dashboard, name='dashboard'),
    path('register/', event_views.register, name='register'),
    path('contact/', event_views.contact_us, name='contact'),
    path('dashboard/event-manage/', event_views.event_manage, name='dashboard-eventmanage'),
    path('dashboard/book-tickets/', event_views.book_ticket, name='dashboard-bookingtickets'),
    path('dashboard/reviews/', event_views.review_list, name='dashboard-reviewlist'),
    path('chat/', event_views.chat_view, name='chat'),
    path('dashboard/', event_views.customer_dashboard, name='customer-dashboard'),
    path('event/<int:event_id>/', event_views.event_details, name='event-details'),
    path('ticket/manage/<int:ticket_id>/', event_views.manage_ticket, name='manage-ticket'),
    path('submit_review/', event_views.submit_review, name='submit-review'),
    path('events/update/<int:pk>/', event_views.event_update, name='dashboard-eventupdate'),
    path('events/delete/<int:pk>/', event_views.event_delete, name='dashboard-eventdelete'),
    
]

