from .models import Product
from core.exceptions import *
from core.validators import validate_user_password

class ProductService:
    model = Product

    @classmethod
    def get(cls, **filters) -> Product:
        return cls.model.objects.get(**filters)

    @classmethod
    def get_all(cls) -> Product:
        return cls.model.objects.all()

    @classmethod
    def get_product(cls, **filters) -> Product:
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Product not found')

    @classmethod
    def filter_user(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def create_product(
                    cls, 
                    user,
                    title,
                    description,
                    currency,
                    price,
                    discount,
                    **kwargs
                    ) -> Product:
        product = cls.model(
                        user=user,
                        title=title,
                        description=description,
                        currency=currency,
                        price=price,
                        discount=discount,
                        **kwargs
                        )
        product.save()
        return product