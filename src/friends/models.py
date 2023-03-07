from django.db import models
from django.contrib.auth.models import User


REQUEST_STATUS_CHOICES = (
    ("PENDING", "Pending"),
    ("ACCEPTED", "Accepted"),
    ("REJECTED", "Rejected"),
)


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

    class Meta:
        unique_together = ('user', 'friend',)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    status = models.CharField(max_length=8, choices=REQUEST_STATUS_CHOICES, default='PENDING')
