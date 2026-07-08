from rest_framework import permissions, viewsets

from .models import Produit
from .serializers import ProduitSerializer


class ProduitViewSet(viewsets.ModelViewSet):
    # Jeu de vues CRUD pour gérer les produits via l'API REST
    queryset = Produit.objects.all().order_by('-id')
    serializer_class = ProduitSerializer
    permission_classes = [permissions.IsAuthenticated]
