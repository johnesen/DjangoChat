from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from chat.models import ChatSendPhoto, Message, Room
from product.models import Product

User = get_user_model()


class ChatSendPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSendPhoto
        fields = ["id", "chat_id", "photo"]


class MessageV2SerialierInner(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "user",
            "message",
            "photo_link",
            "is_read",
            "created_at",
            "current_user",
        ]
        read_only_fields = fields

    current_user = serializers.SerializerMethodField()

    def get_current_user(self, obj) -> bool:
        user = self.context.get("user")
        if user:
            if obj.user and user == obj.user.id:
                return True
            return False


class MessageV2CreateSerializer(serializers.ModelSerializer):
    photo_link = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = ["room", "message", "photo_link"]


class UserInChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "last_active", "photo", "business")
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        is_blocked = self.context.get("is_blocked")
        is_current = self.context.get("is_current")
        data["is_blocked"] = is_blocked
        data["is_current"] = is_current
        if hasattr(instance, "business"):
            data["is_business"] = instance.business.is_active
            data["business"] = (
                instance.business.id if instance.business.is_active else None
            )
            data["business_name"] = (
                instance.business.name if instance.business.is_active else None
            )
        else:
            data["is_business"] = False
            data["business"] = None
            data["business_name"] = None
        return data


class ProductInContactSerializer(serializers.Serializer):
    phone = serializers.CharField(read_only=True)


class ProductPhotoChatSerializer(serializers.Serializer):
    photo = serializers.ImageField(read_only=True)


class ProductInChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "description",
            "photos",
            "currency",
            "initial_price",
            "price_kgs",
            "price_usd",
            "discount_price_kgs",
            "discount_price_usd",
            "discount",
            "contacts",
        )
        read_only_fields = fields

    contacts = ProductInContactSerializer(many=True, read_only=True)
    photos = ProductPhotoChatSerializer(many=True, read_only=True)


class RoomV2CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["reciever", "product"]


class RoomV2ListSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    sender = UserInChatSerializer(read_only=True)
    reciever = UserInChatSerializer(read_only=True)
    product = ProductInChatSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    is_deleted = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = self.context.get("user")
        sender, reciever = instance.sender, instance.reciever
        data["reciever"] = UserInChatSerializer(
            instance.reciever,
            context={
                "is_blocked": True
                if sender and reciever in sender.blocked_users.all()
                else False,
                "is_current": True if reciever and reciever.id == user_id else False,
            },
            read_only=True,
        ).data
        data["sender"] = UserInChatSerializer(
            instance.sender,
            context={
                "is_blocked": True
                if sender and sender in reciever.blocked_users.all()
                else False,
                "is_current": True if sender and sender.id == user_id else False,
            },
            read_only=True,
        ).data
        return data

    def get_last_message(self, instance):
        message = (
            Message.objects.filter(Q(room=instance) & Q(is_deleted=False))
            .order_by("-created_at")
            .first()
        )
        return (
            MessageV2SerialierInner(
                message, context={"user": self.context.get("user")}
            ).data
            if message
            else None
        )

    def get_unread_count(self, instance):
        user_id = self.context.get("user")
        message_cnt = (
            Message.objects.filter(Q(room=instance) & Q(is_read=False))
            .exclude(user_id=user_id)
            .count()
        )
        return message_cnt


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "blocked_users"]
