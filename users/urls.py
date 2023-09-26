from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # path('routes/', views.get_routes, name="get-routes"),
    # path('<uuid:id>/', views.RetrieveUserAPIView.as_view(), name='user-profile'),
    path('<uuid:pk>/', views.UserProfileAPIView.as_view(), name='user-profile'),
    path('search/', views.UserSearchAPIView.as_view(), name='user-search'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]