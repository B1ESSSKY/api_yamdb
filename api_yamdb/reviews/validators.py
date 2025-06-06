from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f"Год создания не может быть больше текущего года: {current_year}"
        )
