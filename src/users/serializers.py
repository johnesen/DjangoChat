from collections import OrderedDict
from pyexpat import model
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class PasswordField(serializers.CharField):
    """
        Just password create passowrd field
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class RegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer for registration user
    """

    password = PasswordField(required=True, allow_blank=False, allow_null=False, min_length=8)
    password2 = PasswordField(required=True, allow_blank=False, allow_null=False, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        account = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Password must much'}
            )
        account.set_password(password)
        account.save()
        return account


class RegisterSerializer(serializers.Serializer):
    # username = serializers.CharField(min_length=2, required=True, validators=[
    #     UniqueValidator(
    #         queryset=User.objects.all()
    #     )])
    email = serializers.EmailField(min_length=2, required=True, validators=[
        UniqueValidator(
            queryset=User.objects.all()
        )])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, required=True)
    password = serializers.CharField(min_length=8, max_length=20, required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                  'id',
                  'username',
                  'email',
                  'photo',
                  'last_active',
                  'created_at',
                  'updated_at',
                ]
