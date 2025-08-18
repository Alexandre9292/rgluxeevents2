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

#Page d'accueil
def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'driver_form':
            form = forms.DriverBookingForm(request.POST)
            if form.is_valid():
                # Calculer le prix basé sur la distance et le type de trajet
                departure = form.cleaned_data['departure']
                arrival = form.cleaned_data['arrival']
                passengers = form.cleaned_data['passengers']
                aller_retour = form.cleaned_data['aller_retour']
                retour_date = form.cleaned_data.get('retour_date')
                retour_heure = form.cleaned_data.get('retour_heure')
                
                # Récupérer la distance depuis la session (calculée par JavaScript)
                distance_km = request.session.get('calculated_distance', 0)
                
                # Calcul du prix selon la grille tarifaire
                if distance_km <= 50:
                    price_per_km = 2.25
                elif distance_km <= 100:
                    price_per_km = 1.90
                else:
                    price_per_km = 1.50
                
                # Prix de base basé sur la distance
                base_price = distance_km * price_per_km # 15€ par passager supplémentaire
                
                # Ajuster le prix pour aller-retour
                if aller_retour:
                    base_price *= 1.8
                
                # Stocker les données de réservation en session
                request.session['booking_data'] = {
                    'type': 'driver',
                    'departure': departure,
                    'arrival': arrival,
                    'passengers': passengers,
                    'distance_km': distance_km,
                    'price_per_km': price_per_km,
                    'date': form.cleaned_data['date'].strftime('%d/%m/%Y'),
                    'hour': form.cleaned_data['hour'].strftime('%H:%M'),
                    'aller_retour': aller_retour,
                    'retour_date': retour_date.strftime('%d/%m/%Y') if retour_date else None,
                    'retour_heure': retour_heure.strftime('%H:%M') if retour_heure else None,
                    'price': round(base_price, 2)
                }
                return redirect('booking_summary')
                
        elif form_type == 'airport_form':
            form = forms.AeroportBookingForm(request.POST)
            if form.is_valid():
                # Calculer le prix pour le transfert aéroport
                departure = form.cleaned_data['departure']
                passengers = form.cleaned_data['passengers']
                bagages = form.cleaned_data['bagages']
                
                # Prix de base pour transfert aéroport
                base_price = 80.0
                # Ajuster le prix selon le nombre de passagers et bagages
                if passengers > 1:
                    base_price += (passengers - 1) * 20.0  # 20€ par passager supplémentaire
                if bagages > 1:
                    base_price += (bagages - 1) * 10.0  # 10€ par bagage supplémentaire
                
                # Stocker les données de réservation en session
                request.session['booking_data'] = {
                    'type': 'airport',
                    'departure': departure,
                    'passengers': passengers,
                    'bagages': bagages,
                    'date': form.cleaned_data['date'].strftime('%d/%m/%Y'),
                    'hour': form.cleaned_data['hour'].strftime('%H:%M'),
                    'price': base_price
                }
                return redirect('booking_summary')
            
        return redirect('home') 
      
    driverForm = forms.DriverBookingForm()
    airportForm = forms.AeroportBookingForm()
    return render(request, 'app/home.html', {'driverForm':driverForm, 'airportForm': airportForm})

