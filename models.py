from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster = models.URLField()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)