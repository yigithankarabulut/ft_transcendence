"""
ASGI config for statusservice project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from .routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'statusservice.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": (
            URLRouter(websocket_urlpatterns)
        )
    }
)
