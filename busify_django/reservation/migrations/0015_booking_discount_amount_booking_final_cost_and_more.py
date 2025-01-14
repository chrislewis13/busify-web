# Generated by Django 4.2.16 on 2024-12-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0014_booking_payment_passengerdetail_dropoffpoint_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='final_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='meal_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='seat',
            name='section',
            field=models.CharField(choices=[('Upper', 'Upper'), ('Lower', 'Lower')], default='Lower', max_length=10),
        ),
    ]
