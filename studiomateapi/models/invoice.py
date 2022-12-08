from django.db import models


class Invoice(models.Model):
    student = models.OneToOneField(
        "Student", on_delete=models.CASCADE, related_name='student_invoices')
    teacher = models.OneToOneField(
        "Teacher", on_delete=models.CASCADE, related_name='teacher_invoices')
    date_created = models.DateField()
    service_date = models.DateField()
    amount = models.IntegerField
    comment = models.CharField(max_length=750)
