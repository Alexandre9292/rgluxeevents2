from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager 
from django.utils.translation import gettext_lazy  as _
from phonenumber_field.modelfields import PhoneNumberField
import os

def upload_to_profile(instance, filename):
    # Extraire l'extension du fichier
    ext = filename.split('.')[-1]
    # Créer un nouveau nom de fichier basé sur l'email et l'extension originale
    filename = f"profile.{ext}"
    # Retourner le chemin : email de la personne / profile_pics / nom du fichier
    return os.path.join(instance.email, 'profile_pics', filename)

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ADMINISTRATION = 'ADMIN'
    CUSTOMER = 'CUSTOMER'

    ROLE_CHOICES = (
        (ADMINISTRATION, 'Admin'),
        (CUSTOMER, 'Customer'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='rôle')
    profile_photo = models.ImageField(verbose_name='photo de profil', null=True, upload_to=upload_to_profile, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=False)

    objects = UserManager()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.ADMINISTRATION:
            group = Group.objects.get(name='administrator')
            group.user_set.add(self)
        elif self.role == self.CUSTOMER:
            group = Group.objects.get(name='customer')
            group.user_set.add(self)




