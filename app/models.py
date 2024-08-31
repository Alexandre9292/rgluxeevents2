from django.db import models

#Class qui gère les réservations des chauffeurs
class DriverBooking(models.Model):
    departure = models.CharField(max_length=500, blank=True, verbose_name='Départ')
    arrival = models.CharField(max_length=500, blank=True, verbose_name='Arrivée')
    date = models.DateField(verbose_name='Date')
    hour = models.TimeField(verbose_name='Heure')
    isReturn = models.BooleanField(default=False)
    price = models.FloatField(default=False, verbose_name='Prix')

#Class qui gère les réservations des Transfert aeroport
class AeroportBooking(models.Model):
    departure = models.CharField(max_length=500, blank=True, verbose_name='Départ')
    date = models.DateField(verbose_name='Date')
    hour = models.TimeField(verbose_name='Heure')
    price = models.FloatField(default=False, verbose_name='Prix')

#Class qui gère les réservations des Excursions
class TourismBooking(models.Model):
    excursion = models.CharField(max_length=500, blank=True, verbose_name='Départ')
    price = models.FloatField(default=False, verbose_name='Prix')

#Class qui gère les réservations des Mariages
class WeddingBooking(models.Model):
    departure = models.CharField(max_length=500, blank=True, verbose_name='Arrivée')
    date = models.DateField(verbose_name='Date')
    hour = models.TimeField(verbose_name='Heure')
    price = models.FloatField(default=False, verbose_name='Prix')

#Class qui gère les locations des utilitaires
class UtilityBooking(models.Model):
    start_date = models.DateField(verbose_name='Date')
    end_date = models.DateField(verbose_name='Date')
    price = models.FloatField(default=False, verbose_name='Prix')

#Class qui gère les locations des Photomatons
class PhotomatonBooking(models.Model):
    date = models.DateField(verbose_name='Date')
    price = models.FloatField(default=False, verbose_name='Prix')
