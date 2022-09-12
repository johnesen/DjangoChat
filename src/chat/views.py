from rest_framework import generics, exceptions, status, views, viewsets
from .serializers import *
from .models import *
from core import exceptions

class ChatAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
