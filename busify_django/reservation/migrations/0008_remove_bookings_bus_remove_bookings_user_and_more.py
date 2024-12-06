# Generated by Django 4.2.16 on 2024-11-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_bookings_buses_coupons_meals_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='bus',
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='user',
        ),
        migrations.DeleteModel(
            name='Coupons',
        ),
        migrations.DeleteModel(
            name='Meals',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.RenameField(
            model_name='buses',
            old_name='bus_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='buses',
            name='available_seats',
        ),
        migrations.RemoveField(
            model_name='buses',
            name='boarding_points',
        ),
        migrations.RemoveField(
            model_name='buses',
            name='bus_type',
        ),
        migrations.RemoveField(
            model_name='buses',
            name='drop_points',
        ),
        migrations.RemoveField(
            model_name='buses',
            name='from_location',
        ),
        migrations.RemoveField(
            model_name='buses',
            name='to_location',
        ),
        migrations.AddField(
            model_name='buses',
            name='is_ev',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buses',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='buses',
            name='rating_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='buses',
            name='type',
            field=models.CharField(choices=[('AC Sleeper', 'AC Sleeper'), ('Non AC Sleeper', 'Non AC Sleeper'), ('AC Seater', 'AC Seater'), ('Non AC Seater', 'Non AC Seater')], default='Non AC Seater', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buses',
            name='total_seats',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Bookings',
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
