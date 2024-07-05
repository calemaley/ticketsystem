# events/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('noughty_by_nature/', views.noughty_by_nature_view, name='noughty_by_nature_view'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),  
    path('event/buy/', views.buy_ticket, name='buy_ticket'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/event-manage/', views.event_manage, name='dashboard-eventmanage'),
    path('dashboard/book-tickets/', views.book_ticket, name='dashboard-bookingtickets'),
    path('dashboard/reviews/', views.review_list, name='dashboard-reviewlist'),
    path('customer/dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('events/update/<int:pk>/', views.event_update, name='dashboard-eventupdate'),
    path('events/delete/<int:pk>/', views.event_delete, name='dashboard-eventdelete'),
    path('tickets/update/<int:pk>/', views.ticket_update, name='dashboard-ticketupdate'),
    path('tickets/delete/<int:pk>/', views.ticket_delete, name='dashboard-ticketdelete'),
    path('reviews/add/', views.add_review, name='dashboard-addreview'),
    path('reviews/delete/<int:pk>/', views.review_delete, name='dashboard-reviewdelete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('chat/', views.chat_view, name='chat'),
    path('admin-chat/', views.admin_chat_view, name='admin-chat'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]
