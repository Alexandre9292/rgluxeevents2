from django import forms
from . import models

class ContactForm(forms.Form):
	name = forms.CharField(max_length = 50, label='Nom')
	email_address = forms.EmailField(max_length = 150, label='Adresse mail')
	message = forms.CharField(widget = forms.Textarea, max_length = 2000, label='Message')

class BookingForm(forms.ModelForm):
	class Meta:
		model = models.Booking
		fields = ['departure', 'arrival', 'date', 'hour']