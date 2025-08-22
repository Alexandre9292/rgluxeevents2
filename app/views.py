from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
from . import forms, models
import math

#Page d'accueil
def home(request):
    return render(request, 'app/home.html')

#Page about
def about(request):
    return render(request, 'app/about.html')

#Page de contact
def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = "RGLuxeEnvents - contact" 
            body = {
            'name': form.cleaned_data['name'], 
            'email': form.cleaned_data['email_address'], 
            'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, form.cleaned_data['email_address'], ['alexandre.boucher92@gmail.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("home")
      
    form = forms.ContactForm()
    return render(request, "app/contact.html", {'form':form})

#Page transport
def transport(request):
    transport_form = forms.TransportForm()
    aeroport_form = forms.AeroportForm()
    
    if request.method == 'POST':
        if 'transport_submit' in request.POST:
            transport_form = forms.TransportForm(request.POST)
            if transport_form.is_valid():
                # Récupérer les coordonnées GPS
                departure_lat = request.POST.get('departure_lat')
                departure_lng = request.POST.get('departure_lng')
                arrival_lat = request.POST.get('arrival_lat')
                arrival_lng = request.POST.get('arrival_lng')
                
                # Calculer la distance en utilisant la formule de Haversine
                if departure_lat and departure_lng and arrival_lat and arrival_lng:
                    distance = calculate_distance(
                        float(departure_lat), float(departure_lng),
                        float(arrival_lat), float(arrival_lng)
                    )
                else:
                    # Fallback si pas de coordonnées GPS
                    distance = 50  # km par défaut
                
                # Calculer le prix selon la grille tarifaire
                if distance <= 50:
                    price_per_km = 2.25
                elif distance <= 100:
                    price_per_km = 1.90
                else:
                    price_per_km = 1.50
                
                price = distance * price_per_km
                
                # Sauvegarder la réservation
                booking = models.TransportBooking.objects.create(
                    transport_type='transport',
                    departure=transport_form.cleaned_data['departure'],
                    arrival=transport_form.cleaned_data['arrival'],
                    departure_date=transport_form.cleaned_data['departure_date'],
                    departure_time=transport_form.cleaned_data['departure_time'],
                    return_trip=transport_form.cleaned_data['return_trip'],
                    return_date=transport_form.cleaned_data['return_date'],
                    return_time=transport_form.cleaned_data['return_time'],
                    passengers=transport_form.cleaned_data['passengers'],
                    price=price
                )
                
                return redirect('transport_summary', booking_id=booking.id)
                
        elif 'aeroport_submit' in request.POST:
            aeroport_form = forms.AeroportForm(request.POST)
            if aeroport_form.is_valid():
                # Récupérer les coordonnées GPS
                departure_lat = request.POST.get('departure_lat')
                departure_lng = request.POST.get('departure_lng')
                arrival_lat = request.POST.get('arrival_lat')
                arrival_lng = request.POST.get('arrival_lng')
                aeroport_address_lat = request.POST.get('aeroport_address_lat')
                aeroport_address_lng = request.POST.get('aeroport_address_lng')
                
                # Calculer la distance selon le type de service
                service_type = aeroport_form.cleaned_data['service_type']
                distance = 0
                
                if service_type == 'venir':
                    # Venir me chercher : de l'aéroport vers l'adresse client
                    if aeroport_address_lat and aeroport_address_lng:
                        distance = calculate_distance(
                            -20.890089, 55.516448,  # Coordonnées aéroport
                            float(aeroport_address_lat), float(aeroport_address_lng)
                        )
                    departure = "Aéroport Roland Garros, La Réunion"
                    arrival = request.POST.get('aeroport_address', 'Adresse client')
                elif service_type == 'deposer':
                    # Me déposer : de l'adresse client vers l'aéroport
                    if aeroport_address_lat and aeroport_address_lng:
                        distance = calculate_distance(
                            float(aeroport_address_lat), float(aeroport_address_lng),
                            -20.890089, 55.516448  # Coordonnées aéroport
                        )
                    departure = request.POST.get('aeroport_address', 'Adresse client')
                    arrival = "Aéroport Roland Garros, La Réunion"
                
                # Fallback si pas de coordonnées GPS
                if distance == 0:
                    distance = 30  # km par défaut
                
                # Calculer le prix selon la grille tarifaire
                if distance <= 30:
                    price_per_km = 2.00
                else:
                    price_per_km = 1.50
                
                price = distance * price_per_km
                
                # Sauvegarder la réservation
                booking = models.TransportBooking.objects.create(
                    transport_type='aeroport',
                    departure=departure,
                    arrival=arrival,
                    departure_date=aeroport_form.cleaned_data['departure_date'],
                    departure_time=aeroport_form.cleaned_data['departure_time'],
                    passengers=aeroport_form.cleaned_data['passengers'],
                    luggage=aeroport_form.cleaned_data['luggage'],
                    service_type=service_type,
                    price=price
                )
                
                return redirect('transport_summary', booking_id=booking.id)
    
    return render(request, 'app/transport.html', {
        'transport_form': transport_form,
        'aeroport_form': aeroport_form
    })

# Fonction pour calculer la distance entre deux points GPS (formule de Haversine)
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calcule la distance entre deux points GPS en utilisant la formule de Haversine
    Retourne la distance en kilomètres
    """
    # Rayon de la Terre en kilomètres
    R = 6371
    
    # Conversion des degrés en radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Différences des coordonnées
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Formule de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Distance en kilomètres
    distance = R * c
    
    return distance

#Page récapitulative transport
def transport_summary(request, booking_id):
    booking = get_object_or_404(models.TransportBooking, id=booking_id)
    return render(request, 'app/transport_summary.html', {'booking': booking})

#Page photobooth
def photobooth(request):
    if request.method == 'POST':
        form = forms.PhotoboothForm(request.POST)
        if form.is_valid():
            # Calculer le prix
            service_type = form.cleaned_data['service_type']
            if service_type == 'journee':
                days = form.cleaned_data['days']
                price = days * 400
            else:
                hours = form.cleaned_data['hours']
                price = hours * 85
            
            # Sauvegarder la réservation
            booking = models.PhotoboothBooking.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                service_type=service_type,
                hours=form.cleaned_data['hours'],
                days=form.cleaned_data['days'],
                event_date=form.cleaned_data['event_date'],
                event_time=form.cleaned_data['event_time'],
                location=form.cleaned_data['location'],
                event_type=form.cleaned_data['event_type'],
                price=price
            )
            
            # Envoyer l'email
            subject = "RG Luxe Events - Demande Photobooth"
            message = f"""
            Merci pour votre demande, nous vous contacterons sous 24h pour confirmer votre réservation.
            
            Détails de votre demande :
            Nom : {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}
            Adresse : {form.cleaned_data['address']}
            Email : {form.cleaned_data['email']}
            Téléphone : {form.cleaned_data['phone']}
            Type de service : {form.cleaned_data['service_type']}
            Date : {form.cleaned_data['event_date']}
            Heure : {form.cleaned_data['event_time']}
            Lieu : {form.cleaned_data['location']}
            Type d'événement : {form.cleaned_data['event_type']}
            Prix : {price}€
            """
            
            try:
                send_mail(
                    subject, 
                    message, 
                    'rg.luxeevents@gmail.com', 
                    [form.cleaned_data['email'], 'rg.luxeevents@gmail.com']
                )
                messages.success(request, 'Votre demande a été envoyée avec succès !')
            except BadHeaderError:
                messages.error(request, 'Erreur lors de l\'envoi de l\'email.')
            
            return redirect('photobooth')
    else:
        form = forms.PhotoboothForm()
    
    return render(request, 'app/photobooth.html', {'form': form})

#Page drone
def drone(request):
    if request.method == 'POST':
        form = forms.DroneForm(request.POST)
        if form.is_valid():
            # Sauvegarder la réservation
            booking = models.DroneBooking.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                date=form.cleaned_data['date'],
                description=form.cleaned_data['description']
            )
            
            # Envoyer l'email
            subject = "RG Luxe Events - Demande Drone"
            message = f"""
            Merci pour votre demande, nous vous contacterons sous 24h pour confirmer votre réservation.
            
            Détails de votre demande :
            Nom : {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}
            Email : {form.cleaned_data['email']}
            Téléphone : {form.cleaned_data['phone']}
            Date souhaitée : {form.cleaned_data['date']}
            Description : {form.cleaned_data['description']}
            """
            
            try:
                send_mail(
                    subject, 
                    message, 
                    'rg.luxeevents@gmail.com', 
                    [form.cleaned_data['email'], 'rg.luxeevents@gmail.com']
                )
                messages.success(request, 'Votre demande a été envoyée avec succès !')
            except BadHeaderError:
                messages.error(request, 'Erreur lors de l\'envoi de l\'email.')
            
            return redirect('drone')
    else:
        form = forms.DroneForm()
    
    return render(request, 'app/drone.html', {'form': form})

