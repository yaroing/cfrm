# Tests de la Plateforme CFRM Humanitaire

Ce répertoire contient tous les outils de test pour la plateforme de feedback communautaire humanitaire CFRM.

## 📁 Structure des Fichiers

```
tests/
├── README.md                    # Ce fichier
├── run_tests.py                 # Script principal d'exécution
├── test_automation.py           # Tests automatisés
├── test_data.py                 # Générateur de données de test
├── test_scenarios.md            # Scénarios de test détaillés
├── kpi_metrics.py              # Calcul des KPI et métriques
└── test_report_template.md     # Modèle de rapport de test
```

## 🚀 Utilisation Rapide

### Exécution Simple
```bash
cd tests
python run_tests.py
```

### Exécution avec Configuration
```bash
python run_tests.py --base-url http://localhost:8000 --verbose
```

## 📊 Types de Tests

### 1. Tests de Réception
- **SMS** : Messages multilingues, PSEA, urgences
- **Web** : Formulaires sécurisés, données sensibles
- **Messageries** : WhatsApp, Telegram, groupes

### 2. Tests de Classification
- Classification automatique par catégorie
- Détection de la priorité
- Analyse du sentiment
- Détection PSEA/SEA

### 3. Tests de Performance
- Charge normale (100 msg/min)
- Charge élevée (500 msg/min)
- Pic de charge (1000 msg/min)
- Temps de réponse

### 4. Tests de Sécurité
- Protection contre les injections SQL
- Protection XSS
- Chiffrement des données PSEA
- Conformité RGPD

### 5. Tests d'Intégration
- APIs SMS (Twilio)
- APIs WhatsApp Business
- Service de traduction
- Notifications email

## 🎯 KPI et Métriques

### Métriques Critiques
- **Taux de réception** : ≥ 99.5%
- **Délai de traitement** : ≤ 15 minutes
- **Précision classification** : ≥ 85%
- **Satisfaction utilisateur** : ≥ 8.0/10
- **Taux d'escalade PSEA** : 100%

### Métriques par Canal
- **SMS** : Taux de succès, temps de réponse, satisfaction
- **Web** : Completion des formulaires, sécurité
- **Messageries** : Intégration, médias, groupes

## 🔧 Configuration

### Variables d'Environnement
```bash
export CFRM_BASE_URL="http://localhost:8000"
export CFRM_TEST_MODE="development"
export CFRM_LOG_LEVEL="INFO"
```

### Configuration des Tests
```python
# Dans test_automation.py
tester = CFRMTestRunner(
    base_url="http://localhost:8000",
    timeout=30,
    retry_count=3
)
```

## 📈 Génération de Données

### Données Humanitaires Réalistes
Le générateur crée des données contextuelles :
- **Langues** : Français, Anglais, Arabe, Espagnol, Swahili, Amharique, Somali, Tigrinya
- **Catégories** : Information, Complaint, Request, PSEA, SEA, Feedback, Suggestion
- **Contextes** : Camps de réfugiés, déplacement, urgence, récupération
- **Populations** : Réfugiés, PDI, communautés d'accueil, groupes vulnérables

### Exemple d'Utilisation
```python
from test_data import TestDataGenerator

generator = TestDataGenerator()

# Générer 100 messages SMS
sms_messages = generator.generate_sms_messages(100)

# Générer 50 formulaires web
web_forms = generator.generate_web_forms(50)

# Générer 75 messages de messagerie
messaging_messages = generator.generate_messaging_messages(75)
```

## 📋 Scénarios de Test

### Scénarios SMS
- **SMS-001** : Demande d'aide alimentaire
- **SMS-002** : Problème eau potable urgent
- **SMS-003** : Message multilingue (arabe)
- **SMS-004** : Signalement PSEA
- **SMS-005** : Message de remerciement

### Scénarios Web
- **WEB-001** : Formulaire complet valide
- **WEB-002** : Formulaire avec pièce jointe
- **WEB-003** : Formulaire PSEA sécurisé
- **WEB-004** : Formulaire de remerciement
- **WEB-005** : Informations de vulnérabilité

### Scénarios Messageries
- **MSG-001** : WhatsApp - Demande d'aide
- **MSG-002** : WhatsApp - Photo problème
- **MSG-003** : Groupe - Coordination
- **MSG-004** : WhatsApp - Signalement PSEA
- **MSG-005** : Message arabe

## 📊 Rapports de Test

### Format JSON
```json
{
  "test_summary": {
    "test_date": "2024-01-15T10:30:00",
    "total_scenarios": 100,
    "scenarios_passed": 95,
    "scenarios_failed": 5,
    "success_rate": 95.0
  },
  "test_results": { ... },
  "kpi_results": { ... },
  "recommendations": [ ... ]
}
```

### Format Markdown
Le rapport est également généré en format Markdown pour une lecture facile.

## 🔍 Dépannage

### Problèmes Courants

#### 1. Erreur de Connexion
```
💥 Erreur lors de l'exécution des tests: Connection refused
```
**Solution** : Vérifier que le backend est démarré sur le port 8000

#### 2. Timeout des Tests
```
⚠️ Tests terminés avec des avertissements.
```
**Solution** : Augmenter le timeout dans la configuration

#### 3. Échec de Classification
```
❌ Classification incorrecte de 2 messages
```
**Solution** : Vérifier l'algorithme de classification et enrichir le dataset

### Logs de Debug
```bash
python run_tests.py --verbose --debug
```

## 🚀 Intégration CI/CD

### GitHub Actions
```yaml
name: CFRM Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python tests/run_tests.py
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'python tests/run_tests.py'
            }
        }
    }
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'tests',
                reportFiles: 'test_report_*.html',
                reportName: 'CFRM Test Report'
            ])
        }
    }
}
```

## 📚 Documentation Supplémentaire

- [Scénarios de Test Détaillés](test_scenarios.md)
- [Modèle de Rapport](test_report_template.md)
- [Configuration des KPI](kpi_metrics.py)

## 🤝 Contribution

Pour ajouter de nouveaux tests :

1. Créer un nouveau scénario dans `test_scenarios.md`
2. Ajouter les données de test dans `test_data.py`
3. Implémenter le test dans `test_automation.py`
4. Mettre à jour les KPI si nécessaire
5. Tester et documenter

## 📞 Support

Pour toute question sur les tests :
- Créer une issue sur GitHub
- Contacter l'équipe de développement
- Consulter la documentation technique
