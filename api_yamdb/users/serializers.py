from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
from users.validators import validate_username

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)


class UserCreationSerializer(serializers.Serializer):
    """Сериализатор для создания нового пользователя."""
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username]
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(email=email, username=username).exists():
            return data

        if User.objects.filter(email=email).exists():
            return ValidationError(
                'Пользователь с таким Email уже существует'
            )

        if User.objects.filter(username=username).exists():
            return ValidationError(
                'Пользователь с таким ником уже существует'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username]
    )
    confirmation_code = serializers.CharField()
