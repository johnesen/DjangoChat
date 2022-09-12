from django.urls import path, include
from .views import CreateProduct


urlpatterns = [
    path('v1', CreateProduct.as_view(), name='create-product'),
]
