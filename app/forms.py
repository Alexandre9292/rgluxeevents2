from django import forms
from . import models

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 50, label='Nom')
    email_address = forms.EmailField(max_length = 150, label='Adresse mail')
    message = forms.CharField(widget = forms.Textarea, max_length = 2000, label='Message')

class DriverBookingForm(forms.ModelForm):
    passengers = forms.ChoiceField(
        choices=[(i, f"{i}") for i in range(1, 5)],
        label='Nombre de passagers',
        widget=forms.Select(attrs={'class': 'passengers-select'})
    )
    
    aller_retour = forms.BooleanField(
        required=False,
        label='Aller-retour',
        widget=forms.CheckboxInput(attrs={'class': 'aller-retour-checkbox'})
    )
    
    retour_date = forms.DateField(
        required=False,
        label='Date de retour',
        widget=forms.TextInput(attrs={
            'class': 'flatpickr-date retour-field',
            'placeholder': 'dd/mm/yyyy',
        })
    )
    
    retour_heure = forms.TimeField(
        required=False,
        label='Heure de retour',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'time-input retour-field',
            'placeholder': 'HH:MM',
        })
    )
    
    class Meta:
        model = models.DriverBooking
        fields = ['departure', 'arrival', 'date', 'hour']
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
    
    def clean(self):
        cleaned_data = super().clean()
        aller_retour = cleaned_data.get('aller_retour')
        retour_date = cleaned_data.get('retour_date')
        retour_heure = cleaned_data.get('retour_heure')
        
        # Si aller-retour est coché, les champs de retour sont obligatoires
        if aller_retour:
            if not retour_date:
                raise forms.ValidationError("La date de retour est obligatoire pour un trajet aller-retour.")
            if not retour_heure:
                raise forms.ValidationError("L'heure de retour est obligatoire pour un trajet aller-retour.")
        
        return cleaned_data

class AeroportBookingForm(forms.ModelForm):
    passengers = forms.ChoiceField(
        choices=[(i, f"{i}") for i in range(1, 5)],
        label='Nombre de passagers',
        widget=forms.Select(attrs={'class': 'passengers-select'})
    )
    
    bagages = forms.ChoiceField(
        choices=[(i, f"{i}") for i in range(1, 4)],
        label='Nombre de bagages',
        widget=forms.Select(attrs={'class': 'bagages-select'})
    )
    
    class Meta:
        model = models.AeroportBooking
        fields = ['departure', 'date', 'hour']
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
        fields = ['excursion']

class WeddingBookingForm(forms.ModelForm):
    class Meta:
        model = models.WeddingBooking
        fields = ['departure', 'date', 'hour']
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
        fields = ['start_date', 'end_date']
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
        fields = ['date']
        widgets = {
            'date': forms.TextInput(attrs={
                'class': 'flatpickr-date',  # Classe CSS spécifique pour Flatpickr
                'placeholder': 'dd/mm/yyyy',  # Placeholder pour le champ
            }),
        }

# Nouveaux formulaires pour le paiement
class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('card', 'Carte bancaire'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        label='Méthode de paiement'
    )
    
    # Champs pour carte bancaire
    card_number = forms.CharField(
        max_length=19,
        required=False,
        label='Numéro de carte',
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'})
    )
    
    card_holder = forms.CharField(
        max_length=100,
        required=False,
        label='Nom du titulaire',
        widget=forms.TextInput(attrs={'placeholder': 'NOM Prénom'})
    )
    
    expiry_month = forms.ChoiceField(
        choices=[(str(i), str(i).zfill(2)) for i in range(1, 13)],
        required=False,
        label='Mois d\'expiration'
    )
    
    expiry_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(2024, 2035)],
        required=False,
        label='Année d\'expiration'
    )
    
    cvv = forms.CharField(
        max_length=4,
        required=False,
        label='Code de sécurité',
        widget=forms.TextInput(attrs={'placeholder': '123'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'card':
            # Validation des champs de carte bancaire
            required_fields = ['card_number', 'card_holder', 'expiry_month', 'expiry_year', 'cvv']
            for field in required_fields:
                if not cleaned_data.get(field):
                    raise forms.ValidationError(f"Le champ {field} est requis pour le paiement par carte bancaire.")
            
            # Validation du numéro de carte (format basique)
            card_number = cleaned_data.get('card_number', '').replace(' ', '')
            if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
                raise forms.ValidationError("Le numéro de carte n'est pas valide.")
            
            # Validation du CVV
            cvv = cleaned_data.get('cvv', '')
            if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
                raise forms.ValidationError("Le code de sécurité n'est pas valide.")
        
        return cleaned_data