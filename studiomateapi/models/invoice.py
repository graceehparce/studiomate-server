from django.db import models


class Invoice(models.Model):
    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE, related_name='student_invoices')
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, related_name='teacher_invoices')
    date_created = models.DateField()
    service_date = models.DateField()
    amount = models.CharField(max_length=50)
    comment = models.CharField(max_length=750)
    paid = models.BooleanField(default=False)
