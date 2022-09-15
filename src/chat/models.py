from django.contrib.auth import get_user_model
from django.db import models
from core.base_model import BaseModel


User = get_user_model()
class Room(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class Message(BaseModel):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()

    class Meta:
        ordering = ('created_at',)