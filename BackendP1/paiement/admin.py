from django.contrib import admin

from .models import HistoriquePaiement, Paiement


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'montant', 'mode_paiement', 'statut', 'date_paiement']
    list_filter = ['statut', 'mode_paiement']
    search_fields = ['user__username', 'reference', 'commande_reference']


@admin.register(HistoriquePaiement)
class HistoriquePaiementAdmin(admin.ModelAdmin):
    list_display = ['id', 'paiement', 'ancien_statut', 'nouveau_statut', 'date_maj']
    search_fields = ['paiement__reference', 'commentaire']
