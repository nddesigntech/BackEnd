from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authentification.models.user import Utilisateur
from .models import PlanAbonnement


class AbonnementEndpointTests(TestCase):
    """Tests d'API pour la gestion des abonnements et des plans."""

    def setUp(self):
        self.client = APIClient()
        self.user = Utilisateur.objects.create_user(
            username='vendeur',
            email='vendeur@example.com',
            password='motdepasse123',
        )
        self.client.force_authenticate(user=self.user)

    def test_can_list_and_create_plans(self):
        """Vérifie qu'un utilisateur authentifié peut lister et créer un plan d'abonnement."""
        response = self.client.get('/api/abonnements/plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            '/api/abonnements/plans/',
            {
                'nom': 'Premium',
                'description': 'Accès complet',
                'prix': '19.99',
                'duree_jours': 30,
                'avantages': 'Support prioritaire',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanAbonnement.objects.count(), 1)
