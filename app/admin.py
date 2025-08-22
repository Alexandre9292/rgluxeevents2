from django.contrib import admin
from . import models

@admin.register(models.TransportBooking)
class TransportBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'transport_type', 'departure', 'arrival', 'departure_date', 'passengers', 'price', 'created_at']
    list_filter = ['transport_type', 'departure_date', 'return_trip', 'created_at']
    search_fields = ['departure', 'arrival']
    readonly_fields = ['created_at']
    date_hierarchy = 'departure_date'

@admin.register(models.PhotoboothBooking)
class PhotoboothBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'service_type', 'event_date', 'price', 'created_at']
    list_filter = ['service_type', 'event_date', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at']
    date_hierarchy = 'event_date'

@admin.register(models.DroneBooking)
class DroneBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'date', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
