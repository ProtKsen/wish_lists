from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

    class Meta:
        unique_together = ('user', 'friend',)
