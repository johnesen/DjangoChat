from attr import fields
import coreapi
from rest_framework.schemas.coreapi import AutoSchema
import coreschema


class ProductSchemas(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == 'POST':
            api_fields = [
                coreapi.Field(name='user', required=True, location='form',
                    schema=coreschema.String(description='int')),
                coreapi.Field(name='title', required=True, location='form',
                    schema=coreschema.String(description='str')),
                coreapi.Field(name='description', required=True, location='form',
                    schema=coreschema.String(description='str')),
                coreapi.Field(name='currency', required=True, location='form',
                    schema=coreschema.String(description='str')),
                coreapi.Field(name='price', required=True, location='form',
                    schema=coreschema.Integer(description='int')),
                coreapi.Field(name='discount', required=False, location='form',
                    schema=coreschema.Integer(description='int')),
            ]
        return self._manual_fields + api_fields


