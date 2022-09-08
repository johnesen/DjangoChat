from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class BaseUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, is_superuser, is_staff,
                    is_active, password=None):
        if not email:
            raise ValueError("User must have an email")
        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email=email),
            last_active=now,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, False, True, True, password)

    def create_superuser(self, email, password=None):
        return self._create_user(email, True, True, True, password)