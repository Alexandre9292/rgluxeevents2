from django import forms
from . import models

class ContactForm(forms.Form):
	name = forms.CharField(max_length = 50, label='Nom')
	email_address = forms.EmailField(max_length = 150, label='Adresse mail')
	message = forms.CharField(widget = forms.Textarea, max_length = 2000, label='Message')

class DriverBookingForm(forms.ModelForm):
	class Meta:
		model = models.DriverBooking
		fields = ['departure', 'arrival', 'date', 'hour', 'isReturn', 'price']

class AeroportBookingForm(forms.ModelForm):
	class Meta:
		model = models.AeroportBooking
		fields = ['departure', 'date', 'hour', 'price']

class TourismBookingForm(forms.ModelForm):
	class Meta:
		model = models.TourismBooking
		fields = ['excursion', 'price']

class WeddingBookingForm(forms.ModelForm):
	class Meta:
		model = models.WeddingBooking
		fields = ['departure', 'date', 'hour', 'price']

class UtilityBookingForm(forms.ModelForm):
	class Meta:
		model = models.UtilityBooking
		fields = ['start_date', 'end_date', 'price']

class PhotomatonBookingForm(forms.ModelForm):
	class Meta:
		model = models.PhotomatonBooking
		fields = ['date', 'price']