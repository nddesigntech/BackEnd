from django.db import models
from django.utils import timezone

from authentification.models.user import CustomUser


class Paiement(models.Model):
    """Modèle représentant une transaction de paiement."""
    PAYMENT_METHOD_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('paypal', 'PayPal'),
        ('virement', 'Virement bancaire'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('payé', 'Payé'),
        ('échoué', 'Échoué'),
        ('annulé', 'Annulé'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='carte')
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    date_paiement = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=200, blank=True)
    commande_reference = models.CharField(max_length=200, blank=True)
    abonnement = models.ForeignKey(
        'abonnementVendeur.Abonnement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paiements_generaux',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return f'Paiement #{self.id} - {self.montant}€ - {self.get_statut_display()}'

    def est_payé(self):
        """Retourne True si le paiement est finalisé avec succès."""
        return self.statut == 'payé'

    def est_en_attente(self):
        """Retourne True si le paiement est encore en attente."""
        return self.statut == 'en_attente'

    def est_echoue(self):
        """Retourne True si le paiement a échoué."""
        return self.statut == 'échoué'

    def est_annule(self):
        """Retourne True si le paiement a été annulé."""
        return self.statut == 'annulé'

    def marquer_payé(self, reference=None):
        """Marque le paiement comme payé et enregistre la référence de transaction."""
        self.statut = 'payé'
        if reference:
            self.reference = reference
        self.date_paiement = timezone.now()
        self.save(update_fields=['statut', 'reference', 'date_paiement', 'updated_at'])

    def marquer_echoue(self, message=None):
        """Marque le paiement comme échoué et conserve un message de suivi."""
        self.statut = 'échoué'
        if message:
            self.reference = message
        self.save(update_fields=['statut', 'reference', 'updated_at'])

    def annuler(self):
        """Annule le paiement sans effectuer la transaction."""
        self.statut = 'annulé'
        self.save(update_fields=['statut', 'updated_at'])

    def creer_historique(self, ancien_statut, nouveau_statut, commentaire=''):
        """Crée une entrée d'historique pour ce paiement."""
        from .historique_Paiement import HistoriquePaiement

        HistoriquePaiement.objects.create(
            paiement=self,
            ancien_statut=ancien_statut,
            nouveau_statut=nouveau_statut,
            commentaire=commentaire,
        )
