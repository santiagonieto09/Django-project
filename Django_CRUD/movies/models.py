from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    director = models.CharField(max_length=100)
    release_year = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    age_rating = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100)
    rating = models.FloatField(null=True)
    image_url = models.URLField()
    trailer_url = models.URLField()
    users = models.ManyToManyField(User, through='UserMovieRating')

    def __str__(self):
        return self.title

class UserMovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True) 

    class Meta:
        unique_together = ('user', 'movie')


