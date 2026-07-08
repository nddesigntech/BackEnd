from rest_framework import serializers

from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la gestion des paiements effectués par les utilisateurs."""

    class Meta:
        model = Paiement
        fields = [
            'id',
            'user',
            'montant',
            'mode_paiement',
            'statut',
            'date_paiement',
            'reference',
            'commande_reference',
            'abonnement',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user', 'date_paiement', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Assigne automatiquement l'utilisateur connecté comme auteur du paiement."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
