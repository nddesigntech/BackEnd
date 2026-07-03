from django.db import models

from .user import CustomUser


class AdminProfile(models.Model):
    """Profil administrateur pour les utilisateurs ayant des droits avancés."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    niveau = models.PositiveSmallIntegerField(default=1)
    contact_interne = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'Admin {self.user.username} (niveau {self.niveau})'

    def has_privileges(self):
        """Indique si l'utilisateur a les privilèges d'administration élevés."""
        return self.user.is_superuser

    def set_niveau(self, niveau):
        """Définit le niveau d'administration."""
        self.niveau = niveau
        self.save()
