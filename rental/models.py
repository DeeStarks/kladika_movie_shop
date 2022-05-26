from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie

# Create your models here.
class RentMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username + ' - ' + self.movie.title

class MaxRent(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)