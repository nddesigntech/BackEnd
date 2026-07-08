from rest_framework import permissions, viewsets

from .models import Abonnement, PlanAbonnement
from .serializers import AbonnementSerializer, PlanAbonnementSerializer


class PlanAbonnementViewSet(viewsets.ModelViewSet):
    """Vue permettant de lister et gérer les plans d'abonnement disponibles."""

    queryset = PlanAbonnement.objects.filter(actif=True).order_by('-id')
    serializer_class = PlanAbonnementSerializer
    permission_classes = [permissions.IsAuthenticated]


class AbonnementViewSet(viewsets.ModelViewSet):
    """Vue permettant de gérer les abonnements souscrits par les vendeurs."""

    queryset = Abonnement.objects.select_related('plan', 'vendeur').order_by('-id')
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Limite la visibilité des abonnements à l'utilisateur connecté, sauf pour les administrateurs."""
        user = self.request.user
        if user.is_staff or user.role == 'admin':
            return self.queryset
        return self.queryset.filter(vendeur=user)
