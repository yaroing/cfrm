"""
WSGI config for cfrm project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfrm.settings')

application = get_wsgi_application()
