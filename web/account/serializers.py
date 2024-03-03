from rest_framework import serializers

from . import models


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> models.User:
        user: models.User = models.User.objects.default_user(**validated_data)
        return user
