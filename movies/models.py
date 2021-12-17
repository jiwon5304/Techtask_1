from typing import Text
from django.db   import models

from core.models import TimeStamp
from users.models   import User


class Movie(models.Model):
    movies_id    = models.IntegerField()
    title        = models.CharField(max_length=128)
    year         = models.IntegerField()
    rating       = models.DecimalField(max_digits=3, decimal_places=1)
    genres       = models.CharField(max_length=128)
    summary      = models.TextField()

    class Meta:
        db_table = "movies"


class Review(TimeStamp):
    user         = models.ForeignKey(User, on_delete = models.CASCADE)
    movie        = models.ForeignKey(Movie, on_delete = models.CASCADE)
    text         = models.TextField()
    rating       = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        db_table = "reviews"


class Recommend(models.Model):
    user         = models.ForeignKey(User, on_delete = models.CASCADE)
    review       = models.ForeignKey(Review, on_delete = models.CASCADE)

    class Meta:
        db_table = "recommends"


