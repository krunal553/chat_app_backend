# users/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # path("", consumers.ChatConsumer.as_asgi()),
    # re_path(r"(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    # path('<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    re_path(r'^(?P<user_id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})/$', consumers.UserConsumer.as_asgi()),
]