from django.db import models

# Create your models here.

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=20)
    date = models.DateField()

class Guest(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservations')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reservations')
