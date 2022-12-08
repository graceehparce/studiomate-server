from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_student')
    phone_number = models.CharField(max_length=250)
    img = models.CharField(max_length=1000)
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, related_name='teachers_student')

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'

    @property
    def email(self):
        return f'{self.user.email}'
