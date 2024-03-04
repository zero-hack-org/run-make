from rest_framework import serializers

from . import models


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value: str) -> None:
        result = models.User.check_password(value)
        if result is False:
            raise serializers.ValidationError("test")

    def create(self, validated_data: dict) -> models.User:
        user: models.User = models.User.objects.create_user(**validated_data)
        return user
