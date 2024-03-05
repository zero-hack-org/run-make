from uuid import UUID

from django.db import transaction
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from . import models, serializers, services


class SignUpView(CreateAPIView):
    "Create user account and send verify email"
    permission_classes = [AllowAny]
    serializer_class = serializers.SignUpSerializer

    @transaction.atomic
    def post(self, request: Request) -> Response:

        # Create user temp register
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Token
        token_service = services.VerifyTokenService()
        verify_token = token_service.make_token(user)

        # Send verify email
        email_service = services.EmailService()
        email_service.send_activation(target_user=user, verify_token=verify_token)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailView(TemplateView):
    template_name = "account/verify_email_success.html"

    _user_id = "user_id"
    _token = "token"

    _expired_error_template_name = "account/verify_expired_token_error.html"
    _other_error_template_name = "account/verify_other_error.html"

    def get_template_names(self) -> list[str]:
        user_id: UUID = self.kwargs.get(self._user_id)
        verify_token: str = self.kwargs.get(self._token)

        user = models.User.objects.get(pk=user_id)

        token_service = services.VerifyTokenService()
        result = token_service.custom_check_token(user=user, token=verify_token, limit=11)

        # Success Case
        if result.is_success is True:
            return [self.template_name]

        # Failed Case
        if result.error_code == services.VerifyTokenCheckResult.EXPIRED_ERROR_CODE:
            # Expired
            return [self._expired_error_template_name]
        else:
            # Other
            return [self._other_error_template_name]
