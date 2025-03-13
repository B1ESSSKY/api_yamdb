from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

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
            raise serializers.ValidationError(
                'Пользователь с таким Email уже существует'
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким ником уже существует'
            )
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user, _ = User.objects.get_or_create(username=username, email=email)
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username]
    )
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            raise serializers.ValidationError('Неверный код')
        return data
