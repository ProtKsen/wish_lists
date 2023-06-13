from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")

    class Meta:
        unique_together = (
            "user",
            "friend",
        )


class FriendRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = "Pending"
        ACCEPTED = "Accepted"
        REJECTED = "Rejected"

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    status = models.CharField(
        max_length=8, choices=RequestStatus.choices, default=RequestStatus.PENDING
    )
