from django import forms
from .models import Booking, BusJourney, Bus
from datetime import datetime


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger_name', 'passenger_email', 'passenger_phone', 'seats']
        widgets = {
            'passenger_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'passenger_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'passenger_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Number of Seats'
            }),
        }


class ScheduleSearchForm(forms.Form):
    origin = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'From (City)',
            'autocomplete': 'off'
        })
    )
    destination = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'To (City)',
            'autocomplete': 'off'
        })
    )
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': datetime.now().date()
        })
    )
    bus_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + list(Bus.BUS_TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
