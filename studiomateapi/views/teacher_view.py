from studiomateapi.models import Teacher, Student
from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


class TeacherPermission(permissions.BasePermission):
    """Custom permissions for assessment status view"""

    def has_permission(self, request, view):
        if view.action in ['list']:
            return True
        if view.action in ['create', 'update', 'retrieve']:
            return request.auth is not None
        else:
            return False


class TeacherView(ViewSet):
    permission_classes = [TeacherPermission]

    def list(self, request):
        teachers = []

        if "status" in request.query_params:
            logged_in_teacher = Teacher.objects.filter(user=request.auth.user)
            teachers = logged_in_teacher

        elif "student" in request.query_params:
            student_id = request.query_params['student']
            student = Student.objects.get(pk=student_id)
            teachers = Teacher.objects.filter(pk=student.teacher_id)
        else:
            teachers = Teacher.objects.all()

        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        teacher = Teacher.objects.get(pk=pk)

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_teacher = Teacher()
        new_teacher.user = request.auth.user
        new_teacher.phone_number = request.data["phoneNumber"]
        new_teacher.img = request.data["img"]
        new_teacher.save()

        serializer = TeacherSerializer(new_teacher)
        return Response(serializer.data)

    def update(self, request, pk):

        teacher = Teacher.objects.get(pk=pk)
        user = User.objects.get(pk=request.auth.user.pk)
        teacher.user = user
        teacher.phone_number = request.data["phone_number"]
        teacher.img = request.data["img"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        teacher.save()
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class TeacherSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'phone_number', 'img',
                  'email', 'full_name', 'username')
