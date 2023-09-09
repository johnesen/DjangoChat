from django.contrib import admin

from chat.models import ChatSendPhoto, Message, Room

admin.site.register(ChatSendPhoto)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "created_at"]
    fields = [
        "product",
        "sender",
        "reciever",
        "updated_at",
        "created_at",
        "is_deleted",
    ]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "room", "user", "message", "is_read", "created_at"]
