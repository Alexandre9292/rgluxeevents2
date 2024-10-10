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

from . import forms, models

from authentication.models import User

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
                print(message)
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
def admin_page_calendar(request):
    # Récupérer l'année et le mois actuels
    now = datetime.now()
    annee = now.year
    mois = now.month

    # Générer le tableau des jours du mois actuel
    cal = calendar.Calendar(firstweekday=0)
    
    # Créer un tableau des jours pour le mois actuel
    jours_mois = list(cal.itermonthdays4(annee, mois))

    # Filtrer pour ne garder que les jours appartenant au mois actuel
    jours_mois = [jour for jour in jours_mois if jour[1] == mois]

    # jours_mois = [(année, mois, jour, jour_de_la_semaine)]
    jours_formattes = [{
        'jour': jour[2],
        'jour_semaine': calendar.day_name[jour[3]],  # Nom du jour de la semaine
        'jour_semaine_abbr': calendar.day_abbr[jour[3]]  # Abréviation (ex : "Lun" pour Lundi)
    } for jour in jours_mois]

    # Récupérer le premier jour du mois pour savoir combien de "jours vides" ajouter au début
    premier_jour = jours_mois[0][3]  # jour[3] correspond au jour de la semaine (0 = lundi, 6 = dimanche)
    jours_vides = [{'jour': '', 'jour_semaine': '', 'jour_semaine_abbr': ''}] * premier_jour

    # Ajouter les jours vides au début de la liste
    jours_formattes = jours_vides + jours_formattes

    # Envoyer les données au template
    contexte = {
        'jours_formattes': jours_formattes,
        'mois': now.strftime('%B'),  # Mois en toutes lettres
        'annee': annee,
    }

    return render(request, 'authentication/view_administration_calendar.html', contexte)

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
