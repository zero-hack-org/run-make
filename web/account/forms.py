from django.forms import ModelForm

from .models import User


class ResendVerifyEmailForm(ModelForm):
    class Meta:
        model = User
        fields = ["email"]
