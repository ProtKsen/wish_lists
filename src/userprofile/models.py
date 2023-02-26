from django.db import models


class Wish(models.Model):
    username = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='img/', default='default.jpg', blank=True)
    description = models.CharField(max_length=500, default='')
    type = models.CharField(max_length=50, default='Разное')

    def __str__(self):
        return self.title
