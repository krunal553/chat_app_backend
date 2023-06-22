import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .routing import websocket_routes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app_backend.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_routes
        ),
    ),
})
