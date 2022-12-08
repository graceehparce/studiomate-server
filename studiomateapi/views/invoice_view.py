from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Student, Teacher, Invoice
from django.contrib.auth.models import User


class InvoiceView(ViewSet):

    def retrieve(self, request, pk):

        invoice = Invoice.objects.get(pk=pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        logged_in_student = Student.objects.get(user=request.auth.user)

        invoices = Student.objects.filter(student=logged_in_student)

        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_invoice = Student()

        logged_in_teacher = Teacher.objects.get(user=request.auth.user)

        new_invoice.teacher = logged_in_teacher.pk
        new_invoice.student = request.data["studentId"]
        new_invoice.date_created = request.data["dateCreated"]
        new_invoice.service_date = request.data["serviceDate"]
        new_invoice.amount = request.data["amount"]
        new_invoice.comment = request.data["comment"]
        new_invoice.save()

        serializer = InvoiceSerializer(new_invoice)
        return Response(serializer.data)

    def destroy(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        invoice.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ('id', 'student', 'teacher', 'date_created', 'service_date',
                  'amount', 'comment')
