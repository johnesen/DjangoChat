import os
from django.utils.translation import gettext_lazy as _
from core.utils import get_filename

PHOTO_UPLOAD_DIR = 'products/photo'

class CurrencyType:
    USD = 'USD'
    KGS = 'KGS'

    @classmethod
    def choices(cls):
        return (
            (cls.USD, cls.USD),
            (cls.KGS, cls.KGS)
        )

    @classmethod
    def all(cls):
        return cls.USD, cls.KGS


class ProductState:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'
    BLOCKED = 'blocked'
    ON_REVIEW = 'on_review'

    @classmethod
    def choices(cls):
        return (
            (cls.ACTIVE, _(cls.ACTIVE)),
            (cls.INACTIVE, _(cls.INACTIVE)),
            (cls.DELETED, _(cls.DELETED)),
            (cls.BLOCKED, _(cls.BLOCKED)),
            (cls.ON_REVIEW, _('on review'))
        )


def photo_upload_to(instance, filename):
    new_filename = get_filename(filename)
    return os.path.join(PHOTO_UPLOAD_DIR, new_filename)