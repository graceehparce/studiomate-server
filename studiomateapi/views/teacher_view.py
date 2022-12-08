from studiomateapi.models import Teacher
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
        user = User.objects.get(pk=request.auth.user)
        teacher.user = user
        teacher.phone_number = request.data["phoneNumber"]
        teacher.img = request.data["img"]
        user.first_name = request.data["firstName"]
        user.last_name = request.data["lastName"]
        user.email = request.data["email"]
        teacher.save()
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'phone_number', 'img',
                  'email', 'full_name', 'username')
