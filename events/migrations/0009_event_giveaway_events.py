# Generated by Django 5.1 on 2024-08-19 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_event_event_type_alter_ticket_ticket_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='giveaway_events',
            field=models.BooleanField(default=False),
        ),
    ]
