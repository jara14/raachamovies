from django import forms
from .models import Booking, UserProfile
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'tickets']

    def __init__(self, *args, **kwargs):
        # Get the user from kwargs and remove it to avoid passing it twice
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If user is provided, pre-fill name and email fields
        if user:
            self.fields['name'].initial = user.first_name + ' ' + user.last_name if user.first_name else user.username
            self.fields['email'].initial = user.email

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    # Inherits everything from PasswordChangeForm
    pass