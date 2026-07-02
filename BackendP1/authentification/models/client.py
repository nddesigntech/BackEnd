from django.db import models

from .user import CustomUser


class ClientProfile(models.Model):
    """Profil client pour l'utilisateur de type client."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    adresse = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Client {self.user.username}'

    def get_nom_complet(self):
        """Retourne le nom complet du client."""
        return f'{self.user.first_name} {self.user.last_name}'.strip()

    def is_client(self):
        """Vérifie si l'utilisateur est bien un client."""
        return self.user.role == 'client'
