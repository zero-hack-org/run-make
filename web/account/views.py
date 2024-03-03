from django.db import transaction
from django.views.generic.base import TemplateView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from . import serializers, services


class SignUpView(CreateAPIView):
    "Create user account and send verify email."
    permission_classes = [AllowAny]
    serializer_class = serializers.SignUpSerializer

    @transaction.atomic
    def post(self, request: Request) -> Response:

        # Create user temp register
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Token
        generator = services.VerifyTokenService()
        verify_token = generator.make_token(user)

        # Send verify email
        email_service = services.EmailService()
        email_service.send_activation(target_user=user, verify_token=verify_token)
        raise ValueError("test")
        return Response(serializer.data)


class VerifyEmailView(TemplateView):
    template_name = "verify_email.html"
