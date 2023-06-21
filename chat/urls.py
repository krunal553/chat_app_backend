from django.urls import path, include
from . import views

urlpatterns = [
    path('routes/', views.get_routes, name="get_routes"),
    path('create-thread/', views.get_or_create_thread, name="create-thread"),
    path('create-message/', views.create_message, name="create-message"),
    path('<str:username>/read-messages/', views.read_messages, name="read-messages"),
    path('<str:username>/delete-messages/', views.delete_messages, name="delete-messages"),
    path('chatlist/', views.get_user_threads, name="chatlist"),

    # path('get-all-messages/', views.get_all_messages, name="get-all-messages"),

]

    # path('get-messages/', views.get_messages, name="get-messages"),
    # path('get-all-threads/', views.get_all_threads, name="get-all-threads"),