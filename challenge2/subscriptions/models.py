from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    stripeId = models.CharField(max_length=255, null=True)
    subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class Subscription(models.Model):
    stripeSubscriptionId = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255)
    user = models.OneToOneField(User, related_name="user_subscription", on_delete=models.CASCADE)
