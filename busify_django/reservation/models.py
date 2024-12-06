from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

# Signals to create and save UserProfile when a User is created or saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Route(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    boarding_points = models.JSONField(default=list)  # List of boarding points
    dropoff_points = models.JSONField(default=list)  # List of drop-off points

    def __str__(self):
        return f"{self.from_location} to {self.to_location}"

class Buses(models.Model):
    name = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='buses')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    type = models.CharField(max_length=50, choices=[
        ('AC Sleeper', 'AC Sleeper'),
        ('Non AC Sleeper', 'Non AC Sleeper'),
        ('AC Seater', 'AC Seater'),
        ('Non AC Seater', 'Non AC Seater'),
    ])
    base_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_ev = models.BooleanField(default=False)  # EV bus flag
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    total_seats = models.IntegerField()
    booked_seats = models.IntegerField(default=0)



    def journey_duration(self):
        """Calculate the journey duration as a formatted string."""
        duration = self.arrival_time - self.departure_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes = remainder // 60
        return f"{int(hours)}h {int(minutes)}m"


    def __str__(self):
        return self.name

class Seat(models.Model):
    SECTION_CHOICES = [
        ('Upper', 'Upper'),
        ('Lower', 'Lower'),
    ]
    bus = models.ForeignKey('Buses', related_name="seats", on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)  # E.g., A1, B2, C3, etc.
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, default='Lower')
    is_booked = models.BooleanField(default=False)  # True if the seat is booked
    is_held = models.BooleanField(default=False)  # Temporarily reserved
    booked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # User who booked the seat, if any

    def __str__(self):
        return f"Seat {self.seat_number} ({self.section}) on {self.bus.name}"

    class Meta:
        unique_together = ('bus', 'seat_number')


class BoardingPoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    point = models.CharField(max_length=255)
    sequence = models.IntegerField()

class DropOffPoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    point = models.CharField(max_length=255)
    sequence = models.IntegerField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey('Buses', on_delete=models.CASCADE)
    booking_date = models.DateField(null=True)
    travel_date = models.DateField(null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    ev_discount_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Added fields to manage the meal cost and discount status
    meal_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_total_cost(self):
        """Calculate the total cost including meal preferences and discounts."""
        # Primary passenger meal cost
        primary_meal_cost = self.passengerdetail_set.filter(status='primary').first().calculate_meal_cost() if self.passengerdetail_set.filter(status='primary').exists() else 0
        
        # Co-passenger meal cost
        co_meal_cost = sum([passenger.calculate_meal_cost() for passenger in self.passengerdetail_set.filter(status='co_passenger')])

        # Total meal cost
        self.meal_cost = primary_meal_cost + co_meal_cost

        self.total_cost = self.bus.base_fare + self.meal_cost
        
        # Apply EV discount if applicable
        if self.ev_discount_applied:
            self.discount_amount = self.total_cost * 0.10  # EV discount: 10%
        else:
            self.discount_amount = 0
        
        # Final cost after applying any discounts
        self.final_cost = self.total_cost - self.discount_amount
        self.save()

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} on {self.booking_date}"

class PassengerDetail(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    boarding_point = models.CharField(max_length=255)
    drop_off_point = models.CharField(max_length=255)
    SEAT_STATUSES = [('primary', 'Primary Passenger'), ('co_passenger', 'Co-Passenger')]
    MEAL_PREFERENCES = [('veg', 'Vegetarian'), ('nonveg', 'Non-Vegetarian'), ('none', 'No Meal')]
    meal_preference = models.CharField(max_length=10, choices=MEAL_PREFERENCES)
    status = models.CharField(max_length=20, choices=SEAT_STATUSES, default='co_passenger')

    def calculate_meal_cost(self):
        """Calculate meal cost based on the passenger's choice."""
        if self.meal_preference == 'veg':
            return 200
        elif self.meal_preference == 'nonveg':
            return 250
        elif self.meal_preference == 'none':
            return 0
        return 0

    def __str__(self):
        return f"Passenger {self.full_name} for Booking {self.booking.id}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed'), ('Pending', 'Pending')])
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)


@receiver(post_save, sender=Buses)
def create_default_seats(sender, instance, created, **kwargs):
    if created:  # Only create seats for newly created buses
        for i in range(1, 17):  # Seats 1 to 16
            # Create Upper Section Seats
            Seat.objects.create(
                bus=instance,
                seat_number=f"U{i}",  # U1, U2, ..., U16
                section='Upper',
                is_booked=False,
                is_held=False
            )
        for i in range(1, 17):  # Seats 1 to 16 again for Lower Section
            # Create Lower Section Seats
            Seat.objects.create(
                bus=instance,
                seat_number=f"L{i}",  # L1, L2, ..., L16
                section='Lower',
                is_booked=False,
                is_held=False
            )