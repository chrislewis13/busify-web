# Generated by Django 4.2.16 on 2024-11-20 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bus_type', models.CharField(max_length=50)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('journey_duration', models.DurationField()),
                ('departure_location', models.CharField(max_length=100)),
                ('arrival_location', models.CharField(max_length=100)),
                ('boarding_point', models.CharField(max_length=150)),
                ('dropping_point', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('seats_available', models.IntegerField()),
                ('rating', models.FloatField()),
                ('amenities', models.JSONField()),
            ],
        ),
    ]