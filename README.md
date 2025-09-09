# CFRM - Plateforme Multicanal de Feedback Communautaire

Une plateforme sécurisée et interopérable pour la collecte et la gestion du feedback communautaire dans le secteur humanitaire, conforme aux standards CHS, IASC, UNHCR et IFRC.

## 🎯 Objectifs

- **Collecte multicanal** : SMS, WhatsApp, Web, Email, Téléphone
- **Sécurité renforcée** : Chiffrement AES-256, authentification JWT, rôles granulaires
- **Conformité normative** : CHS, IASC, UNHCR, IFRC, PSEA
- **Interopérabilité** : API RESTful, intégrations tierces
- **Analytics avancés** : Tableaux de bord, rapports, métriques

## 🏗️ Architecture

### Stack Technologique

- **Frontend** : React/Next.js avec TypeScript et Tailwind CSS
- **Backend** : Django REST Framework avec Python
- **Base de données** : PostgreSQL avec chiffrement au repos
- **Cache** : Redis pour les sessions et les tâches asynchrones
- **Queue** : Celery pour les tâches en arrière-plan
- **Conteneurisation** : Docker et Docker Compose

### Services Tiers

- **SMS** : Twilio/FrontlineSMS
- **WhatsApp** : WhatsApp Business Cloud API
- **Email** : SMTP sécurisé
- **Monitoring** : Logs structurés et métriques

## 🚀 Installation et Démarrage

### Prérequis

- Docker et Docker Compose
- Git

### Installation

1. **Cloner le repository**
   ```bash
   git clone <repository-url>
   cd cfrm_projet
   ```

2. **Configuration de l'environnement**
   ```bash
   # Backend
   cp backend/env.example backend/.env
   # Modifier les valeurs dans backend/.env
   
   # Frontend
   cp frontend/.env.example frontend/.env.local
   # Modifier les valeurs dans frontend/.env.local
   ```

3. **Démarrage des services**
   ```bash
   docker-compose up -d
   ```

