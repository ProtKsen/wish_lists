from django.contrib.auth.models import User
from django.db import models


class HashSalt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salt = models.CharField(max_length=100)
