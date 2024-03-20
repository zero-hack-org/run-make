import re
import uuid
from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    # Default
    DEFAULT_USERNAME: ClassVar = "Unknown"

    # Gender choices
    MAN: ClassVar = "M"
    WOMAN: ClassVar = "W"
    OTHER: ClassVar = "O"
    GENDER_CHOICES: ClassVar = [(MAN, "Man"), (WOMAN, "Woman"), (OTHER, "Other")]

    # eng=min(1)
    # num=min(1)
    # available=mark
    # length=min(8)max(14)
    USER_PASSWORD_REGEX: ClassVar = r"^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9!@#$%^&*()-_+=]{8,14}$"

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_("email"), unique=True, max_length=100)
    username = models.CharField(_("username"), max_length=30, null=False, blank=False, default=DEFAULT_USERNAME)
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER_CHOICES, null=True, blank=True, default=None)
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
    is_email_verified = models.BooleanField(_("is email verified"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    created_at = models.DateTimeField(_("created at"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELD = ""

    objects = managers.UserManager()  # type: ignore

    def send_mail(
        self,
        subject: str,
        message: str,
        from_email: str | None = None,
        html_message: str | None = None,
    ) -> None:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL if from_email is None else from_email,
            recipient_list=[self.email],
            html_message=html_message,
        )

    @staticmethod
    def check_password(password: str) -> bool:
        """Check password

        True:Success
        False:Failed
        """
        return False if re.fullmatch(User.USER_PASSWORD_REGEX, password) is None else True
