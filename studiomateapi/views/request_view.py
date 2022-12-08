from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Teacher, Request


class RequestView(ViewSet):

    def retrieve(self, request, pk):

        request = Request.objects.get(pk=pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_request = Request()

        logged_in_teacher = Teacher.objects.get(user=request.auth.user)

        new_request.teacher = logged_in_teacher.pk
        new_request.student = request.data["studentId"]
        new_request.accepted = False
        new_request.time = request.data["time"]
        new_request.date = request.data["date"]
        new_request.save()

        serializer = RequestSerializer(new_request)
        return Response(RequestSerializer.data)

    def destroy(self, request, pk):
        resource = Request.objects.get(pk=pk)
        resource.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ('id', 'student', 'viewed', 'date',
                  'time', 'teacher')
