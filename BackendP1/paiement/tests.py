from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authentification.models.user import Utilisateur


class PaiementEndpointTests(TestCase):
    """Tests d'API pour la gestion des paiements."""

    def setUp(self):
        self.client = APIClient()
        self.user = Utilisateur.objects.create_user(
            username='client',
            email='client@example.com',
            password='motdepasse123',
        )
        self.client.force_authenticate(user=self.user)

    def test_can_list_and_create_payments(self):
        """Vérifie qu'un utilisateur authentifié peut lister et créer un paiement."""
        response = self.client.get('/api/paiements/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            '/api/paiements/',
            {
                'montant': '12.50',
                'mode_paiement': 'carte',
                'statut': 'en_attente',
                'commande_reference': 'CMD-100',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
