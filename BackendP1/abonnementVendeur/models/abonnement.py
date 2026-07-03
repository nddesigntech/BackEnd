from datetime import timedelta

from django.db import models
from django.utils import timezone

from authentification.models.user import CustomUser
from .plan_Abonnement import PlanAbonnement


class Abonnement(models.Model):
    """Représente un abonnement souscrit par un vendeur."""
    # Vendeur qui a pris cet abonnement
    vendeur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='abonnements')
    # Plan choisi par le vendeur
    plan = models.ForeignKey(PlanAbonnement, on_delete=models.PROTECT, related_name='abonnements')
    # Date de début de l'abonnement
    date_debut = models.DateTimeField(default=timezone.now)
    # Date de fin calculée à partir du plan
    date_fin = models.DateTimeField()
    # Statut actif ou inactif de l'abonnement
    actif = models.BooleanField(default=True)
    # Active ou non le renouvellement automatique
    renouvellement_automatique = models.BooleanField(default=False)
    # Date planifiée de renouvellement si activée
    date_renouvellement = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Abonnement {self.vendeur.username} - {self.plan.nom}'

    def save(self, *args, **kwargs):
        # Si la date de fin n'est pas fournie, on la calcule automatiquement
        if not self.date_fin:
            self.date_fin = self.date_debut + timedelta(days=self.plan.duree_jours)
        # Si le renouvellement automatique est activé, on fixe la date de renouvellement
        if self.renouvellement_automatique and not self.date_renouvellement:
            self.date_renouvellement = self.date_fin
        super().save(*args, **kwargs)

    def est_expire(self):
        """Retourne True si l'abonnement est expiré."""
        return timezone.now() > self.date_fin

    def get_jours_restants(self):
        """Retourne le nombre de jours restants avant l'expiration."""
        if self.est_expire():
            return 0
        return max((self.date_fin - timezone.now()).days, 0)

    def renouveler(self):
        """Renouvelle l'abonnement pour une nouvelle période."""
        self.date_debut = timezone.now()
        self.date_fin = self.date_debut + timedelta(days=self.plan.duree_jours)
        self.date_renouvellement = self.date_fin if self.renouvellement_automatique else None
        self.actif = True
        self.save()

    def annuler(self):
        """Annule l'abonnement immédiatement."""
        self.actif = False
        self.save()
