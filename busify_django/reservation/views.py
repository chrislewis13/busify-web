from django.shortcuts import render
from .models import Buses, Seat, Booking, PassengerDetail, Payment, BoardingPoint, DropOffPoint
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, PrimaryPassengerForm, CoPassengerForm, HelpForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.http import Http404
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime
from decimal import Decimal
from django.core.mail import send_mail


def home(request):
    return render(request, "reservation/index.html")

def help(request):
    return render(request, "reservation/help.html")

def account(request):
    return render(request, "reservation/account-info.html")

def search_buses(request):
    if request.method == 'GET':
        # Get the filters from the GET parameters
        from_location = request.GET.get('from_location')
        to_location = request.GET.get('to_location')
        travel_date = request.GET.get('travel_date')
        departure_time_filters = request.GET.getlist('departure_time')
        bus_type_filters = request.GET.getlist('bus_type')
        price_range_filters = request.GET.getlist('price_range')
        sort_by = request.GET.get('sort_by')

        # Validate inputs
        if not from_location or not to_location or not travel_date:
            return render(request, 'reservation/index.html', {'error': 'All fields are required!'})

        try:
            travel_date_obj = datetime.strptime(travel_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'reservation/index.html', {'error': 'Invalid travel date format!'})

        # Base query to filter buses by location and date
        buses = Buses.objects.filter(
            route__from_location=from_location,
            route__to_location=to_location,
            departure_time__date=travel_date_obj
        ).select_related('route')

        # Apply filters for Departure Time (Morning, Afternoon, etc.)
        if departure_time_filters:
            # Here, map each time range to a corresponding time range filter in the query
            time_filters = {
                'morning': (6, 12),
                'afternoon': (12, 16),
                'evening': (16, 20),
                'night': (20, 24)
            }
            buses = buses.filter(departure_time__hour__gte=time_filters[departure_time_filters[0]][0], departure_time__hour__lt=time_filters[departure_time_filters[0]][1])

        # Apply filters for Bus Type (AC Sleeper, Non AC Sleeper, etc.)
        if bus_type_filters:
            buses = buses.filter(bus_type__in=bus_type_filters)

        # Apply filters for Price Range (Below ₹500, ₹500 - ₹1000, etc.)
        if price_range_filters:
            price_ranges = {
                'below_500': (0, 500),
                '500_1000': (500, 1000),
                '1000_1500': (1000, 1500),
                'above_1500': (1500, float('inf'))
            }
            price_filter = price_ranges[price_range_filters[0]]
            buses = buses.filter(base_fare__gte=price_filter[0], base_fare__lte=price_filter[1])

        # Apply sorting based on selected criteria
        if sort_by == "price_asc":
            buses = buses.order_by('base_fare')
        elif sort_by == "price_desc":
            buses = buses.order_by('-base_fare')
        elif sort_by == "departure_time":
            buses = buses.order_by('departure_time')
        elif sort_by == "duration":
            buses = buses.order_by('journey_duration')  # Assuming you have a method to calculate journey time
        elif sort_by == "seats_available":
            buses = buses.order_by('-remaining_seats')

        # Add additional attributes to buses
        for bus in buses:
            bus.remaining_seats = bus.total_seats - bus.booked_seats
            bus.journey_time = bus.journey_duration()  # Add journey duration calculation
            bus.drop_off_points = bus.route.dropoff_points

        # Check if buses were found
        bus_count = buses.count()

        # Return filtered buses to the template
        return render(request, 'reservation/buslist.html', {
            'buses': buses,
            'source_city': from_location,
            'destination_city': to_location,
            'journey_date': travel_date_obj.strftime('%d %B %Y'),
            'bus_count': bus_count
        })

@login_required
def account_view(request):
    if request.method == 'POST':
        # Handle update of user details (email & phone)
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        user = request.user
        user.profile.phone = phone
        user.email = email
        user.save()
        user.profile.save()

        messages.success(request, 'Your information has been updated successfully.')
        return redirect('account')  # Redirect to account page
    
    return render(request, 'account.html')
# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()

            if not hasattr(user, 'profile'):
                    # Create the UserProfile if it doesn't exist
                    profile = UserProfile(user=user)
                    profile.full_name = form.cleaned_data.get('full_name')
                    profile.phone = form.cleaned_data.get('phone')
                    profile.save()

            # Log in the user
            login(request, user)

            # Add success message
            messages.success(request, "User created successfully! You are now logged in.")
            return redirect('home')  # Redirect to home or a success page
        else:
            print(form.errors)
            messages.error(request, "There was an error with the form. Please try again.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'reservation/login-signup.html', {'form': form, 'is_signup': True})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate and log in the user
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home or a success page
    else:
        form = AuthenticationForm()
    return render(request, 'reservation/login-signup.html', {'form': form, 'is_signup': False})

#for seat

def seat_selection(request, bus_id):
    try:
        bus = Buses.objects.get(id=bus_id)
    except Buses.DoesNotExist:
        return HttpResponse("Bus not found", status=404)

    # Logic for handling seat selection
    return render(request, 'reservation/seat.html', {'bus': bus})

# Login view for redirection
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)  # Redirect to next or home page
    else:
        form = AuthenticationForm()
    return render(request, 'reservation/login-signup.html', {'form': form, 'is_signup': False})

