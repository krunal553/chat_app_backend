from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # path('routes/', views.get_routes, name="get-routes"),
    path('', views.get_user_profiles, name="get-users"),
    path('user/', views.get_user_profile, name="get-user-profile"),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]