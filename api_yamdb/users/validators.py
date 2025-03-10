from django.core.exceptions import ValidationError

from users.constants import DISALLOWED_USERNAME


def validate_username(username):
    if username in DISALLOWED_USERNAME:
        raise ValidationError(
            f'К сожалению имя {username} недоступно.'
        )
