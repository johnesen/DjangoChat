from django.urls import path

from chat import consumers

websocket_urlpatterns = [
    path("ws/<int:userId>/", consumers.RoomListConsumers.as_asgi()),
    path("ws/<int:userId>/<str:roomId>/", consumers.ChatConsumer.as_asgi()),
]
