from django.urls import path, include
from . import views

urlpatterns = [
    path('routes/', views.get_routes, name="get_routes"),
    path('messages/', views.MessageAPIView.as_view(), name="messages"),
    path('messages/<uuid:pk>', views.MessageAPIView.as_view(), name="messages"),
    path('threads/', views.ThreadAPIView.as_view(), name="thread"),
]