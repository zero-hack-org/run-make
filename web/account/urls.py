from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/signup", view=views.SignUpView.as_view(), name="signup"),
    path(
        "verify/email/<uuid:user_id>/<str:token>",
        view=views.VerifyEmailView.as_view(),
        name="verify_email",
    ),
]
