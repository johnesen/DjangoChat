import datetime
import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_q.tasks import async_task

from chat import jobs
from chat.models import Message, Room
from chat.serializers import MessageV2SerialierInner, RoomV2ListSerializer

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["roomId"]
        self.user_id = self.scope["url_route"]["kwargs"]["userId"]
        self.channel_layer = get_channel_layer()
        self.room_group_name = "chat_%s" % self.room_id

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.getResponse()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def isJsonable(self, jsonData):
        try:
            json.loads(jsonData)
        except ValueError as err:
            return False
        return True

    async def receive(self, text_data):
        if self.isJsonable(jsonData=text_data):
            data = json.loads(text_data)
            message = data.get("message")
            if not message:
                await self.getResponse()
                return
            await self.save_message(room=self.room_id, user=self.user_id, **data)

        await self.getResponse()
        await self.get_room_query(self.room_id)

    async def chatMessage(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "count": len(await self.getMesssages()),
                    "undread": await self.getUnreadMesssagesCount(),
                    "messages": await self.getMesssages(),
                    "room": await self.get_room(self.room_id),
                }
            )
        )

    async def getResponse(self):
        return await self.channel_layer.group_send(
            self.room_group_name, {"type": "chatMessage"}
        )

    @sync_to_async
    def getMesssages(self):
        queryset = Message.objects.filter(
            Q(room_id=self.room_id) & Q(is_deleted=False)
        ).order_by("-created_at")

        queryset.exclude(Q(is_deleted=True) | Q(user=self.user_id)).update(is_read=True)

        return MessageV2SerialierInner(
            queryset, context={"user": self.user_id}, many=True
        ).data

    @sync_to_async
    def getUnreadMesssagesCount(self):
        queryset = Message.objects.filter(room_id=self.room_id, is_read=False).exclude(
            user_id=self.user_id
        )
        return queryset.count()

    @sync_to_async
    def save_message(self, **kwargs):
        message = Message.objects.create(
            room_id=kwargs.get("room"),
            message=kwargs.get("message"),
            user_id=kwargs.get("user"),
            photo_link=kwargs.get("photo_link"),
        )
        message.room.updated_at = datetime.datetime.now()
        message.room.save()
        reciever = (
            message.room.sender
            if message.user == message.room.reciever
            else message.room.reciever
        )
        async_task(
            jobs.new_message,
            message.user,
            reciever,
            message.room.product,
            message.message,
            message.room.id,
            task_name="chat-new-message",
        )
        return message

    @sync_to_async
    def get_room(self, room_id):
        my_room = Room.objects.filter(id=room_id).first()
        return RoomV2ListSerializer(my_room, context={"user": self.user_id}).data

    @sync_to_async
    def get_room_query(self, room_id):
        room = Room.objects.filter(id=room_id)
        user_ids = [room.first().sender.id, room.first().reciever.id]
        for user_id in user_ids:
            if self.user_id != user_id:
                my_rooms = (
                    Room.objects.filter(Q(sender_id=user_id) | Q(reciever_id=user_id))
                    .exclude(is_deleted=True)
                    .order_by("updated_at")
                )
                async_to_sync(self.channel_layer.group_send)(
                    f"chat_user_{user_id}",
                    {
                        "type": "send_user_id",
                        "rooms": RoomV2ListSerializer(
                            my_rooms, many=True, context={"user": user_id}
                        ).data,
                    },
                )


class RoomListConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["userId"]
        self.room_group_name = "chat_user_%s" % self.user_id

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.getResponse()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        await self.getResponse()

    async def send_user_id(self, event):
        rooms = event.get("rooms")
        await self.send(text_data=json.dumps({"count": len(rooms), "rooms": rooms}))

    async def getResponse(self):
        return await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "send_user_id", "rooms": await self.get_room(self.user_id)},
        )

    @sync_to_async
    def get_room(self, user):
        user_queryset = User.objects.filter(id=user).first()

        my_rooms = (
            Room.objects.filter(
                Q(sender_id=user_queryset.id) | Q(reciever_id=user_queryset.id)
            )
            .exclude(is_deleted=True)
            .order_by("-updated_at")
        )
        return RoomV2ListSerializer(my_rooms, many=True, context={"user": user}).data