# Page de récapitulatif de la réservation
def booking_summary(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        return redirect('home')
    
    context = {
        'booking_data': booking_data
    }
    return render(request, 'app/booking_summary.html', context)

# Page de paiement
def payment(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        return redirect('home')
    
    if request.method == 'POST':
        form = forms.PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            
            # Créer la commande
            order_number = f"RG{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
            
            order = models.Order.objects.create(
                order_number=order_number,
                customer=request.user,
                booking_type=booking_data['type'],
                booking_data=booking_data,
                total_price=booking_data['price'],
                status='pending'
            )
            
            # Créer le paiement
            payment = models.Payment.objects.create(
                order=order,
                payment_method=payment_method,
                amount=booking_data['price'],
                status='pending'
            )
            
            if payment_method == 'paypal':
                # Rediriger vers PayPal (intégration à implémenter)
                return redirect('payment_paypal', order_id=order.id)
            else:
                # Traitement de la carte bancaire (simulation)
                # En production, intégrer avec Stripe ou autre processeur de paiement
                if process_card_payment(form.cleaned_data, order):
                    order.status = 'paid'
                    order.save()
                    payment.status = 'completed'
                    payment.save()
                    
                    # Envoyer les emails
                    send_booking_confirmation_emails(order)
                    
                    # Nettoyer la session
                    del request.session['booking_data']
                    
                    return redirect('payment_success', order_id=order.id)
                else:
                    order.status = 'failed'
                    order.save()
                    payment.status = 'failed'
                    payment.save()
                    
                    return redirect('payment_failed', order_id=order.id)
    else:
        form = forms.PaymentForm()
    
    context = {
        'form': form,
        'booking_data': booking_data
    }
    return render(request, 'app/payment.html', context)

# Page de succès du paiement
def payment_success(request, order_id):
    order = get_object_or_404(models.Order, id=order_id, customer=request.user)
    context = {
        'order': order
    }
    return render(request, 'app/payment_success.html', context)

# Page d'échec du paiement
def payment_failed(request, order_id):
    order = get_object_or_404(models.Order, id=order_id, customer=request.user)
    context = {
        'order': order
    }
    return render(request, 'app/payment_failed.html', context)

# Fonction pour traiter le paiement par carte (simulation)
def process_card_payment(card_data, order):
    # Simulation de traitement de paiement
    # En production, intégrer avec un processeur de paiement réel
    import random
    return random.choice([True, False])  # 50% de chance de succès pour la démo

# Vue pour stocker la distance calculée en session
@csrf_exempt
def store_distance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            distance = data.get('distance', 0)
            request.session['calculated_distance'] = distance
            return JsonResponse({'status': 'success', 'distance': distance})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

# Vue pour stocker les données de réservation complètes en session
@csrf_exempt
def store_booking_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Stocker toutes les données de réservation en session
            request.session['booking_data'] = {
                'type': data.get('type'),
                'departure': data.get('departure'),
                'arrival': data.get('arrival'),
                'passengers': data.get('passengers'),
                'distance_km': data.get('distance_km'),
                'price_per_km': data.get('price_per_km'),
                'date': data.get('date'),
                'hour': data.get('hour'),
                'aller_retour': data.get('aller_retour'),
                'price': data.get('price')
            }
            
            return JsonResponse({'status': 'success', 'message': 'Données sauvegardées'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

# Fonction pour envoyer les emails de confirmation
def send_booking_confirmation_emails(order):
    try:
        # Email au client
        customer_subject = f"Confirmation de votre réservation - {order.order_number}"
        customer_message = f"""
        Bonjour {order.customer.first_name or order.customer.username},
        
        Votre réservation a été confirmée !
        
        Numéro de commande : {order.order_number}
        Type : {order.get_booking_type_display()}
        Prix total : {order.total_price}€
        
        Merci de votre confiance !
        RG Luxe Events
        """
        
        send_mail(
            customer_subject,
            customer_message,
            'noreply@rgluxeevents.com',
            [order.customer.email],
            fail_silently=False
        )
        
        # Email au responsable
        admin_subject = f"Nouvelle réservation confirmée - {order.order_number}"
        admin_message = f"""
        Nouvelle réservation confirmée :
        
        Numéro de commande : {order.order_number}
        Client : {order.customer.email}
        Type : {order.get_booking_type_display()}
        Prix total : {order.total_price}€
        Date : {order.created_at.strftime('%d/%m/%Y %H:%M')}
        """
        
        send_mail(
            admin_subject,
            admin_message,
            'noreply@rgluxeevents.com',
            ['alexandre.boucher92@gmail.com'],  # Email du responsable
            fail_silently=False
        )
        
    except Exception as e:
        print(f"Erreur lors de l'envoi des emails : {e}")

#Page des services
def services(request):
    return render(request, 'app/services.html')

#Page du service aéroport
def aeroport(request):
    return render(request, 'app/aeroport.html')

#Page du service transport
def transport(request):
    return render(request, 'app/transport.html')

#Page du service mariage
def mariage(request):
    return render(request, 'app/mariage.html')

#Page du service tourisme
def tourisme(request):
    return render(request, 'app/tourisme.html')

#Page utilitaire
def utilitaire(request):
    if request.method == 'POST':
        form = forms.UtilityBookingForm(request.POST)
        if form.is_valid():
            resa = form.save(commit=False)
            resa.customer = request.user
            resa.acti = 'UTILITAIRE'
            resa.save()
            return redirect('home')
            """ subject = "RGLuxeEnvents - Réservation" 
            body = {
            'name': form.cleaned_data['name'], 
            'email': form.cleaned_data['email_address'], 
            'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, form.cleaned_data['email_address'], ['alexandre.boucher92@gmail.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.') """
      
    form = forms.UtilityBookingForm()
    return render(request, 'app/utilitaire.html', {'form':form})

#Page photomaton
def photomaton(request):
    if request.method == 'POST':
        form = forms.PhotomatonBookingForm(request.POST)
        if form.is_valid():
            resa = form.save(commit=False)
            resa.customer = request.user
            resa.acti = 'PHOTOMATON'
            resa.save()

            return redirect('home')
            """ subject = "RGLuxeEnvents - Réservation" 
            body = {
            'name': form.cleaned_data['name'], 
            'email': form.cleaned_data['email_address'], 
            'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, form.cleaned_data['email_address'], ['alexandre.boucher92@gmail.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.') """
      
    form = forms.PhotomatonBookingForm()
    return render(request, 'app/photomaton.html', {'form':form})

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

