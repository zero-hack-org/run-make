from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("api/v1/signup", view=views.SignUpView.as_view(), name="signup"),
    path(
        "verify_email/<uuid:user_id>/<str:token>",
        view=views.VerifyEmailReceiverView.as_view(),
        name="verify_email_receiver",
    ),
    path(
        "verify_email_success",
        view=views.VerifyEmailSuccessView.as_view(),
        name="verify_email_success",
    ),
    path(
        "verify_email_failed",
        view=views.VerifyEmailFailedView.as_view(),
        name="verify_email_failed",
    ),
    path(
        "verify_email_expired_to_resend",
        view=views.VerifyExpiredFailedToResendView.as_view(),
        name="verify_email_failed_expired_to_resend",
    ),
    path(
        "verify_email_resend",
        view=views.VerifyEmailResendView.as_view(),
        name="verify_email_resend",
    ),
    path(
        "verify_email_resend_success",
        view=views.VerifyEmailResendSuccessView.as_view(),
        name="verify_email_resend_success",
    ),
    path(
        "verify_email_resend_failed",
        view=views.VerifyEmailResendFailedView.as_view(),
        name="verify_email_resend_failed",
    ),
]
