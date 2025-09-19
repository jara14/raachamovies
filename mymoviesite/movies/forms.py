from django import forms
from .models import Booking, UserProfile
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email','phone','tickets']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tickets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            # 'seats': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            # Prepopulate with user data
            self.fields['name'].initial = user.get_full_name() or user.username
            self.fields['email'].initial = user.email
            
            # Make fields readonly for logged-in users
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['style'] = 'background-color: #f8f9fa;'
            self.fields['email'].widget.attrs['style'] = 'background-color: #f8f9fa;'
            
            # Try to get additional info from UserProfile
            try:
                profile = user.userprofile
                if profile.full_name:
                    self.fields['name'].initial = profile.full_name
                if profile.phone:
                    self.fields['phone'].initial = profile.phone
                    self.fields['phone'].widget.attrs['readonly'] = True
                    self.fields['phone'].widget.attrs['style'] = 'background-color: #f8f9fa;'
            except:
                pass

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