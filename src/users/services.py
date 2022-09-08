from django.contrib.auth import get_user_model
from core.exceptions import *
from core.validators import validate_user_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from typing import Tuple, List


User = get_user_model()


class JWTTokenService:
    model = RefreshToken

    @classmethod
    def create_auth_token(cls, email: str, password: str):
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return user, refresh
        else:
            raise ObjectNotFoundException('User not found or not active')

    @classmethod
    def destroy_auth_token(cls, user: User) -> None:
        return cls.model.objects.filter(user=user).delete()



class UserService:
    model = User

    @classmethod
    def get(cls, **filters) -> User:
        return cls.model.objects.filter(**filters)

    @classmethod
    def get_user(cls, **filters) -> User:
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('User not found')

    @classmethod
    def filter_user(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def exclude_user(cls, **filters):
        return cls.model.objects.exclude(**filters)

    @classmethod
    def check_user(cls, **filters) -> tuple:
        default_user = {'email': '', 'username': ''}
        if filters.get('user'):
            default_user = filters.pop('user')
        return filters, default_user

    @classmethod
    def create_user(cls, username: str, email: str, password: str, conf_password: str, **kwargs) -> User:
        user = cls.model(username=username, email=email, **kwargs)
        correct_password = validate_user_password(password=password, conf_password=conf_password)
        user.set_password(correct_password)
        user.save()
        return user