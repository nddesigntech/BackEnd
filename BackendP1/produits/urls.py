from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProduitViewSet

router = DefaultRouter()
router.register('', ProduitViewSet, basename='produit')

urlpatterns = [
    # Toutes les routes CRUD pour les produits via le router DRF
    path('', include(router.urls)),
]
