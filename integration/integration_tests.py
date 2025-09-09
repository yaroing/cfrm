"""
Tests d'intégration pour la plateforme CFRM
"""
import pytest
import requests
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, Mock
import json

User = get_user_model()


class IntegrationTests(TransactionTestCase):
    """Tests d'intégration pour l'API CFRM"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_complete_ticket_workflow(self):
        """Test du workflow complet d'un ticket"""
        # 1. Créer un ticket
        ticket_data = {
            "title": "Test Integration Ticket",
            "content": "This is a test ticket for integration testing",
            "category": 1,
            "priority": 3,
            "channel": 4,
            "submitter_name": "Test User",
            "submitter_email": "test@example.com"
        }
        
        response = self.client.post("/api/v1/tickets/tickets/", ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ticket_id = response.json()['id']
        
        # 2. Récupérer le ticket
        response = self.client.get(f"/api/v1/tickets/tickets/{ticket_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket = response.json()
        self.assertEqual(ticket['title'], ticket_data['title'])
        
        # 3. Assigner le ticket
        response = self.client.post(f"/api/v1/tickets/tickets/{ticket_id}/assign/", {
            "assigned_to": self.user.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Ajouter une réponse
        response_data = {
            "content": "This is a response to the ticket",
            "is_internal": False,
            "channel": 4
        }
        response = self.client.post("/api/v1/tickets/responses/", {
            "ticket": ticket_id,
            **response_data
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 5. Fermer le ticket
        response = self.client.post(f"/api/v1/tickets/tickets/{ticket_id}/close/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 6. Vérifier que le ticket est fermé
        response = self.client.get(f"/api/v1/tickets/tickets/{ticket_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket = response.json()
        self.assertEqual(ticket['status']['name'], 'Fermé')
    
    def test_sms_webhook_integration(self):
        """Test d'intégration du webhook SMS"""
        # Simuler un webhook Twilio
        webhook_data = {
            "MessageSid": "SM1234567890",
            "MessageStatus": "delivered",
            "From": "+1234567890",
            "To": "+0987654321",
            "Body": "Test SMS message"
        }
        
        response = self.client.post("/api/v1/channels/webhooks/sms/", webhook_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que le message est créé
        response = self.client.get("/api/v1/channels/messages/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        messages = response.json()['results']
        self.assertTrue(any(msg['external_id'] == 'SM1234567890' for msg in messages))
    
    def test_whatsapp_webhook_integration(self):
        """Test d'intégration du webhook WhatsApp"""
        # Simuler un webhook WhatsApp
        webhook_data = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "1234567890",
                            "text": {"body": "Test WhatsApp message"}
                        }]
                    }
                }]
            }]
        }
        
        response = self.client.post("/api/v1/channels/webhooks/whatsapp/", webhook_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_email_integration(self):
        """Test d'intégration email"""
        with patch('django.core.mail.send_mail') as mock_send:
            mock_send.return_value = True
            
            # Créer un ticket via email
            ticket_data = {
                "title": "Email Ticket",
                "content": "This ticket was created via email",
                "category": 1,
                "priority": 3,
                "channel": 3,  # Email channel
                "submitter_email": "test@example.com"
            }
            
            response = self.client.post("/api/v1/tickets/tickets/", ticket_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
            # Vérifier que l'email de confirmation est envoyé
            mock_send.assert_called_once()
    
    def test_analytics_integration(self):
        """Test d'intégration des analytics"""
        # Créer plusieurs tickets pour les tests
        for i in range(5):
            ticket_data = {
                "title": f"Analytics Test Ticket {i}",
                "content": f"Test content {i}",
                "category": 1,
                "priority": 3,
                "channel": 4
            }
            self.client.post("/api/v1/tickets/tickets/", ticket_data)
        
        # Récupérer les statistiques
        response = self.client.get("/api/v1/tickets/tickets/dashboard_stats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        stats = response.json()
        self.assertIn('status_stats', stats)
        self.assertIn('category_stats', stats)
        self.assertIn('channel_stats', stats)
    
    def test_user_management_integration(self):
        """Test d'intégration de la gestion des utilisateurs"""
        # Créer un nouvel utilisateur
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User"
        }
        
        response = self.client.post("/api/v1/users/users/", user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Vérifier que l'utilisateur est créé
        response = self.client.get("/api/v1/users/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users = response.json()['results']
        self.assertTrue(any(user['username'] == 'newuser' for user in users))
    
    def test_channel_management_integration(self):
        """Test d'intégration de la gestion des canaux"""
        # Récupérer les canaux
        response = self.client.get("/api/v1/channels/channels/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        channels = response.json()['results']
        self.assertTrue(len(channels) > 0)
        
        # Tester un canal
        channel = channels[0]
        response = self.client.post(f"/api/v1/channels/channels/{channel['id']}/test_connection/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_error_handling_integration(self):
        """Test d'intégration de la gestion des erreurs"""
        # Test avec des données invalides
        invalid_data = {
            "title": "",  # Titre vide
            "content": "",  # Contenu vide
            "category": 999,  # Catégorie inexistante
        }
        
        response = self.client.post("/api/v1/tickets/tickets/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Vérifier que l'erreur est bien formatée
        error_data = response.json()
        self.assertIn('errors', error_data or {})
    
    def test_performance_integration(self):
        """Test d'intégration des performances"""
        import time
        
        # Mesurer le temps de réponse pour la liste des tickets
        start_time = time.time()
        response = self.client.get("/api/v1/tickets/tickets/")
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end_time - start_time, 1.0)  # Moins d'1 seconde
    
    def test_security_integration(self):
        """Test d'intégration de la sécurité"""
        # Test d'authentification
        self.client.logout()
        response = self.client.get("/api/v1/tickets/tickets/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test d'autorisation
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/tickets/tickets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_data_consistency_integration(self):
        """Test d'intégration de la cohérence des données"""
        # Créer un ticket
        ticket_data = {
            "title": "Consistency Test",
            "content": "Test content",
            "category": 1,
            "priority": 3,
            "channel": 4
        }
        
        response = self.client.post("/api/v1/tickets/tickets/", ticket_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ticket_id = response.json()['id']
        
        # Modifier le ticket
        update_data = {"title": "Updated Title"}
        response = self.client.patch(f"/api/v1/tickets/tickets/{ticket_id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que les modifications sont persistées
        response = self.client.get(f"/api/v1/tickets/tickets/{ticket_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket = response.json()
        self.assertEqual(ticket['title'], 'Updated Title')
