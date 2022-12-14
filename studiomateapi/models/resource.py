from django.db import models


class Resource(models.Model):
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, related_name='teacher_resources')
    resource = models.CharField(max_length=250)
    img = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
