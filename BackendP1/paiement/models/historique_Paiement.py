from django.db import models
from django.utils import timezone


class HistoriquePaiement(models.Model):
    """Journalise les changements d'état d'un paiement."""
    paiement = models.ForeignKey('paiement.Paiement', on_delete=models.CASCADE, related_name='historiques')
    ancien_statut = models.CharField(max_length=50)
    nouveau_statut = models.CharField(max_length=50)
    commentaire = models.TextField(blank=True)
    date_maj = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Historique de paiement'
        verbose_name_plural = 'Historiques de paiement'
        ordering = ['-date_maj']

    def __str__(self):
        return f'Historique #{self.id} pour Paiement #{self.paiement.id}'

    def enregistrer(self):
        """Enregistre l'entrée d'historique dans la base de données."""
        self.date_maj = timezone.now()
        self.save()

    def est_valide(self):
        """Retourne True si l'entrée a des statuts anciens et nouveaux valides."""
        return bool(self.ancien_statut and self.nouveau_statut)
