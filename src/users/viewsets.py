from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from .models import User

class UserAPIViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
