from django.db import models

#Class qui gère les réservations
class Booking(models.Model):
    departure = models.CharField(max_length=500, blank=True, verbose_name='Départ')
    arrival = models.CharField(max_length=500, blank=True, verbose_name='Arrivée')
    date = models.DateField(verbose_name='Date')
    hour = models.TimeField(verbose_name='Heure')
    isReturn = models.BooleanField(default=False)
