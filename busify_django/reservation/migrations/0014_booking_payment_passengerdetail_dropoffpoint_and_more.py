# Generated by Django 4.2.16 on 2024-12-02 04:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0013_seat_is_held'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('travel_date', models.DateField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('coupon_code', models.CharField(blank=True, max_length=50, null=True)),
                ('ev_discount_applied', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.buses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('Success', 'Success'), ('Failed', 'Failed'), ('Pending', 'Pending')], max_length=20)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.booking')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('boarding_point', models.CharField(max_length=255)),
                ('drop_off_point', models.CharField(max_length=255)),
                ('meal_preference', models.CharField(choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Jain', 'Jain')], max_length=20)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.booking')),
            ],
        ),
        migrations.CreateModel(
            name='DropOffPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(max_length=255)),
                ('sequence', models.IntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.route')),
            ],
        ),
        migrations.CreateModel(
            name='BoardingPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(max_length=255)),
                ('sequence', models.IntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.route')),
            ],
        ),
    ]