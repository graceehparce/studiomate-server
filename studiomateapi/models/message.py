from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender_user_messages')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipient_user_messages')
    date_time = models.DateTimeField()
    content = models.CharField(max_length=3000)
