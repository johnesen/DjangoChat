from copy import deepcopy
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.utils import compress_image
from .utils import CurrencyType, ProductState
from core.base_model import BaseModel
from .utils import photo_upload_to


class Rate(BaseModel):
    class Meta:
        db_table = 'rate'

    currency = models.CharField(_('title'), max_length=5, choices=CurrencyType.choices(),
                                null=False, unique=True)
    rate = models.DecimalField(_('rate'), null=False, max_digits=20, decimal_places=2, default=0)
    last_update = models.DateTimeField(_('last update time'), auto_now=True)

    def __str__(self):
        return str(self.currency)


class Product(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='products',
                             null=False, verbose_name=_('user'))
    title = models.CharField(max_length=50, null=False, db_index=True, verbose_name=_('title'))
    description = models.TextField(null=False, verbose_name=_('description'))
    currency = models.CharField(max_length=5, choices=CurrencyType.choices(), null=False,
                                verbose_name=_('currency'))
    price = models.DecimalField(null=False, max_digits=20, decimal_places=2,
                                        verbose_name=_('price'))
    state = models.CharField(choices=ProductState.choices(), null=False, default=ProductState.ON_REVIEW,
                             max_length=20, verbose_name=_('state'))
    rating = models.PositiveSmallIntegerField(null=True, verbose_name=_('rating'))
    discount = models.IntegerField(null=True, blank=True, verbose_name=_("discount"))

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'product'
        ordering = ('-id',)

class ProductPhoto(models.Model):
    product = models.ForeignKey('Product', related_name='photos', null=False, on_delete=models.CASCADE,
                                verbose_name=_('product'))
    photo = models.ImageField(null=False, upload_to=photo_upload_to, verbose_name=_('photo'), )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo_ = deepcopy(self.photo)

    def save(self, *args, **kwargs):
        if self.photo and self.photo != self.photo_:
            self.photo = compress_image(self.photo, is_medium_thumbnail=True, quality=100)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'product_photo'
