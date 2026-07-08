from rest_framework import serializers

from .models import Abonnement, PlanAbonnement


class PlanAbonnementSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la gestion des plans d'abonnement."""

    class Meta:
        model = PlanAbonnement
        fields = '__all__'


class AbonnementSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la gestion des abonnements souscrits par les vendeurs."""

    jours_restants = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Abonnement
        fields = [
            'id',
            'vendeur',
            'plan',
            'date_debut',
            'date_fin',
            'actif',
            'renouvellement_automatique',
            'date_renouvellement',
            'jours_restants',
        ]
        read_only_fields = ['vendeur', 'date_debut', 'date_fin', 'date_renouvellement', 'jours_restants']

    def get_jours_restants(self, obj):
        """Retourne le nombre de jours restants avant expiration."""
        return obj.get_jours_restants()

    def create(self, validated_data):
        """Assigne automatiquement l'utilisateur connecté comme vendeur."""
        validated_data['vendeur'] = self.context['request'].user
        return super().create(validated_data)
