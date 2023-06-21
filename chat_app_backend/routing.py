from django.urls import path
from channels.routing import  URLRouter

from chat.routing import websocket_urlpatterns as chat_ws_urlpatterns
from users.routing import websocket_urlpatterns as user_ws_urlpatterns

websocket_routes = [
    path("ws/chat/", URLRouter(chat_ws_urlpatterns)),
    path("ws/user/", URLRouter(user_ws_urlpatterns)),
]