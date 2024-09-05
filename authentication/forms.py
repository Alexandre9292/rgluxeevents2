from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

class ChangeUserForm(UserChangeForm):    
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe', required=False)
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Confirmation Mot de passe', required=False)
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
