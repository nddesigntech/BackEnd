from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


# Modèle utilisateur personnalisé pour le système d'authentification
# Ce modèle remplace l'utilisateur Django par défaut pour ajouter des rôles spécifiques à la plateforme.
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        # Création d'un utilisateur normal avec email et mot de passe
        if not username:
            raise ValueError('The username must be set')
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('vendeur', 'Vendeur'),
        ('gestionnaire', 'Gestionnaire'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class BlacklistedToken(models.Model):
    # Stocke les tokens JWT invalidés lors du logout
    token = models.CharField(max_length=500, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Blacklisted token expiring {self.expires_at}'
