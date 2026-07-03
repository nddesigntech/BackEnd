from django.db import models
from django.utils import timezone

from authentification.models.user import CustomUser
from .abonnement import Abonnement


class PaiementAbonnement(models.Model):
    """Représente un paiement lié à un abonnement vendeur."""
    # Abonnement concerné par ce paiement
    abonnement = models.ForeignKey(Abonnement, on_delete=models.CASCADE, related_name='paiements')
    # Montant payé ou à payer
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    # Date et heure du paiement
    date_paiement = models.DateTimeField(default=timezone.now)
    # Statut du paiement : en_attente, payé, échoué...
    statut = models.CharField(max_length=50, default='en_attente')
    # Référence de transaction fournie par le système de paiement
    reference = models.CharField(max_length=200, blank=True)
    # Vendeur qui réalise ce paiement
    vendeur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='paiements_abonnement')

    def __str__(self):
        return f'Paiement {self.id} - {self.montant}€'

    def marquer_payé(self, reference=None):
        """Marque le paiement comme payé et stocke la référence de transaction."""
        self.statut = 'payé'
        if reference:
            self.reference = reference
        self.date_paiement = timezone.now()
        self.save()

    def est_payé(self):
        """Retourne True si le paiement est finalisé."""
        return self.statut == 'payé'

    def est_en_attente(self):
        """Retourne True si le paiement est encore en attente."""
        return self.statut == 'en_attente'
