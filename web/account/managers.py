# type: ignore


from typing import TypeVar

from django.contrib.auth.models import UserManager as BaseUserManager
from django.db.models.base import Model

_T = TypeVar("_T", bound=Model, covariant=True)


class UserManager(BaseUserManager[_T]):
    def get_or_none(self, **kwargs) -> _T:
        try:
            return self.get_queryset().get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def _create_user(self, email: str, password: str, **extra_fields) -> _T:
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def default_user(self, email: str, password: str) -> _T:
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields) -> _T:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> _T:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_email_verified", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_email_verified") is not True:
            raise ValueError("Superuser must have is_email_verified=True.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
