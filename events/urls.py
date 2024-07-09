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
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
]
