from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Student, Request, Assignment, Teacher


class AssignmentView(ViewSet):

    def retrieve(self, request, pk):

        assignment = Assignment.objects.get(pk=pk)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        logged_in_student = Student.objects.get(user=request.auth.user)
        assignments = Assignment.objects.filter(student=logged_in_student)

        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_assignment = Assignment()

        logged_in_teacher = Teacher.objects.get(user=request.auth.user)

        new_assignment.teacher = logged_in_teacher.pk
        new_assignment.student = request.data["studentId"]
        new_assignment.date_created = request.data["date"]
        new_assignment.fundamentals = request.data["fundamentals"]
        new_assignment.repertoire = request.data["repertoire"]
        new_assignment.comments = request.data["comments"]
        new_assignment.save()

        serializer = AssignmentSerializer(new_assignment)
        return Response(AssignmentSerializer.data)

    def destroy(self, request, pk):
        assignment = Assignment.objects.get(pk=pk)
        assignment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ('id', 'student', 'teacher', 'date_created',
                  'fundamentals', 'repertoire', 'comments')
