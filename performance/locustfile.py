"""
Tests de performance avec Locust pour l'API CFRM
"""
from locust import HttpUser, task, between
import json
import random


class CFRMUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Connexion de l'utilisateur au début de la session"""
        self.login()
    
    def login(self):
        """Connexion à l'API"""
        response = self.client.post("/api/v1/auth/login/", json={
            "username": "admin",
            "password": "admin123"
        })
        if response.status_code == 200:
            self.token = response.json()["access"]
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
    
    @task(3)
    def get_tickets(self):
        """Récupérer la liste des tickets"""
        self.client.get("/api/v1/tickets/tickets/")
    
    @task(2)
    def get_dashboard_stats(self):
        """Récupérer les statistiques du tableau de bord"""
        self.client.get("/api/v1/tickets/tickets/dashboard_stats/")
    
    @task(1)
    def create_ticket(self):
        """Créer un nouveau ticket"""
        ticket_data = {
            "title": f"Ticket de test {random.randint(1, 1000)}",
            "content": "Ceci est un ticket de test créé par Locust",
            "category": 1,
            "priority": 3,
            "channel": 4,
            "submitter_name": "Test User",
            "submitter_email": "test@example.com"
        }
        self.client.post("/api/v1/tickets/tickets/", json=ticket_data)
    
    @task(1)
    def get_categories(self):
        """Récupérer les catégories"""
        self.client.get("/api/v1/tickets/categories/")
    
    @task(1)
    def get_priorities(self):
        """Récupérer les priorités"""
        self.client.get("/api/v1/tickets/priorities/")
    
    @task(1)
    def get_statuses(self):
        """Récupérer les statuts"""
        self.client.get("/api/v1/tickets/statuses/")
    
    @task(1)
    def get_channels(self):
        """Récupérer les canaux"""
        self.client.get("/api/v1/tickets/channels/")
