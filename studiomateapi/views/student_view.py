from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Student, Teacher
from django.contrib.auth.models import User


class StudentView(ViewSet):

    def retrieve(self, request, pk):

        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        students = []

        if "status" in request.query_params:
            logged_in_student = Student.objects.filter(user=request.auth.user)
            students = logged_in_student

        else:
            logged_in_teacher = Teacher.objects.get(user=request.auth.user)

            students = Student.objects.filter(teacher=logged_in_teacher.pk)

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_student = Student()
        new_student.user = User.objects.get(request.auth.user)
        new_student.phone_number = request.data["phone_number"]
        new_student.img = request.data["img"]
        needed_teacher = Teacher.objects.get(pk=request.data["teacher"])
        new_student.teacher = needed_teacher
        new_student.save()

        serializer = StudentSerializer(new_student)
        return Response(serializer.data)

    def destroy(self, request, pk):
        student = Student.objects.get(pk=pk)
        student.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        student = Student.objects.get(pk=pk)
        user = User.objects.get(pk=request.auth.user.pk)
        student.user = user
        student.phone_number = request.data["phone_number"]
        needed_teacher = Teacher.objects.get(pk=request.data["teacher"])
        student.teacher = needed_teacher
        student.img = request.data["img"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        student.save()
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'full_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class StudentSerializer(serializers.ModelSerializer):

    teacher = TeacherSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = ('id', 'user', 'teacher', 'phone_number', 'img',
                  'email', 'full_name', 'username')
