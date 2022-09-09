from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .schema import UserRegisterSchema, LoginSchema
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .services import UserService, JWTTokenService

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    schema = UserRegisterSchema()

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.create_user(
                                username=serializer.validated_data.get('username'),
                                email=serializer.validated_data.get('email'),
                                password=serializer.validated_data.get('password'),
                                conf_password=serializer.validated_data.get('confirm_password'),
        )
        return Response(data={
            'message': 'The user has successfully registered and the profile has been successfully created',
            'status': 'CREATED'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    schema = LoginSchema()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = JWTTokenService.create_auth_token(
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password')
        )
        return Response(data={
            'message': 'You have successfully logged in',
            'data': {
                'access': str(token.access_token),
                'refresh': str(token),
                'token_type': 'Bearer',
                'user': user.pk
            },
            'status': "OK"
        }, status=status.HTTP_200_OK)
