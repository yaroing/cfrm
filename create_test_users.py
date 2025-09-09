#!/usr/bin/env python3
"""
Script pour créer des utilisateurs de test via l'API
"""
import requests
import json

API_BASE_URL = "http://localhost:8000/api/v1"

def create_user(username, email, first_name, last_name, password, role_id, is_staff=False, is_superuser=False):
    """Créer un utilisateur via l'API"""
    user_data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "password_confirm": password,  # Ajouter la confirmation du mot de passe
        "role": role_id,
        "is_staff": is_staff,
        "is_superuser": is_superuser,
        "is_active": True,
        "is_verified": True
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/users/", json=user_data)
        if response.status_code == 201:
            print(f"✅ Utilisateur {username} créé avec succès")
            return response.json()
        else:
            print(f"❌ Erreur lors de la création de {username}: {response.status_code}")
            print(f"   Détails: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion pour {username}: {e}")
        return None

def get_roles():
    """Récupérer les rôles disponibles"""
    try:
        response = requests.get(f"{API_BASE_URL}/roles/")
        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f"❌ Erreur lors de la récupération des rôles: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erreur de connexion pour les rôles: {e}")
        return []

def main():
    print("🚀 Création des utilisateurs de test...")
    
    # Récupérer les rôles
    print("📋 Récupération des rôles...")
    roles = get_roles()
    if not roles:
        print("❌ Impossible de récupérer les rôles")
        return
    
    # Créer un mapping des rôles
    role_map = {role["name"]: role["id"] for role in roles}
    print(f"✅ Rôles trouvés: {list(role_map.keys())}")
    
    # Définir les utilisateurs de test
    test_users = [
        {
            "username": "test_admin",
            "email": "admin@test.com",
            "first_name": "Admin",
            "last_name": "Test",
            "password": "admin123456",
            "role_name": "Admin",
            "is_staff": True,
            "is_superuser": True,
        },
        {
            "username": "test_manager",
            "email": "manager@test.com",
            "first_name": "Manager",
            "last_name": "Test",
            "password": "manager123456",
            "role_name": "Manager",
            "is_staff": True,
            "is_superuser": False,
        },
        {
            "username": "test_agent",
            "email": "agent@test.com",
            "first_name": "Agent",
            "last_name": "Test",
            "password": "agent123456",
            "role_name": "Agent",
            "is_staff": False,
            "is_superuser": False,
        },
        {
            "username": "test_psea",
            "email": "psea@test.com",
            "first_name": "PSEA",
            "last_name": "Focal Point",
            "password": "psea123456",
            "role_name": "PSEA_Focal_Point",
            "is_staff": True,
            "is_superuser": False,
        },
        {
            "username": "test_viewer",
            "email": "viewer@test.com",
            "first_name": "Viewer",
            "last_name": "Test",
            "password": "viewer123456",
            "role_name": "Viewer",
            "is_staff": False,
            "is_superuser": False,
        },
    ]
    
    # Créer les utilisateurs
    created_users = []
    for user_data in test_users:
        role_name = user_data["role_name"]
        if role_name not in role_map:
            print(f"❌ Rôle {role_name} non trouvé")
            continue
            
        role_id = role_map[role_name]
        user = create_user(
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password=user_data["password"],
            role_id=role_id,
            is_staff=user_data["is_staff"],
            is_superuser=user_data["is_superuser"]
        )
        
        if user:
            created_users.append({
                **user_data,
                "role_id": role_id
            })
    
    # Afficher le résumé
    print("\n🎉 Résumé de la création des utilisateurs:")
    print("=" * 60)
    for user in created_users:
        print(f"👤 {user['first_name']} {user['last_name']}")
        print(f"   Username: {user['username']}")
        print(f"   Password: {user['password']}")
        print(f"   Email: {user['email']}")
        print(f"   Rôle: {user['role_name']}")
        print(f"   Staff: {'Oui' if user['is_staff'] else 'Non'}")
        print(f"   Superuser: {'Oui' if user['is_superuser'] else 'Non'}")
        print()

if __name__ == "__main__":
    main()
