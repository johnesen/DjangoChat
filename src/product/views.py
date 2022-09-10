from rest_framework.response import Response
from rest_framework import viewsets, generics, permissions, status, exceptions
from rest_framework.views import APIView
from .schemas import ProductSchemas
from .serializers import ProductSerializer
from .services import ProductService

class CreateProduct(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    schema = ProductSchemas()

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = ProductService.create_product(
                                        user=serializer.validated_data.get('user'),
                                        title=serializer.validated_data.get('title'),
                                        description=serializer.validated_data.get('description'),
                                        currency=serializer.validated_data.get('currency'),
                                        price=serializer.validated_data.get('price'),
                                        discount=serializer.validated_data.get('discount'),
            )
        except Exception:
            raise exceptions.ValidationError()
        return Response(data={
            'message': 'Product created successfully :)',
            'status': 'CREATED',
        }, status=status.HTTP_201_CREATED)
