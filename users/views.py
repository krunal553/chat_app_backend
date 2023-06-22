from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile, User
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.db.models import Q

@api_view(['GET'])
def get_routes(request):
    routes = [
        'token/',
        'token/refresh/',
    ]
    return Response(routes)

class RetrieveUserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'

class UserSearchAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ['name', 'username']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('query', '')
        terms = query.split()  # Split query into individual terms
        if terms:
            q_objects = Q()  # Create an empty Q object to combine search conditions
            for term in terms:
                q_objects |= Q(name__icontains=term) | Q(username__icontains=term)
            queryset = queryset.filter(q_objects)
        else:
            queryset = queryset.none()  # Return an empty queryset
        return queryset

# authentication and authorization

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['profile_pic'] = UserProfileSerializer(
            UserProfile.objects.get(username=user.username), many=False
            ).data['profile_pic']
        # ...
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    