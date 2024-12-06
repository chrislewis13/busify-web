from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PassengerDetail, BoardingPoint, DropOffPoint

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone', 'password1', 'password2']

# No need to redefine fields in CustomAuthenticationForm
class CustomAuthenticationForm(AuthenticationForm):
    pass
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone', 'password1', 'password2']

# No need to redefine fields in CustomAuthenticationForm
class CustomAuthenticationForm(AuthenticationForm):
    pass

#Pessenger Details form
class PrimaryPassengerForm(forms.ModelForm):
    class Meta:
        model = PassengerDetail
        fields = ['full_name', 'phone', 'email', 'age', 'gender', 'boarding_point', 'drop_off_point', 'meal_preference']

class CoPassengerForm(forms.ModelForm):
    class Meta:
        model = PassengerDetail
        fields = ['full_name', 'age', 'gender', 'boarding_point', 'drop_off_point', 'meal_preference']

        boarding_point = forms.ChoiceField(choices=[], required=True)  # Will be populated dynamically
        drop_off_point = forms.ChoiceField(choices=[], required=True)  # Will be populated dynamically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the drop-down choices dynamically
        boarding_points = BoardingPoint.objects.all()
        dropoff_points = DropOffPoint.objects.all()

        self.fields['boarding_point'].choices = [(bp.point, bp.point) for bp in boarding_points]
        self.fields['drop_off_point'].choices = [(dp.point, dp.point) for dp in dropoff_points]

class HelpForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border',
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border',
        })
    )
    issue = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border',
            'rows': 4,
        })
    )