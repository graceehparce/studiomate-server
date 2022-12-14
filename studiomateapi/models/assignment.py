from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE, related_name='student_assignments')
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, related_name='teacher_assignments')
    date_created = models.DateField()
    fundamentals = models.CharField(max_length=1000)
    repertoire = models.CharField(max_length=1000)
    comments = models.CharField(max_length=2000)
