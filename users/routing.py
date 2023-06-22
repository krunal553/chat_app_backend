# users/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^(?P<user_id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})/$', consumers.UserConsumer.as_asgi()),
]

# ws://127.0.0.1:8080/ws/user/id/