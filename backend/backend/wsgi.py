"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/opt/render/project/src/backend')

print("Python Path:", sys.path)
print("DJANGO_SETTINGS_MODULE:", os.getenv('DJANGO_SETTINGS_MODULE'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
