from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin
    )
from copy import deepcopy
from core.utils import compress_image
from .utils import upload_user_photo_to
from django.utils.translation import gettext_lazy as _
from core.base_model import BaseModel
from .managers import BaseUserManager



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=150, blank=True, null=True, unique=True, verbose_name=_('username'))
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name=_('E-Mail'))
    photo = models.ImageField(upload_to=upload_user_photo_to, null=True, blank=True, verbose_name=_('photo'))
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('password'))
    is_superuser = models.BooleanField(default=False, blank=True, verbose_name=_('admin-user'))
    is_staff = models.BooleanField(default=False, blank=True, verbose_name=_('staff'))
    is_active = models.BooleanField(default=False, blank=True, verbose_name=_('active'))
    last_active = models.DateTimeField(blank=True, null=True, verbose_name=_('last login'))

    USERNAME_FIELD = 'email'

    objects = BaseUserManager()

    def __str__(self):
        return self.email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo_ = deepcopy(self.photo)

    def save(self, *args, **kwargs):
        if self.photo and self.photo != self.photo_:
            self.photo = compress_image(self.photo, is_medium_thumbnail=True, quality=80)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        # ordering = ('-created_at',)
# 