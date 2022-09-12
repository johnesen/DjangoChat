from rest_framework import serializers as s
from .models import *
from users.serializers import UserSerializer


class MessageSerializer(s.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'user', 'message', 'created_at']

class RoomSerializer(s.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)
    class Meta:
        model = Room
        fields = ['id', 'slug', 'name', 'messages', 'created_at']

