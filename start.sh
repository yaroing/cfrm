#!/bin/bash

# Script de démarrage pour la plateforme CFRM
# Usage: ./start.sh [dev|prod]

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages colorés
print_message() {
    echo -e "${GREEN}[CFRM]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[CFRM]${NC} $1"
}

print_error() {
    echo -e "${RED}[CFRM]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[CFRM]${NC} $1"
}

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Mode par défaut
MODE=${1:-dev}

print_message "Démarrage de la plateforme CFRM en mode $MODE..."

# Créer les répertoires nécessaires
print_info "Création des répertoires nécessaires..."
mkdir -p backend/logs
mkdir -p frontend/.next
mkdir -p postgres_data

# Vérifier les fichiers de configuration
if [ ! -f "backend/.env" ]; then
    print_warning "Fichier backend/.env non trouvé. Copie depuis env.example..."
    cp backend/env.example backend/.env
    print_warning "Veuillez configurer backend/.env avant de continuer."
fi

if [ ! -f "frontend/.env.local" ]; then
    print_warning "Fichier frontend/.env.local non trouvé. Création..."
    cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOF
fi

# Construire les images Docker
print_info "Construction des images Docker..."
docker-compose build

# Démarrer les services
print_info "Démarrage des services..."
docker-compose up -d

# Attendre que la base de données soit prête
print_info "Attente de la base de données..."
sleep 10

# Exécuter les migrations
print_info "Exécution des migrations de base de données..."
docker-compose exec -T backend python manage.py migrate

# Charger les données initiales
print_info "Chargement des données initiales..."
docker-compose exec -T backend python manage.py loaddata initial_data.json 2>/dev/null || {
    print_warning "Fichier initial_data.json non trouvé. Création d'un superutilisateur..."
    print_info "Création d'un superutilisateur par défaut..."
    docker-compose exec -T backend python manage.py shell << EOF
from django.contrib.auth import get_user_model
from users.models import Organization, Role

User = get_user_model()

# Créer l'organisation par défaut si elle n'existe pas
org, created = Organization.objects.get_or_create(
    code='CFRM',
    defaults={
        'name': 'CFRM Platform',
        'description': 'Plateforme de feedback communautaire',
        'contact_email': 'admin@cfrm.org',
        'is_active': True
    }
)

# Créer le rôle admin si il n'existe pas
role, created = Role.objects.get_or_create(
    name='Admin',
    defaults={
        'description': 'Administrateur système',
        'permissions': ['all'],
        'is_psea_authorized': True,
        'can_escalate': True,
        'can_assign': True,
        'can_close': True,
        'can_view_analytics': True
    }
)

# Créer l'utilisateur admin si il n'existe pas
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@cfrm.org',
        password='admin123',
        first_name='Admin',
        last_name='CFRM',
        organization=org,
        role=role
    )
    print("Superutilisateur créé: admin/admin123")
else:
    print("Superutilisateur existe déjà")
EOF
}

# Collecter les fichiers statiques
print_info "Collecte des fichiers statiques..."
docker-compose exec -T backend python manage.py collectstatic --noinput

# Vérifier le statut des services
print_info "Vérification du statut des services..."
docker-compose ps

# Afficher les URLs d'accès
print_message "Plateforme CFRM démarrée avec succès !"
echo ""
print_info "URLs d'accès:"
echo "  🌐 Frontend:     http://localhost:3000"
echo "  🔧 Backend API:  http://localhost:8000/api"
echo "  👤 Admin:        http://localhost:8000/admin"
echo "  📚 Documentation: http://localhost:8000/swagger/"
echo ""
print_info "Identifiants par défaut:"
echo "  👤 Utilisateur: admin"
echo "  🔑 Mot de passe: admin123"
echo ""
print_warning "N'oubliez pas de changer le mot de passe par défaut !"
echo ""
print_info "Pour arrêter les services: docker-compose down"
print_info "Pour voir les logs: docker-compose logs -f"
