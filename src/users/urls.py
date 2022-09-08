from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserAPIView, 'user')

urlpatterns = [
    path('login', views.LoginAPIView.as_view(), name='login'),
    path('register', views.RegisterAPIView.as_view(), name='register'),
    path('v1/', include(router.urls), name='user'),
    path('gg', views.RegistrationAPIView.as_view(), name='users'),
    
# RegistrationAPIView
]
