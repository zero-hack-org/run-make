from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int

from . import models


class EmailService:
    common_context = {
        "application_name": settings.APPLICATION_NAME,
        "support_email_address": settings.SUPPORT_EMAIL_ADDRESS,
    }

    def send_activation(self, target_user: models.User, verify_token: str) -> None:
        subject = f"仮登録完了のお知らせ[{settings.APPLICATION_NAME}]"
        message_template_name = "account/emails/activation_by_email.txt"
        context = {
            "verify_url": f"{settings.EMAIL_VERIFY_END_POINT}/{target_user.id}/{verify_token}"
        }
        target_user.send_mail(
            subject=subject,
            message=render_to_string(
                template_name=message_template_name, context={**self.common_context, **context}
            ),
        )


class VerifyTokenService(PasswordResetTokenGenerator):
    """
    Verify token generator
    override check_token() available limit second.
    """

    def check_token(
        self, user: AbstractBaseUser | None, token: str | None, limit: int = 60 * 60 * 24 * 3
    ) -> bool:
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                break
        else:
            return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > limit:
            return False

        return True
