from django.contrib import admin
from .models import Route, Buses, Seat, Booking, PassengerDetail

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('from_location', 'to_location', 'boarding_points', 'dropoff_points')
    search_fields = ('from_location', 'to_location')

@admin.register(Buses)
class BusesAdmin(admin.ModelAdmin):
    list_display = ('name', 'route', 'departure_time', 'arrival_time', 'type', 'is_ev', 'rating', 'total_seats', 'get_available_seats')
    list_filter = ('type', 'is_ev')
    search_fields = ('name', 'route__from_location', 'route__to_location')

    def get_available_seats(self, obj):
        return obj.total_seats - obj.booked_seats
    get_available_seats.short_description = 'Available Seats'

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'section', 'bus', 'is_booked', 'is_held', 'booked_by')
    list_filter = ('section', 'is_booked', 'is_held', 'bus')

admin.site.register(Booking)
admin.site.register(PassengerDetail)