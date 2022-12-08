from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    student = models.OneToOneField(
        "Student", on_delete=models.CASCADE, related_name='student_requests')
    date = models.DateTimeField()
    time = models.TimeField()
    accepted = models.BooleanField()
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, related_name='teacher_requests')
