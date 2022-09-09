import coreapi
from rest_framework.schemas.coreapi import AutoSchema
import coreschema


class UserRegisterSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        api_fields = []
        if method == 'POST':
            api_fields = [
                coreapi.Field(name='username', required=True, location='form',
                              schema=coreschema.String(description='str')),
                coreapi.Field(name='email', required=True, location='form',
                              schema=coreschema.String(description='email')),
                coreapi.Field(name='password', required=True, location='form',
                              schema=coreschema.String(description='str')),
                coreapi.Field(name='confirm_password', required=True, location='form',
                              schema=coreschema.String(description='str')),

            ]
        return self._manual_fields + api_fields


class LoginSchema(AutoSchema):
    
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == 'POST':
            api_fields = [
                coreapi.Field(name='email', required=True, location='form',
                              schema=coreschema.String(description='email')),
                coreapi.Field(name='password', required=True, location='form',
                              schema=coreschema.String(description='str')),
            ]
        return self._manual_fields + api_fields