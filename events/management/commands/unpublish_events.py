from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event

class Command(BaseCommand):
    help = 'Unpublish past events that have already happened'

    def handle(self, *args, **kwargs):
        # Get current date and time
        current_time = timezone.now()

        # Find events that are past and still published
        past_events = Event.objects.filter(date__lt=current_time.date(), is_published=True)

        # Unpublish those events
        for event in past_events:
            event.is_published = False
            event.save()

        # Output how many events were unpublished
        self.stdout.write(self.style.SUCCESS(f'Successfully unpublished {past_events.count()} past events.'))
