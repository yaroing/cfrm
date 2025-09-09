# Configuration CFRM

# Ceci garantit que Celery est chargé quand Django démarre
from .celery import app as celery_app

__all__ = ('celery_app',)
