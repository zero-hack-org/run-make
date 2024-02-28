import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    # Default
    DEFAULT_USERNAME = "Unknown"

    # Gender choices
    MAN = "M"
    WOMAN = "W"
    OTHER = "O"
    GENDER_CHOICES = [(MAN, "Man"), (WOMAN, "Woman"), (OTHER, "Other")]

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_("email"), unique=True, max_length=100)
    username = models.CharField(
        _("username"), max_length=30, null=False, blank=False, default=DEFAULT_USERNAME
    )
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER_CHOICES, null=True, blank=False, default=None
    )
    birthday = models.DateField(_("birthday"), null=True, blank=True, default=None)
    body_weight = models.DecimalField(
        _("body weight (kg)"),
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        default=None,
        validators=[validators.MaxValueValidator(999.9), validators.MinValueValidator(0.0)],
    )
    body_height = models.DecimalField(
        _("body height (cm)"),
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        default=None,
        validators=[validators.MaxValueValidator(999.9), validators.MinValueValidator(0.0)],
    )
    is_staff = models.BooleanField(_("is staff"), default=False)
    is_active = models.BooleanField(_("is active"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    created_at = models.DateTimeField(_("created at"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELD = ""

    objects = managers.UserManager()  # type: ignore