@login_required
def seat_selection(request, bus_id):
    bus = get_object_or_404(Buses, id=bus_id)
    seats = Seat.objects.filter(bus=bus)

    # Prepare seat groups

    upper_deck_group_1 = []
    upper_deck_group_2 = []
    lower_deck_group_1 = []
    lower_deck_group_2 = []

    for seat in seats:
        seat_number = seat.seat_number  # e.g., 'U1', 'L9', etc.
        deck = seat_number[0]  # 'U' or 'L' (upper or lower deck)
        try:
            number = int(seat_number[1:])  # Convert numeric part to an integer
        except ValueError:
            number = 0  # Fallback for invalid seat numbers

        if deck == "U":  # Upper Deck Seats
            if 1 <= number <= 8:
                upper_deck_group_1.append({
                    'id': seat.id,
                    'seat_number': seat.seat_number,
                    'is_booked': seat.is_booked,
                    'is_held': seat.is_held,
                })
            elif 9 <= number <= 16:
                upper_deck_group_2.append({
                    'id': seat.id,
                    'seat_number': seat.seat_number,
                    'is_booked': seat.is_booked,
                    'is_held': seat.is_held,
                })
        elif deck == "L":  # Lower Deck Seats
            if 1 <= number <= 8:
                lower_deck_group_1.append({
                    'id': seat.id,
                    'seat_number': seat.seat_number,
                    'is_booked': seat.is_booked,
                    'is_held': seat.is_held,
                })
            elif 9 <= number <= 16:
                lower_deck_group_2.append({
                    'id': seat.id,
                    'seat_number': seat.seat_number,
                    'is_booked': seat.is_booked,
                    'is_held': seat.is_held,
                })

    return render(request, 'reservation/seat.html', {
        'bus': bus,
        'bus_base_fare': bus.base_fare,
        'upper_deck_group_1': upper_deck_group_1,
        'upper_deck_group_2': upper_deck_group_2,
        'lower_deck_group_1': lower_deck_group_1,
        'lower_deck_group_2': lower_deck_group_2,
    })

