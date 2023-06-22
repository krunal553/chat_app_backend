# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^(?P<room_name>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})/$', consumers.ChatConsumer.as_asgi()),
]

# ws://127.0.0.1:8080/ws/chat/thrad_id/