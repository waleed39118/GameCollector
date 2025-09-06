from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self) -> str:
        return self.name

class Game(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)
    genre = models.CharField(max_length=60)
    platform = models.CharField(max_length=60)
    release_date = models.DateField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self) -> str:
        return f"{self.name} ({self.platform})"