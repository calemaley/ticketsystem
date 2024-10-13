# Generated by Django 5.1 on 2024-09-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_ticket_is_approved_ticket_user_alter_event_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='advance_ticket_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='event',
            name='gate_adult_ticket_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='event',
            name='gate_kid_ticket_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
