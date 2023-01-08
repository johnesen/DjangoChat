import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework import exceptions
from asgiref.sync import sync_to_async
from django.db.models import Q

from .models import Room, Message


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["id"]
        self.room_group_name = "chat_%s" % self.room_id

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user = data["user"]
        room = data["room"]

        photo_link = data["photo_link"]

        message_queryset = await self.save_message(room, message, user, photo_link)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user,
                "room": room,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        room = event["room"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "user": user,
                    "room": room,
                }
            )
        )

    @sync_to_async
    def save_message(self, room, message, user, photo_link=None):
        try:
            return Message.objects.create(
                room_id=room, message=message, user_id=user, photo_link=photo_link
            )
        except:
            raise exceptions.AuthenticationFailed
