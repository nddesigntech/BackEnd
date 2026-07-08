from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaiementViewSet

router = DefaultRouter()
router.register('', PaiementViewSet, basename='paiement')

urlpatterns = [
    path('', include(router.urls)),
]
