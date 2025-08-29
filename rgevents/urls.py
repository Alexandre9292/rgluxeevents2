"""
URL configuration for rgevents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app import views
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView)
from django.contrib.auth import views as auth_views
from django.views.defaults import page_not_found

import app.views
import authentication.views

# Configuration pour la page 404 personnalisée
handler404 = 'app.views.handler404'

urlpatterns = [
    path('', app.views.home, name='home'),
    path('admin/', admin.site.urls),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),      
    path('password_reset', authentication.views.password_reset_request, name="password_reset"), 
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='change-password'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='change-password-done'
         ),
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('new-user/', authentication.views.new_user_page, name='new_user'),
    path('customer/', authentication.views.customer_page, name='customer'),
    path('customer/<int:user_id>/change/', authentication.views.edit_user, name='edit_user'),
    path('administration/calendrier/', authentication.views.admin_page_calendar, name='admin-calendar'),
    path('administration/calendrier/<int:year>/<int:month>/', authentication.views.admin_page_calendar, name='admin-calendar'),
    path('administration/calendrier/<int:year>/<int:month>/<int:day>', authentication.views.admin_page_calendar, name='admin-calendar'),
    path('administration/utilisateurs', authentication.views.admin_page_users, name='admin-users'),
    path('get_activity_info/<int:acti_id>/<str:acti_type>', authentication.views.get_activity_info, name='get_activity_info'),

    path('mentions-legales/', authentication.views.mentions_legales, name='mention'),
    
    path('about/', app.views.about, name='about'),
    path('contact/', app.views.contact, name='contact'),
    
    # Nouvelles pages de services
    path('transport/', app.views.transport, name='transport'),
    path('transport/summary/<int:booking_id>/', app.views.transport_summary, name='transport_summary'),
    path('photobooth/', app.views.photobooth, name='photobooth'),
    path('photobooth/validation/', app.views.photobooth_validation, name='photobooth_validation'),
    path('photobooth/conditions/', app.views.photobooth_terms, name='photobooth_terms'),
    path('drone/', app.views.drone, name='drone'),
    
    # URL de test pour la page 404 (à supprimer en production)
    path('test-404/', app.views.test_404, name='test_404'),
    
    # URL directe pour tester la page 404
    path('404/', app.views.page_404, name='page_404'),
    
    # URL pour tester le middleware 404
    path('trigger-404/', app.views.trigger_404, name='trigger_404'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
