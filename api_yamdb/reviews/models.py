from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.constants import MAX_NAME_LENGTH, MIN_YEAR

User = get_user_model()


class NameSlugModel(models.Model):
    """Базовая модель для категории и жанров."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Наименование'
    )
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(NameSlugModel):
    """Модель жанров."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(NameSlugModel):
    """Модель категорий."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        verbose_name='Название', max_length=MAX_NAME_LENGTH
    )
    year = models.SmallIntegerField(
        verbose_name='Год создания',
        validators=(
            MinValueValidator(MIN_YEAR),
            MaxValueValidator(timezone.now().year)
        )
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""

    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        default_related_name = 'reviews'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель комментария к отзыву."""

    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:15]
