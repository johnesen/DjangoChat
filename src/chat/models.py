import uuid

from django.contrib.auth import get_user_model
from django.db import models

from core.base_model import BaseModel

User = get_user_model()


class Room(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    sender = models.ForeignKey(
        "users.User",
        related_name="room_sender",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reciever = models.ForeignKey(
        "users.User",
        related_name="room_reciever",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        "product.Product",
        related_name="messages_room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "users.User",
        related_name="messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    message = models.TextField(null=True, blank=True)
    photo_link = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
