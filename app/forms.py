from django import forms
from . import models

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 50, label='Nom')
    email_address = forms.EmailField(max_length = 150, label='Adresse mail')
    message = forms.CharField(widget = forms.Textarea, max_length = 2000, label='Message')

class TransportForm(forms.Form):
    departure = forms.CharField(max_length=200, label='Lieu de départ')
    arrival = forms.CharField(max_length=200, label='Lieu d\'arrivée')
    departure_date = forms.DateField(label='Date de départ', widget=forms.DateInput(attrs={'type': 'date'}))
    departure_time = forms.TimeField(label='Heure de départ', widget=forms.TimeInput(attrs={'type': 'time'}))
    return_trip = forms.BooleanField(label='Aller-retour', required=False)
    return_date = forms.DateField(label='Date de retour', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    return_time = forms.TimeField(label='Heure de retour', widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    passengers = forms.IntegerField(label='Nombre de passagers', min_value=1, max_value=4, widget=forms.NumberInput(attrs={'min': 1, 'max': 4}))

class AeroportForm(forms.Form):
    SERVICE_CHOICES = [
        ('venir', 'Venir me chercher'),
        ('deposer', 'Me déposer'),
    ]
    service_type = forms.ChoiceField(choices=SERVICE_CHOICES, label='Type de service')
    departure_date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    departure_time = forms.TimeField(label='Heure', widget=forms.TimeInput(attrs={'type': 'time'}))
    passengers = forms.IntegerField(label='Nombre de passagers', min_value=1, max_value=4, widget=forms.NumberInput(attrs={'min': 1, 'max': 4}))
    luggage = forms.IntegerField(label='Nombre de bagages', min_value=1, max_value=3, widget=forms.NumberInput(attrs={'min': 1, 'max': 3}))

class PhotoboothForm(forms.Form):
    SERVICE_TYPE_CHOICES = [
        ('journee', 'À la journée'),
        ('heure', 'À l\'heure'),
    ]
    
    first_name = forms.CharField(max_length=100, label='Prénom')
    last_name = forms.CharField(max_length=100, label='Nom')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Adresse')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Téléphone')
    service_type = forms.ChoiceField(choices=SERVICE_TYPE_CHOICES, label='Type de service')
    hours = forms.IntegerField(label='Nombre d\'heures', min_value=2, required=False, widget=forms.NumberInput(attrs={'min': 2}))
    days = forms.IntegerField(label='Nombre de jours', min_value=1, required=False, widget=forms.NumberInput(attrs={'min': 1}))
    event_date = forms.DateField(label='Date de l\'événement', widget=forms.DateInput(attrs={'type': 'date'}))
    event_time = forms.TimeField(label='Heure de l\'événement', widget=forms.TimeInput(attrs={'type': 'time'}))
    location = forms.CharField(max_length=200, label='Lieu')
    event_type = forms.CharField(max_length=100, label='Type d\'événement')

class DroneForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Prénom')
    last_name = forms.CharField(max_length=100, label='Nom')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Téléphone')
    date = forms.DateField(label='Date souhaitée', widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Description de votre demande')

