# Generated by Django 4.2.16 on 2024-12-01 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0011_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=10)),
                ('is_booked', models.BooleanField(default=False)),
                ('booked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='reservation.buses')),
            ],
            options={
                'unique_together': {('bus', 'seat_number')},
            },
        ),
    ]