4. **Initialisation de la base de données**
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py loaddata initial_data.json
   ```

5. **Création d'un superutilisateur**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

### Accès aux services

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/api
- **Admin Django** : http://localhost:8000/admin
- **Documentation API** : http://localhost:8000/swagger/

## 📋 Fonctionnalités

### Collecte Multicanal

- **SMS** : Collecte via Twilio avec numéros courts
- **WhatsApp** : Intégration Business API avec templates
- **Web** : Formulaires accessibles et multilingues
- **Email** : Collecte via SMTP sécurisé
- **Téléphone** : Hotline avec enregistrement

### Gestion des Tickets

- **Classification automatique** : IA légère pour pré-classifier
- **Priorisation** : Niveaux de priorité avec SLA
- **Assignation** : Workflow d'assignation intelligent
- **Escalade** : Escalade automatique PSEA/SEA
- **Traçabilité** : Journal complet des actions

### Sécurité et Conformité

- **Chiffrement** : AES-256 pour les données sensibles
- **Authentification** : JWT avec refresh tokens
- **Autorisation** : Rôles granulaires (Admin, Manager, Agent, PSEA Focal Point)
- **Audit** : Logs immuables de toutes les actions
- **PSEA** : Circuits sécurisés pour les cas sensibles

### Analytics et Rapports

- **Tableaux de bord** : Métriques temps réel
- **Rapports** : Génération automatique (CSV, Excel, PDF)
- **Métriques** : KPIs conformes CHS/IASC
- **Alertes** : Notifications basées sur les seuils

## 🔧 Configuration

### Variables d'environnement

#### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://cfrm_user:cfrm_password@db:5432/cfrm_db
REDIS_URL=redis://redis:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
WHATSAPP_ACCESS_TOKEN=your-whatsapp-token
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Configuration des canaux

1. **SMS (Twilio)**
   - Créer un compte Twilio
   - Obtenir Account SID et Auth Token
   - Configurer le numéro de téléphone

2. **WhatsApp Business**
   - Créer une application Facebook
   - Configurer WhatsApp Business API
   - Obtenir l'access token et phone number ID

3. **Email SMTP**
   - Configurer un serveur SMTP sécurisé
   - Utiliser TLS/SSL pour la sécurité

## 📊 API Documentation

### Endpoints Principaux

#### Tickets
- `GET /api/v1/tickets/` - Liste des tickets
- `POST /api/v1/tickets/` - Créer un ticket
- `GET /api/v1/tickets/{id}/` - Détails d'un ticket
- `PATCH /api/v1/tickets/{id}/` - Modifier un ticket
- `POST /api/v1/tickets/{id}/assign/` - Assigner un ticket
- `POST /api/v1/tickets/{id}/close/` - Fermer un ticket

#### Canaux
- `GET /api/v1/channels/` - Liste des canaux
- `POST /api/v1/channels/{id}/send_test_message/` - Envoyer un message de test
- `POST /api/v1/webhooks/sms/` - Webhook SMS
- `POST /api/v1/webhooks/whatsapp/` - Webhook WhatsApp

#### Analytics
- `GET /api/v1/analytics/dashboard_stats/` - Statistiques du tableau de bord
- `GET /api/v1/analytics/reports/` - Liste des rapports
- `POST /api/v1/analytics/reports/` - Créer un rapport

### Authentification

```bash
# Connexion
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Utilisation du token
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/tickets/
```

## 🧪 Tests

### Tests Backend
```bash
docker-compose exec backend python manage.py test
```

### Tests Frontend
```bash
docker-compose exec frontend npm test
```

### Tests d'intégration
```bash
docker-compose exec backend python manage.py test --settings=cfrm.test_settings
```

## 📈 Monitoring et Logs

### Logs
- **Backend** : `/backend/logs/cfrm.log`
- **Frontend** : Console du navigateur
- **Docker** : `docker-compose logs -f`

### Métriques
- **Performance** : Temps de réponse, débit
- **Sécurité** : Tentatives de connexion, accès
- **Fonctionnel** : Tickets créés/fermés, satisfaction

## 🔒 Sécurité

### Bonnes Pratiques Implémentées

- **Chiffrement** : AES-256 pour les données sensibles
- **HTTPS** : TLS 1.3 pour toutes les communications
- **Authentification** : JWT avec rotation des tokens
- **Autorisation** : RBAC avec permissions granulaires
- **Audit** : Logs immuables de toutes les actions
- **Validation** : Validation stricte des entrées
- **Rate Limiting** : Protection contre les attaques par déni de service

### Conformité PSEA

- **Circuits sécurisés** : Accès restreint aux cas PSEA
- **Anonymisation** : Option d'anonymat pour les plaintes
- **Escalade automatique** : Notification immédiate des cas sensibles
- **Traçabilité** : Journal détaillé des actions PSEA

## 🤝 Contribution

### Workflow de Développement

1. **Fork** du repository
2. **Création** d'une branche feature
3. **Développement** avec tests
4. **Pull Request** avec description détaillée

### Standards de Code

- **Backend** : PEP 8, type hints, docstrings
- **Frontend** : ESLint, Prettier, TypeScript strict
- **Tests** : Couverture > 80%
- **Documentation** : README à jour

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

### Documentation
- [Guide utilisateur](docs/user-guide.md)
- [Guide administrateur](docs/admin-guide.md)
- [Guide développeur](docs/developer-guide.md)

### Contact
- **Email** : support@cfrm.org
- **Issues** : [GitHub Issues](https://github.com/your-org/cfrm/issues)
- **Discussions** : [GitHub Discussions](https://github.com/your-org/cfrm/discussions)

## 🙏 Remerciements

- **Standards humanitaires** : CHS Alliance, IASC, UNHCR, IFRC
- **Communauté open source** : Django, React, PostgreSQL
- **Partenaires** : Twilio, Meta (WhatsApp), organisations humanitaires

---

**CFRM** - Construire des communautés plus fortes grâce au feedback
