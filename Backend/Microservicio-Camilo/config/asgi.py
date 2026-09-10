"""
ASGI config for the materials microservice.
Expone la variable "application" como un objeto ASGI de un solo llamado.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
