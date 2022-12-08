from django.db import models


class NotificationType(models.Model):
    type = models.CharField(max_length=1000)
