"""
Configuration de test pour CFRM
"""
from .settings import *
import tempfile
import os

# Base de données de test
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Cache de test
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Désactiver les migrations pour les tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Configuration de test
DEBUG = False
SECRET_KEY = 'test-secret-key'
ALLOWED_HOSTS = ['testserver']

# Désactiver les logs pendant les tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
}

# Désactiver les middlewares de sécurité pour les tests
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Configuration des tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Désactiver les validations de mot de passe
AUTH_PASSWORD_VALIDATORS = []

# Configuration des tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Désactiver les tâches asynchrones
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
