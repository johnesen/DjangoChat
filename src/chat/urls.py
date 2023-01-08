from django.urls import path, include
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()

router.register('', views.ChatAPIView, 'chat')

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('room/', views.rooms, name='rooms'),
    path('room/<str:id>/', views.room, name='room'),
]