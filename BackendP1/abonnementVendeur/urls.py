from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AbonnementViewSet, PlanAbonnementViewSet

router = DefaultRouter()
router.register('plans', PlanAbonnementViewSet, basename='plan-abonnement')
router.register('abonnements', AbonnementViewSet, basename='abonnement')

urlpatterns = [
    path('', include(router.urls)),
]
