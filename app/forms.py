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
		widgets = {
			'date': forms.TextInput(attrs={
                'class': 'flatpickr-date',  # Classe spécifique pour la date
                'placeholder': 'dd/mm/yyyy',
            }),
			'hour': forms.TimeInput(attrs={
                'type': 'time',  # Type natif HTML5 pour le temps
                'class': 'time-input',  # Classe personnalisée si nécessaire
                'placeholder': 'HH:MM',
            }),
        }

class AeroportBookingForm(forms.ModelForm):
	class Meta:
		model = models.AeroportBooking
		fields = ['departure', 'date', 'hour', 'price']
		widgets = {
            'date': forms.TextInput(attrs={
                'class': 'flatpickr-date',  # Classe CSS spécifique pour Flatpickr
                'placeholder': 'dd/mm/yyyy',  # Placeholder pour le champ
            }),
			'hour': forms.TimeInput(attrs={
                'type': 'time',  # Type natif HTML5 pour le temps
                'class': 'time-input',  # Classe personnalisée si nécessaire
                'placeholder': 'HH:MM',
            }),
        }

class TourismBookingForm(forms.ModelForm):
	class Meta:
		model = models.TourismBooking
		fields = ['excursion', 'price']

class WeddingBookingForm(forms.ModelForm):
	class Meta:
		model = models.WeddingBooking
		fields = ['departure', 'date', 'hour', 'price']
		widgets = {
            'date': forms.TextInput(attrs={
                'class': 'flatpickr-date',  # Classe CSS spécifique pour Flatpickr
                'placeholder': 'dd/mm/yyyy',  # Placeholder pour le champ
            }),
			'hour': forms.TimeInput(attrs={
                'type': 'time',  # Type natif HTML5 pour le temps
                'class': 'time-input',  # Classe personnalisée si nécessaire
                'placeholder': 'HH:MM',
            }),
        }

class UtilityBookingForm(forms.ModelForm):
	class Meta:
		model = models.UtilityBooking
		fields = ['start_date', 'end_date', 'price']
		widgets = {
            'start_date': forms.TextInput(attrs={
                'class': 'flatpickr-date',  # Classe CSS spécifique pour Flatpickr
                'placeholder': 'dd/mm/yyyy',  # Placeholder pour le champ
            }),
            'end_date': forms.TextInput(attrs={
                'class': 'flatpickr-date',  # Classe CSS spécifique pour Flatpickr
                'placeholder': 'dd/mm/yyyy',  # Placeholder pour le champ
            }),
        }

class PhotomatonBookingForm(forms.ModelForm):
	class Meta:
		model = models.PhotomatonBooking
		fields = ['date', 'price']
		widgets = {
            'date': forms.TextInput(attrs={
                'class': 'flatpickr-date',  # Classe CSS spécifique pour Flatpickr
                'placeholder': 'dd/mm/yyyy',  # Placeholder pour le champ
            }),
        }