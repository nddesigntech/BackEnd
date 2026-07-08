from rest_framework import permissions, viewsets

from .models import Paiement
from .serializers import PaiementSerializer


class PaiementViewSet(viewsets.ModelViewSet):
    """Vue permettant de gérer les paiements réalisés par les utilisateurs."""

    queryset = Paiement.objects.select_related('user').order_by('-id')
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Affiche uniquement les paiements de l'utilisateur connecté, sauf pour les administrateurs."""
        user = self.request.user
        if user.is_staff or user.role == 'admin':
            return self.queryset
        return self.queryset.filter(user=user)
