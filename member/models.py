from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    newsletter_subscribed = models.BooleanField(default=False)
    is_business_owner = models.BooleanField(default=False)
    member_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
