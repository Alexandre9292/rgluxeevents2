from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'phone_number', 'email')

class ChangeUserForm(UserChangeForm):    
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'profile_photo')
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
