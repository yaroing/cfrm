import os
from celery import Celery

# Configuration de l'environnement Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfrm.settings')

app = Celery('cfrm')

# Configuration de Celery à partir des paramètres Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tâches dans toutes les applications Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



