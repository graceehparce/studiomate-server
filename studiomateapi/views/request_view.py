from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Teacher, Request, Student


class RequestView(ViewSet):

    def retrieve(self, request, pk):

        request = Request.objects.get(pk=pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        if "student" in request.query_params:
            student_id = request.query_params['student']

            requests = Request.objects.filter(
                student=student_id
            ).order_by("date")

        else:
            logged_in_teacher = Teacher.objects.get(user=request.auth.user)
            requests = Request.objects.filter(
                teacher=logged_in_teacher).order_by("date")

        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_request = Request()

        logged_in_teacher = Teacher.objects.get(user=request.auth.user)

        new_request.teacher = logged_in_teacher
        needed_student = Student.objects.get(pk=request.data["student"])
        new_request.student = needed_student
        new_request.accepted = False
        new_request.time = request.data["time"]
        new_request.date = request.data["date"]
        new_request.save()

        serializer = RequestSerializer(new_request)
        return Response(serializer.data)

    def update(self, request, pk):
        needed_request = Request.objects.get(pk=pk)
        needed_request.accepted = request.data["accepted"]
        needed_request.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        resource = Request.objects.get(pk=pk)
        resource.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:

        model = Student
        fields = ('id', 'full_name')


class RequestSerializer(serializers.ModelSerializer):

    student = StudentSerializer(many=False)

    class Meta:
        model = Request
        fields = ('id', 'student', 'accepted', 'date',
                  'time', 'teacher')
