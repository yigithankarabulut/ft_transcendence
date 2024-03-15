import os

from .routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notificationservice.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": (
            URLRouter(websocket_urlpatterns)
        )
    }
)
