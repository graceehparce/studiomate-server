from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_notifications')
    viewed = models.BooleanField()
    date_created = models.DateTimeField()
    notification_type = models.ForeignKey(
        "NotificationType", on_delete=models.CASCADE, related_name='type_notifications')