@login_required
def hold_seat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seat_ids = data.get('seats')  # Get the list of seat IDs
            
            if not seat_ids or not isinstance(seat_ids, list):
                return JsonResponse({"success": False, "message": "Seat IDs are required and must be a list."})

            held_seats = []
            for seat_id in seat_ids:
                try:
                    seat = Seat.objects.get(id=seat_id, is_booked=False, is_held=False)
                    seat.is_held = True
                    seat.booked_by = request.user
                    seat.save()
                    held_seats.append(seat_id)
                except Seat.DoesNotExist:
                    continue  # Skip seats that are already held or booked

            if not held_seats:
                return JsonResponse({"success": False, "message": "None of the seats could be held."})

            return JsonResponse({"success": True, "message": f"Seats held successfully: {held_seats}"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid request method."})

def passenger_form(request, bus_id):
    # Fetch the selected bus details
    bus = get_object_or_404(Buses, id=bus_id)
    route = bus.route

    boarding_points = route.boarding_points  # This will be a list from the JSONField
    dropoff_points = route.dropoff_points    # This will be a list from the JSONField

    # Debugging output
    print("Boarding Points:", boarding_points)
    print("Drop-off Points:", dropoff_points)

    context = {
        'bus': bus,
        'boarding_points': boarding_points,
        'dropoff_points': dropoff_points,
        'base_fare': bus.base_fare,
    }

    # Render the passenger form template with the bus details
    return render(request, 'reservation/pessenger-form.html', {**context, 'bus': bus})


@method_decorator(csrf_exempt, name='dispatch')
class BookingCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the raw request body
            print("Raw request.body:", request.body.decode('utf-8'))
            data = json.loads(request.body)  # Parse JSON data
            print("Parsed JSON data:", data)

            # Extract nested data
            nested_data = data.get("data", {})
            print("Nested data:", nested_data)

            # Access and validate bus_id
            bus_id = nested_data.get("bus_id")
            if not bus_id or bus_id.strip() == "":
                print("Bus ID is missing or invalid.")
                return JsonResponse({"success": False, "message": "Bus ID is empty or invalid."})
            
            try:
                # Convert bus_id to integer
                bus_id = int(bus_id)
                print(f"Final bus_id: {bus_id} (Type: {type(bus_id)})")
            except ValueError as ve:
                print(f"Invalid bus_id: {bus_id}. Error: {ve}")
                return JsonResponse({"success": False, "message": "Invalid bus ID provided."})

            # Fetch the bus
            try:
                available_buses = Buses.objects.all().values_list("id", "name")
                print(f"Available buses in DB: {list(available_buses)}")
                bus = Buses.objects.get(id=bus_id)
                print(f"Successfully fetched bus: {bus}")
            except Buses.DoesNotExist:
                print(f"No bus found with ID: {bus_id}")
                return JsonResponse({"success": False, "message": f"No bus found with ID: {bus_id}"})

            # Validate travel_date
            travel_date = nested_data.get("travel_date")
            if not travel_date or travel_date.strip() == "":
                print("Travel date is missing or empty. Setting to today's date.")
                travel_date = datetime.now().date()
            else:
                try:
                    travel_date = datetime.strptime(travel_date, "%Y-%m-%d").date()
                    print(f"Validated travel_date: {travel_date}")
                except ValueError:
                    return JsonResponse({"success": False, "message": "Invalid travel date format. Expected YYYY-MM-DD."})

            # Primary passenger data
            primary_passenger_data = {
                "full_name": nested_data.get("primary_full_name"),
                "phone": nested_data.get("primary_phone"),
                "email": nested_data.get("primary_email"),
                "age": nested_data.get("primary_age"),
                "gender": nested_data.get("primary_gender"),
                "boarding_point": nested_data.get("primary_boarding_point"),
                "drop_off_point": nested_data.get("primary_dropoff_point"),
                "meal_preference": nested_data.get("primary_meal_preference"),
            }
            print("Primary passenger data:", primary_passenger_data)

            # Start creating the booking
            booking = Booking.objects.create(
                user=request.user,
                bus=bus,
                booking_date=datetime.now().date(),
                travel_date=travel_date,
                total_cost=Decimal(0),  # Placeholder for now
            )
            print(f"Booking created: {booking}")

            # Add primary passenger
            primary_passenger = PassengerDetail.objects.create(
                booking=booking,
                full_name=primary_passenger_data["full_name"],
                phone=primary_passenger_data["phone"],
                email=primary_passenger_data["email"],
                age=primary_passenger_data["age"],
                gender=primary_passenger_data["gender"],
                boarding_point=primary_passenger_data["boarding_point"],
                drop_off_point=primary_passenger_data["drop_off_point"],
                meal_preference=primary_passenger_data["meal_preference"],
                status="primary",
            )
            primary_meal_cost = primary_passenger.calculate_meal_cost()
            print(f"Primary passenger added: {primary_passenger}, Meal cost: {primary_meal_cost}")

            # Add co-passengers (if any)
            co_passengers = data.get("co_passengers", [])
            co_meal_cost = Decimal(0)
            for co_passenger_data in co_passengers:
                co_passenger = PassengerDetail.objects.create(
                    booking=booking,
                    full_name=co_passenger_data["full_name"],
                    age=co_passenger_data["age"],
                    gender=co_passenger_data["gender"],
                    boarding_point=co_passenger_data["boarding_point"],
                    drop_off_point=co_passenger_data["drop_off_point"],
                    meal_preference=co_passenger_data["meal_preference"],
                    status="co_passenger",
                )
                cost = co_passenger.calculate_meal_cost()
                co_meal_cost += Decimal(cost)
                print(f"Co-passenger added: {co_passenger}, Meal cost: {cost}")

            # Calculate total cost
            base_fare = Decimal(bus.base_fare)
            meal_cost = primary_meal_cost + co_meal_cost
            total_cost = base_fare + Decimal(meal_cost) + Decimal(base_fare + meal_cost) * Decimal(0.18)  # 18% tax
            booking.total_cost = total_cost
            booking.save()

            print(f"Booking completed. Total cost: {total_cost}")
            return JsonResponse({"success": True, "message": "Booking created successfully", "total_cost": float(total_cost)})

        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({"success": False, "message": str(e)})
        
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import HelpForm

def help_request(request):
    form = HelpForm()
    success = False

    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']

            # Log data for debugging
            print("Form data received:", name, phone, email, description)

            # Compose email
            subject = "Help Request from Busify User"
            message = f"""
            Name: {name}
            Phone: {phone}
            Email: {email}

            Issue Description:
            {description}
            """
            recipient_list = ['busifytravel@gmail.com']

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='noreply@busify.com',
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                success = True
            except Exception as e:
                print("Email sending error:", e)
                success = False

    return render(request, 'reservation/help.html', {'form': form, 'success': success})