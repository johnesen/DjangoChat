from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_('удалить'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('дата изменения'))

    class Meta:
        abstract = True
