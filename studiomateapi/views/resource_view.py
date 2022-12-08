from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Student, Resource, Teacher
from django.contrib.auth.models import User


class ResourceView(ViewSet):

    def list(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_resource = Resource()

        logged_in_teacher = Teacher.objects.get(user=request.auth.user)

        new_resource.teacher = logged_in_teacher.pk
        new_resource.resource = request.data["resource"]
        new_resource.img = request.data["img"]
        new_resource.save()

        serializer = ResourceSerializer(new_resource)
        return Response(serializer.data)

    def destroy(self, request, pk):
        resource = Resource.objects.get(pk=pk)
        resource.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'teacher', 'resource', 'img')
