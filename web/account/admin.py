from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_("Authentications"), {"fields": ("email", "password")}),
        (
            _("Profiles"),
            {"fields": ("username", "gender", "birthday", "body_weight", "body_height")},
        ),
        (
            _("Authorities"),
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_email_verified",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Others"),
            {
                "fields": (
                    "last_login",
                    "created_at",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("id", "email", "created_at")
    list_filter = (
        "is_staff",
        "is_active",
        "is_email_verified",
    )
    search_fields = ("id", "email")
    ordering = ("-created_at",)
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
