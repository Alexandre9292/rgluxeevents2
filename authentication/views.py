from django.conf import settings
from django.contrib.auth import login, logout, authenticate  
from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
import calendar
from datetime import datetime

from app import models as model_app
from . import forms, models

from authentication.models import User
from django.http import JsonResponse

#Chargement de la page de mention légales
def mentions_legales(request):
    return render(request, 'authentication/mentions_legales.html')

def new_user_page(request):
    form = forms.NewUserForm()
    if request.method == 'POST':
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'CUSTOMER'
            user.save()
            return redirect('home')
    return render(request, 'authentication/new_user.html', context={'form': form})

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def customer_page(request):
    return render(request, 'authentication/view_customer.html')

@login_required
def admin_page_calendar(request, year=None, month=None, day=None):

    now = datetime.now()
    jourS = now.day
    moisS = now.month
    anneeS = now.year
    if year is None or month is None:
        # Récupérer l'année et le mois actuels
        annee = now.year
        mois = now.month
    else:
        if day is not None:
            jourS = int(day)
            moisS = int(month)
            anneeS = int(year)
        annee = int(year)
        mois = int(month)  

    # Générer le tableau des jours du mois actuel
    cal = calendar.Calendar(firstweekday=0)

    jours_string = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois_string = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    
    # Créer un tableau des jours pour le mois actuel
    jours_mois = list(cal.itermonthdays4(annee, mois))
    joursS_mois = list(cal.itermonthdays4(anneeS, moisS))

    # Filtrer pour ne garder que les jours appartenant au mois actuel
    jours_mois = [jour for jour in jours_mois if jour[1] == mois]
    joursS_mois = [jour for jour in joursS_mois if jour[1] == moisS]

    # jours_mois = [(année, mois, jour, jour_de_la_semaine)]
    jours_formattes = [{
        'jour': jour[2],
        'jour_semaine': calendar.day_name[jour[3]],  # Nom du jour de la semaine
        'jour_semaine_abbr': calendar.day_abbr[jour[3]]  # Abréviation (ex : "Lun" pour Lundi)
    } for jour in jours_mois]

    jourS_string = jours_string[joursS_mois[jourS-1][3]]
    
    # Récupérer le premier jour du mois pour savoir combien de "jours vides" ajouter au début
    premier_jour = jours_mois[0][3]  # jour[3] correspond au jour de la semaine (0 = lundi, 6 = dimanche)
    jours_vides = [{'jour': '', 'jour_semaine': '', 'jour_semaine_abbr': ''}] * premier_jour

    # Ajouter les jours vides au début de la liste
    jours_formattes = jours_vides + jours_formattes

    # Gestion des mois précédent et suivant
    mois_precedent = (mois - 1) if mois > 1 else 12
    annee_precedente = annee if mois > 1 else annee - 1
    mois_suivant = (mois + 1) if mois < 12 else 1
    annee_suivante = annee if mois < 12 else annee + 1

    #Chargement des activités
    date_selected = datetime.strptime(str(jourS) + '/' + str(moisS) + '/' + str(anneeS), '%d/%m/%Y').date()
    all_activity = []
    all_activity.extend(model_app.DriverBooking.objects.filter(
        date = date_selected))
    all_activity.extend(model_app.AeroportBooking.objects.filter(
        date = date_selected))
    all_activity.extend(model_app.TourismBooking.objects.all())
    all_activity.extend(model_app.WeddingBooking.objects.filter(
        date = date_selected))
    all_activity.extend(model_app.UtilityBooking.objects.filter(
        start_date = date_selected))
    all_activity.extend(model_app.PhotomatonBooking.objects.filter(
        date = date_selected))

    # Envoyer les données au template
    contexte = {
        'jours_formattes': jours_formattes,
        'jourS' : jourS,
        'jourS_string' : jourS_string,
        'moisS': moisS, 
        'moisS_string': mois_string[moisS-1], 
        'anneeS' : anneeS,
        'mois': mois, 
        'mois_string': mois_string[mois-1], 
        'annee': annee,        
        'mois_precedent': mois_precedent,
        'annee_precedente': annee_precedente,
        'mois_suivant': mois_suivant,
        'annee_suivante': annee_suivante,
        'all_activity': all_activity
    }

    return render(request, 'authentication/view_administration_calendar.html', contexte)

def get_activity_info(request, acti_id, acti_type):
    acti = ""
    data = {}

    if acti_type == 'DRIVER':
        acti = get_object_or_404(model_app.DriverBooking, id=acti_id)
        data['departure'] = acti.departure
        data['arrival'] = acti.arrival
        data['date'] = acti.date 
        data['hour'] = acti.hour 
    if acti_type == 'AEROPORT':
        acti = get_object_or_404(model_app.AeroportBooking, id=acti_id)
        data['departure'] = acti.departure
        data['date'] = acti.date
        data['hour'] = acti.hour 
    if acti_type == 'UTILITAIRE':
        acti = get_object_or_404(model_app.UtilityBooking, id=acti_id)
        data['date'] = acti.start_date + ' au ' + acti.end_date,
    if acti_type == 'PHOTOMATON':
        acti = get_object_or_404(model_app.PhotomatonBooking, id=acti_id)
        data['date'] = acti.date,
         
    
    data['acti'] = acti.acti
    data['price'] = acti.price
    data['name'] = acti.customer.first_name + ' ' + acti.customer.last_name
    data['phone'] = acti.customer.phone_number
    data['email'] = acti.customer.email
    
    return JsonResponse(data)

@login_required
def admin_page_users(request):
    users = models.User.objects.all()
    return render(request, 'authentication/view_administration_users.html', context={'list_users': users})

@login_required
def edit_user(request, user_id):
    edit_user = get_object_or_404(models.User, id=user_id)
    edit_form = forms.ChangeUserForm(instance=edit_user)
    if request.method == 'POST':
        edit_form = forms.ChangeUserForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
                
    context = {
        'edit_form': edit_form,
        'edit_user' : edit_user
    }
    return render(request, 'authentication/edit_user.html', context=context)

#Page404
def page_not_found_view(request, exception):
    return redirect ("home")

#Password reset
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Demande de réinitialisation du mot de passe"
					email_template_name = "authentication/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'rgluxeevents.fr',
					'site_name': 'rgluxeevents',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'alexandre.boucher92@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="authentication/password_reset.html", context={"password_reset_form":password_reset_form})
