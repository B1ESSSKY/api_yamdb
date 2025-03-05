from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.constants import (
    MAX_EMAIL_LENGTH, MAX_ROLE_LENGTH,
    MAX_USERNAME_LENGTH
)
from users.validators import validate_username


class UserRole(models.TextChoices):
    """Пользовательские роли."""

    ADMIN = 'admin', 'Админ'
    MODERATOR = 'moderator', 'Модератор'
    USER = 'user', 'Пользователь'


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_username]
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=MAX_EMAIL_LENGTH,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_ROLE_LENGTH,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        default=''
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} - {self.role}'

    @property
    def is_admin(self):
        """Проверка на роль администратора."""
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка на роль модератора."""
        return self.role == UserRole.MODERATOR
