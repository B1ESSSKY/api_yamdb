from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
