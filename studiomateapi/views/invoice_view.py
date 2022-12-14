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
        invoices = []

        if "student" in request.query_params:
            student_id = request.query_params['student']
            invoices = Invoice.objects.filter(
                student=student_id
            )

        else:
            invoices = Invoice.objects.all()

        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_invoice = Invoice()

        logged_in_teacher = Teacher.objects.get(user=request.auth.user)
        assigned_student = Student.objects.get(pk=request.data["student"])

        new_invoice.teacher = logged_in_teacher
        new_invoice.student = assigned_student
        new_invoice.date_created = request.data["date_created"]
        new_invoice.service_date = request.data["service_date"]
        new_invoice.amount = request.data["amount"]
        new_invoice.comment = request.data["comment"]
        new_invoice.save()

        serializer = InvoiceSerializer(new_invoice)
        return Response(serializer.data)

    def destroy(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        invoice.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:

        model = Teacher
        fields = ('id', 'full_name', 'img')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:

        model = Student
        fields = ('id', 'full_name', 'img')


class InvoiceSerializer(serializers.ModelSerializer):

    teacher = TeacherSerializer(many=False)
    student = StudentSerializer(many=False)

    class Meta:
        model = Invoice
        fields = ('id', 'student', 'teacher', 'date_created', 'service_date',
                  'amount', 'comment')
        depth = 1
