# Generated by Django 4.2.16 on 2024-12-04 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_booking_discount_amount_booking_final_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passengerdetail',
            name='email',
            field=models.EmailField(default='example@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passengerdetail',
            name='phone',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
    ]
