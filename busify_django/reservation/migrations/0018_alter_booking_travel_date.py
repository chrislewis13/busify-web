# Generated by Django 4.2.16 on 2024-12-05 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0017_passengerdetail_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='travel_date',
            field=models.DateField(null=True),
        ),
    ]
