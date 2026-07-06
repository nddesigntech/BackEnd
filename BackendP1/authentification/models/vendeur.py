from django.db import models

from .user import Utilisateur


class VendeurProfile(models.Model):
    """Profil vendeur pour l'utilisateur ayant le rôle vendeur."""
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='vendeur_profile')
    nom_boutique = models.CharField(max_length=255, blank=True)
    siret = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    adresse_boutique = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        boutique = self.nom_boutique or 'Sans boutique'
        return f'Vendeur {self.user.username} ({boutique})'

    def activer_compte(self):
        """Active le compte vendeur."""
        self.is_active = True
        self.save()

    def desactiver_compte(self):
        """Désactive le compte vendeur."""
        self.is_active = False
        self.save()

    def get_contact(self):
        """Retourne les informations de contact du vendeur."""
        return {
            'telephone': self.telephone,
            'adresse_boutique': self.adresse_boutique,
            'nom_boutique': self.nom_boutique,
        }
