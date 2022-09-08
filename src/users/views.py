from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .services import UserService, JWTTokenService

class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.create_profile_student(username=serializer.validated_data.get('username'),
                                                     email=serializer.validated_data.get('email'),
                                                     password=serializer.validated_data.get('password'),
                                                     conf_password=serializer.validated_data.get('confirm_password'),
        )
        return Response(data={
            'message': 'The user has successfully registered and the profile has been successfully created',
            'status': 'CREATED'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
        Login for user.
    """
    permission_classes = (AllowAny,)

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


class UserAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        instance = UserService.get()
        serializer_class = self.get_serializer()
        serializer = serializer_class(instance, many=False)
        return Response(data={
            'message': 'User profile has been successfully found',
            'data': serializer.data,
            'status': 'OK'
        }, status=status.HTTP_200_OK)

    def retrieve(self, user_id, request, *args, **kwargs):
        serializer_class = self.get_serializer()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data, user_data = UserService.check_user(**serializer.validated_data)
        UserService.get_user(user=user_id, **validated_data, **user_data)
        return Response(data={
            'message': 'The profile has been successfully retrieved',
            'status': 'OK'
        }, status=status.HTTP_200_OK)