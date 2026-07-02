from django.db import models


class PlanAbonnement(models.Model):
    """Représente un plan d'abonnement disponible pour les vendeurs."""
    # Nom du plan, ex: Gratuit, Premium, Pro
    nom = models.CharField(max_length=150)
    # Description détaillée des avantages du plan
    description = models.TextField(blank=True)
    # Prix à payer pour ce plan
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    # Durée de l'abonnement en jours
    duree_jours = models.PositiveIntegerField(default=30)
    # Avantages inclus dans ce plan, stockés en texte libre
    avantages = models.TextField(blank=True)
    # Indique si le plan est activé et peut être souscrit
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nom} - {self.prix}€ / {self.duree_jours}j'

    def est_disponible(self):
        """Retourne True si le plan est actif et disponible à la souscription."""
        return self.actif

    def get_prix_par_jour(self):
        """Calcule le prix moyen par jour du plan."""
        if self.duree_jours <= 0:
            return 0
        return float(self.prix) / self.duree_jours
