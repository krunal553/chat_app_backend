# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # path("", consumers.ChatConsumer.as_asgi()),
    # re_path(r"(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    # path('<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    re_path(r'^(?P<room_name>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})/$', consumers.ChatConsumer.as_asgi()),
]