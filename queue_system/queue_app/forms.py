from django import forms
from .models import Booking, Rating


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['slot']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
