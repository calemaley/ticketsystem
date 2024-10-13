from django.contrib import admin
from .models import Event, Ticket, Payment
from django.contrib.admin.models import LogEntry
from django.core.mail import send_mail

class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at')
    
    def payment_initiated(self):
        # This method checks for payments with 'initiated' status and notifies the admin
        payments_pending = Payment.objects.filter(status='initiated')
        if payments_pending.exists():
            return f"{payments_pending.count()} new payments awaiting approval."
        return "No pending payments."

    # Modify changelist_view to display payment notifications
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['payment_notifications'] = self.payment_initiated()
        return super().changelist_view(request, extra_context=extra_context)

    def payment_notification_display(self, request):
        """ Display payment notifications to the admin """
        pending_message = self.payment_initiated()
        self.message_user(request, pending_message)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'ticket_type', 'amount', 'is_approved')
    actions = ['approve_tickets']

    def approve_tickets(self, request, queryset):
        # Approve selected tickets and send an email to the user
        for ticket in queryset:
            ticket.is_approved = True
            ticket.save()
            self.send_ticket_email(ticket)
        self.message_user(request, "Selected tickets have been approved, and emails have been sent.")

    # Function to send a ticket email to the user
    def send_ticket_email(self, ticket):
        subject = f"Your Ticket for {ticket.event.name}"
        message = (
            f"Hello {ticket.user.first_name},\n\n"
            f"Your ticket for {ticket.event.name} has been approved.\n"
            f"Ticket Type: {ticket.ticket_type}, Amount: {ticket.amount}.\n"
            f"Enjoy the event!\n\n"
            f"Best Regards,\nEvent Management Team"
        )
        # Replace 'noreply@eventmanagement.com' with your actual email
        send_mail(subject, message, 'noreply@eventmanagement.com', [ticket.user.email])
    
    approve_tickets.short_description = "Approve selected tickets"

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'is_published', 'is_approved')
    actions = ['approve_events']

    def approve_events(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected events have been approved.")
    approve_events.short_description = "Approve selected events"

# Register models in admin panel
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Payment, PaymentNotificationAdmin)
