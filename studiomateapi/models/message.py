from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='sender_user_messages')
    recipient = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='recipient_user_messages')
    date = models.DateField()
    timestamp = models.TimeField()
    content = models.CharField(max_length=3000)
