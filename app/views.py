from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from . import forms, models

#Page d'accueil
def home(request):
    if request.method == 'POST':
        form = forms.DriverBookingForm(request.POST)
        if form.is_valid():
            resa = form.save(commit=False)
            resa.customer = request.user
            resa.save()
            return redirect('home')
        else :            
            form = forms.AeroportBookingForm(request.POST)
            if form.is_valid():
                resa = form.save(commit=False)
                resa.customer = request.user
                resa.save()
                return redirect('home')
      
    driverForm = forms.DriverBookingForm()
    airportForm = forms.AeroportBookingForm()
    return render(request, 'app/home.html', {'driverForm':driverForm, 'airportForm': airportForm})

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

