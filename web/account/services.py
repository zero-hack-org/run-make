from dataclasses import dataclass
from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int

from . import models


@dataclass
class VerifyTokenCheckResult:
    EXPIRED_ERROR_CODE: ClassVar = 1
    OTHER_ERROR_CODE: ClassVar = 9

    is_success: bool

    # error_code=None: Success
    # error_code=1: Expired
    # error_code=9: Other
    error_code: int | None

    @staticmethod
    def get_success() -> "VerifyTokenCheckResult":
        return VerifyTokenCheckResult(True, None)

    @staticmethod
    def get_expired_error() -> "VerifyTokenCheckResult":
        return VerifyTokenCheckResult(False, VerifyTokenCheckResult.EXPIRED_ERROR_CODE)

    @staticmethod
    def get_other_error() -> "VerifyTokenCheckResult":
        return VerifyTokenCheckResult(False, VerifyTokenCheckResult.OTHER_ERROR_CODE)


class EmailService:
    common_context = {
        "application_name": settings.APPLICATION_NAME,
        "support_email_address": settings.SUPPORT_EMAIL_ADDRESS,
    }

    def send_activation(self, target_user: models.User, verify_token: str) -> None:
        subject = f"仮登録完了のお知らせ[{settings.APPLICATION_NAME}]"
        message_template_name = "email/activation_by_email.txt"
        context = {"verify_url": f"{settings.EMAIL_VERIFY_END_POINT}/{target_user.id}/{verify_token}"}
        target_user.send_mail(
            subject=subject,
            message=render_to_string(template_name=message_template_name, context={**self.common_context, **context}),
        )

    def resend_activation(self, target_user: models.User, verify_token: str) -> None:
        subject = f"登録完了URLの再送[{settings.APPLICATION_NAME}]"
        message_template_name = "email/activation_by_email_resend.txt"
        context = {"verify_url": f"{settings.EMAIL_VERIFY_END_POINT}/{target_user.id}/{verify_token}"}
        target_user.send_mail(
            subject=subject,
            message=render_to_string(template_name=message_template_name, context={**self.common_context, **context}),
        )


class VerifyTokenService(PasswordResetTokenGenerator):
    """
    Verify token generator
    override check_token() available limit second and type
    """

    def custom_check_token(
        self, user: AbstractBaseUser | None, token: str | None, limit: int = 60 * 60 * 24
    ) -> VerifyTokenCheckResult:
        if not (user and token):
            return VerifyTokenCheckResult.get_other_error()
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return VerifyTokenCheckResult.get_other_error()

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return VerifyTokenCheckResult.get_other_error()

        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                break
        else:
            return VerifyTokenCheckResult.get_other_error()

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > limit:
            return VerifyTokenCheckResult.get_expired_error()

        return VerifyTokenCheckResult.get_success()


email = EmailService()
verify_token = VerifyTokenService()
