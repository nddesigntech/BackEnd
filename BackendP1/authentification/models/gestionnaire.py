from django.db import models

from .user import CustomUser


class GestionnaireProfile(models.Model):
    """Profil gestionnaire pour les administrateurs internes."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='gestionnaire_profile')
    departement = models.CharField(max_length=100, blank=True)
    statut = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Gestionnaire {self.user.username}'

    def get_role_description(self):
        """Retourne une description du rôle du gestionnaire."""
        return f'Gestionnaire en charge de {self.departement or "la plateforme"} ({self.statut})'
