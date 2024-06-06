from django.urls import path
from . import views
from .views import homepage, index, event_manage, event_update, event_delete, book_ticket, ticket_update, ticket_delete, add_review, review_list, review_delete, logout_user, chat_view, admin_chat_view

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dashboard/', index, name='dashboard-index'),
    path('events/', event_manage, name='dashboard-eventmanage'),
    path('events/update/<int:pk>/', event_update, name='dashboard-eventupdate'),
    path('events/delete/<int:pk>/', event_delete, name='dashboard-eventdelete'),
    path('tickets/', book_ticket, name='dashboard-bookingtickets'),
    path('tickets/update/<int:pk>/', ticket_update, name='dashboard-ticketupdate'),
    path('tickets/delete/<int:pk>/', ticket_delete, name='dashboard-ticketdelete'),
    path('reviews/', add_review, name='dashboard-addreview'),
    path('reviews/list/', review_list, name='dashboard-reviewlist'),
    path('reviews/delete/<int:pk>/', review_delete, name='dashboard-reviewdelete'),
    path('logout/', logout_user, name='logout'),
    path('chat/', chat_view, name='chat'),
    path('admin-chat/', admin_chat_view, name='admin-chat'),
]

