import urllib
from typing import Any
from uuid import UUID

from django.conf import settings
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from . import forms, models, serializers, services


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
        verify_token = services.verify_token.make_token(user)

        # Send verify email
        services.email.send_activation(target_user=user, verify_token=verify_token)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailSuccessView(TemplateView):
    template_name = "account/verify_email_success.html"


class VerifyEmailResendView(TemplateView):
    template_name = "account/verify_email_resend.html"


class VerifyEmailFailedView(TemplateView):
    template_name = "account/verify_other_failed.html"
    extra_context = {
        "support_email_address": settings.SUPPORT_EMAIL_ADDRESS,
        "support_email_address_link": settings.SUPPORT_EMAIL_ADDRESS
        + f"?subject={urllib.parse.quote(settings.SUPPORT_EMAI_DEFAULT_SUBJECT)}"
        + f"&body={urllib.parse.quote(settings.SUPPORT_EMAI_DEFAULT_BODY)}",
    }


class VerifyEmailResendFailedView(TemplateView):
    template_name = "account/verify_other_failed.html"
    extra_context = {
        "support_email_address": settings.SUPPORT_EMAIL_ADDRESS,
        "support_email_address_link": settings.SUPPORT_EMAIL_ADDRESS
        + f"?subject={urllib.parse.quote(settings.SUPPORT_EMAI_DEFAULT_SUBJECT)}"
        + f"&body={urllib.parse.quote(settings.SUPPORT_EMAI_DEFAULT_BODY)}",
    }


class VerifyEmailResendSuccessView(TemplateView):
    template_name = "account/verify_email_resend_success.html"


class VerifyExpiredFailedToResendView(CreateView):
    form_class = forms.ResendVerifyEmailForm
    template_name = "account/verify_expired_failed_to_resend.html"
    extra_context = {
        "support_email_address": settings.SUPPORT_EMAIL_ADDRESS,
        "support_email_address_link": settings.SUPPORT_EMAIL_ADDRESS
        + f"?subject={urllib.parse.quote(settings.SUPPORT_EMAI_DEFAULT_SUBJECT)}"
        + f"&body={urllib.parse.quote(settings.SUPPORT_EMAI_DEFAULT_BODY)}",
    }
    success_url = reverse_lazy("account:verify_email_resend")

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        return self.form_valid(form)

    def form_valid(self, form: forms.ResendVerifyEmailForm) -> HttpResponse:
        email: str = form.data["email"]
        user = models.User.objects.get_or_none(email=email)

        if user is None:
            # Not registered email address
            return redirect("account:verify_email_resend_success")

        token = services.verify_token.make_token(user=user)

        services.email.resend_activation(target_user=user, verify_token=token)
        return redirect("account:verify_email_resend_success")


class VerifyEmailReceiverView(View):
    template_name = "account/verify_email_success.html"

    def get(self, request: HttpRequest, user_id: UUID, token: str) -> HttpResponseRedirect:
        user = models.User.objects.get_or_none(pk=user_id)

        result = services.verify_token.custom_check_token(user=user, token=token)

        # Success Case
        if result.is_success is True:
            return redirect("account:verify_email_success")

        # Failed Case
        if result.error_code == services.VerifyTokenCheckResult.EXPIRED_ERROR_CODE:
            # Expired
            return redirect("account:verify_email_failed_expired_to_resend")
        else:
            # Other
            return redirect("account:verify_email_failed")
