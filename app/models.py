from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TransportBooking(models.Model):
    TRANSPORT_TYPE_CHOICES = [
        ('transport', 'Transport'),
        ('aeroport', 'Aéroport'),
    ]
    
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPE_CHOICES)
    departure = models.CharField(max_length=200)
    arrival = models.CharField(max_length=200)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    return_trip = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    passengers = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    luggage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=True, blank=True)
    service_type = models.CharField(max_length=50, null=True, blank=True)  # "venir me chercher" ou "me déposer"
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transport {self.transport_type} - {self.departure} vers {self.arrival}"

class PhotoboothBooking(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('journee', 'À la journée'),
        ('heure', 'À l\'heure'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    hours = models.IntegerField(validators=[MinValueValidator(2)], null=True, blank=True)
    days = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photobooth - {self.first_name} {self.last_name} - {self.event_date}"

class DroneBooking(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Drone - {self.first_name} {self.last_name} - {self.date}"
