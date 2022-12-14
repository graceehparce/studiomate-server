from django.db import models


class Comment(models.Model):
    assignment = models.OneToOneField(
        "Assignment", on_delete=models.CASCADE, related_name='assignment_comments')
    comment = models.CharField(max_length=1000)
