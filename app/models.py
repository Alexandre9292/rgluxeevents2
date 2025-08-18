from django.db import models
from django.conf import settings

#Class qui gère les réservations des chauffeurs
class DriverBooking(models.Model):
    departure = models.CharField(max_length=500, blank=True, verbose_name='Départ')
    arrival = models.CharField(max_length=500, blank=True, verbose_name='Arrivée')
    date = models.DateField(verbose_name='Date')
    hour = models.TimeField(verbose_name='Heure')
    passengers = models.IntegerField(choices=[(i, str(i)) for i in range(1, 5)], default=1, verbose_name='Nombre de passagers')
    isReturn = models.BooleanField(default=False)
    price = models.FloatField(default=False, verbose_name='Prix')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acti = models.CharField(max_length=100, blank=True)

#Class qui gère les réservations des Transfert aeroport
class AeroportBooking(models.Model):
    departure = models.CharField(max_length=500, blank=True, verbose_name='Départ')
    date = models.DateField(verbose_name='Date')
    hour = models.TimeField(verbose_name='Heure')
    passengers = models.IntegerField(choices=[(i, str(i)) for i in range(1, 5)], default=1, verbose_name='Nombre de passagers')
    bagages = models.IntegerField(choices=[(i, str(i)) for i in range(1, 4)], default=1, verbose_name='Nombre de bagages')
    price = models.FloatField(default=False, verbose_name='Prix')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acti = models.CharField(max_length=100, blank=True)

#Class qui gère les réservations des Excursions
class TourismBooking(models.Model):
    excursion = models.CharField(max_length=500, blank=True, verbose_name='Départ')
    price = models.FloatField(default=False, verbose_name='Prix')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acti = models.CharField(max_length=100, blank=True)

#Class qui gère les réservations des Mariages
class WeddingBooking(models.Model):
    departure = models.CharField(max_length=500, blank=True, verbose_name='Arrivée')
    date = models.DateField(verbose_name='Date')
    hour = models.TimeField(verbose_name='Heure')
    price = models.FloatField(default=False, verbose_name='Prix')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acti = models.CharField(max_length=100, blank=True)

#Class qui gère les locations des utilitaires
class UtilityBooking(models.Model):
    start_date = models.DateField(verbose_name='Date')
    end_date = models.DateField(verbose_name='Date')
    price = models.FloatField(default=False, verbose_name='Prix')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acti = models.CharField(max_length=100, blank=True)

#Class qui gère les locations des Photomatons
class PhotomatonBooking(models.Model):
    date = models.DateField(verbose_name='Date')
    price = models.FloatField(default=False, verbose_name='Prix')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acti = models.CharField(max_length=100, blank=True)

# Nouveau modèle pour gérer les commandes
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'En attente de paiement'),
        ('paid', 'Payée'),
        ('failed', 'Échouée'),
        ('cancelled', 'Annulée'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, verbose_name='Numéro de commande')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Client')
    booking_type = models.CharField(max_length=50, verbose_name='Type de réservation')
    booking_data = models.JSONField(verbose_name='Données de réservation')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix total')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name='Statut')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créée le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modifiée le')
    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
    
    def __str__(self):
        return f"Commande {self.order_number} - {self.customer.email}"

# Modèle pour les informations de paiement
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('card', 'Carte bancaire'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='Commande')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Méthode de paiement')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID de transaction')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant')
    status = models.CharField(max_length=20, verbose_name='Statut du paiement')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    
    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
    
    def __str__(self):
        return f"Paiement {self.transaction_id} - {self.order.order_number}"
