# Generated by Django 4.2.16 on 2024-11-22 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_alter_bus_arrival_time_alter_bus_departure_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
