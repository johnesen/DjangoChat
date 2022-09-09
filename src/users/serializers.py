from collections import OrderedDict
from pyexpat import model
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, required=True, validators=[
        UniqueValidator(
            queryset=User.objects.all()
        )])
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
