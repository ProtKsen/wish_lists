from django.db import models

class Wish(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.title
