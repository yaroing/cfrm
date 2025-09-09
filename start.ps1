# Script de démarrage PowerShell pour la plateforme CFRM
# Usage: .\start.ps1 [dev|prod]

param(
    [string]$Mode = "dev"
)

# Fonction pour afficher des messages colorés
function Write-Message {
    param([string]$Message, [string]$Color = "Green")
    Write-Host "[CFRM] $Message" -ForegroundColor $Color
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[CFRM] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[CFRM] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[CFRM] $Message" -ForegroundColor Blue
}

# Vérifier si Docker est installé
try {
    docker --version | Out-Null
} catch {
    Write-Error "Docker n'est pas installé. Veuillez installer Docker Desktop d'abord."
    exit 1
}

try {
    docker-compose --version | Out-Null
} catch {
    Write-Error "Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
}

Write-Message "Démarrage de la plateforme CFRM en mode $Mode..."

# Créer les répertoires nécessaires
Write-Info "Création des répertoires nécessaires..."
New-Item -ItemType Directory -Force -Path "backend\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "frontend\.next" | Out-Null
New-Item -ItemType Directory -Force -Path "postgres_data" | Out-Null

# Vérifier les fichiers de configuration
if (-not (Test-Path "backend\.env")) {
    Write-Warning "Fichier backend\.env non trouvé. Copie depuis env.example..."
    Copy-Item "backend\env.example" "backend\.env"
    Write-Warning "Veuillez configurer backend\.env avant de continuer."
}

if (-not (Test-Path "frontend\.env.local")) {
    Write-Warning "Fichier frontend\.env.local non trouvé. Création..."
    @"
NEXT_PUBLIC_API_URL=http://localhost:8000/api
"@ | Out-File -FilePath "frontend\.env.local" -Encoding UTF8
}

# Construire les images Docker
Write-Info "Construction des images Docker..."
docker-compose build

# Démarrer les services
Write-Info "Démarrage des services..."
docker-compose up -d

# Attendre que la base de données soit prête
Write-Info "Attente de la base de données..."
Start-Sleep -Seconds 15

# Exécuter les migrations
Write-Info "Exécution des migrations de base de données..."
docker-compose exec -T backend python manage.py migrate

# Charger les données initiales
Write-Info "Chargement des données initiales..."
try {
    docker-compose exec -T backend python manage.py loaddata initial_data.json
} catch {
    Write-Warning "Fichier initial_data.json non trouvé. Création d'un superutilisateur..."
    Write-Info "Création d'un superutilisateur par défaut..."
    
    $pythonScript = @"
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
"@
    
    $pythonScript | docker-compose exec -T backend python manage.py shell
}

# Collecter les fichiers statiques
Write-Info "Collecte des fichiers statiques..."
docker-compose exec -T backend python manage.py collectstatic --noinput

# Vérifier le statut des services
Write-Info "Vérification du statut des services..."
docker-compose ps

# Afficher les URLs d'accès
Write-Message "Plateforme CFRM démarrée avec succès !"
Write-Host ""
Write-Info "URLs d'accès:"
Write-Host "  🌐 Frontend:     http://localhost:3000" -ForegroundColor Cyan
Write-Host "  🔧 Backend API:  http://localhost:8000/api" -ForegroundColor Cyan
Write-Host "  👤 Admin:        http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host "  📚 Documentation: http://localhost:8000/swagger/" -ForegroundColor Cyan
Write-Host ""
Write-Info "Identifiants par défaut:"
Write-Host "  👤 Utilisateur: admin" -ForegroundColor Yellow
Write-Host "  🔑 Mot de passe: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Warning "N'oubliez pas de changer le mot de passe par défaut !"
Write-Host ""
Write-Info "Pour arrêter les services: docker-compose down"
Write-Info "Pour voir les logs: docker-compose logs -f"
