from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension
from django.db import models


class Wish(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=50, default='', blank=True)
    image = models.ImageField(
        upload_to='img/',
        default='img/wish_default.jpg',
        blank=True,
        validators=[validate_image_file_extension]
    )
    description = models.CharField(max_length=500, default='', blank=True)
    type = models.CharField(max_length=50, default='Разное', blank=True)

    def __str__(self):
        return self.title
