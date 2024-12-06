from django.urls import path
from . import views
from .views import BookingCreateView

urlpatterns = [
    path("", views.home, name="home"),
    path("help", views.help, name="help"),
    path("account", views.account, name="account"),
    path('search/', views.search_buses, name='search_buses'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('seat-selection/<int:bus_id>/', views.seat_selection, name='seat_selection'),
    path('login/', views.login_view, name='login'),
    path('hold-seat/', views.hold_seat, name='hold_seat'),
    path('passenger-form/<int:bus_id>/', views.passenger_form, name='passenger_form'),
    path('create-booking/', BookingCreateView.as_view(), name='create_booking'),
]
