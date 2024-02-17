# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *
from django.forms import DateInput
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'password1', 'password2']

class StaffRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'password1', 'password2', 'user_type']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_out_date <= check_in_date:
                raise forms.ValidationError("Check-out date must be after check-in date.")

            # Add additional validation logic as needed

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set a minimum date for check_in_date field
        self.fields['check_in_date'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
        self.fields['check_out_date'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')

class RoomRegistrationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'normal_price', 'season_price', 'available_count', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        # Your custom validation logic for the image field can be added here
        return image