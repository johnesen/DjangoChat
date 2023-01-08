from rest_framework import generics, exceptions, status, views, viewsets
from .serializers import *
from .models import *
from core import exceptions
from django.shortcuts import  render
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Room, Message

class ChatAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

def frontpage(request):
    return render(request, 'chat/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('chat/frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'chat/signup.html', {'form': form})

def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'chat/rooms.html', {'rooms': rooms})

def room(request, id):
    room = Room.objects.get(id=id)
    messages = Message.objects.filter(room=room)

    return render(request, 'chat/room.html', {'room': room, 'messages': messages})