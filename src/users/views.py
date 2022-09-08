from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer,RegistrationSerializer
from .services import UserService, JWTTokenService

User = get_user_model()
class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.create_user(
                                email=serializer.validated_data.get('email'),
                                password=serializer.validated_data.get('password'),
                                conf_password=serializer.validated_data.get('confirm_password'),
        )
        #username=serializer.validated_data.get('username'),
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


class UserAPIView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


def get_login_response(user, request):
    refresh = RefreshToken.for_user(user)
    data = {
        "user": UserSerializer(instance=user, context={'request': request}).data,
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
    return data



class RegistrationAPIView(generics.GenericAPIView):
    """
        APIViews for signUp
    """

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        user_data = serializers.data
        user = User.objects.get(email=user_data['email'])
        # user.provider = Provider.EMAIL
        user.save()
        return Response(data=get_login_response(user, request), status=status.HTTP_201_CREATED)
