from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.constants import (
    MAX_NAME_LENGTH, MAX_SCORE, MIN_SCORE, TEXT_PREVIEW_LENGTH
)
from reviews.validators import validate_year

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
        validators=(validate_year,)
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
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseReviewCommentModel(models.Model):
    """Абстрактная модель для отзыва и комментария."""

    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:TEXT_PREVIEW_LENGTH]


class Review(BaseReviewCommentModel):
    """Модель отзыва."""

    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Произведение'
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
        ordering = ('pub_date',)


class Comment(BaseReviewCommentModel):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('pub_date',)
