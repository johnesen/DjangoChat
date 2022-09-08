from pyexpat import model
from rest_framework import serializers
from .models import Product, ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('id', 'photo')

class ProductSerializer(serializers.ModelSerializer):
    photos = ProductPhotoSerializer()
    class Meta:
        model = Product
        fields = [
                  'id', 
                  'title',
                  'description',
                  'currency',
                  'price',
                  'state',
                  'rating',
                  'discount'
                ]