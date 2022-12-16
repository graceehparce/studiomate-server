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
        assignments = []

        if "student" in request.query_params:
            student_id = request.query_params['student']
            assignments = Assignment.objects.filter(
                student=student_id
            ).order_by("date_created")

        else:
            assignments = Assignment.objects.all().order_by("date_created")

        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_assignment = Assignment()

        logged_in_teacher = Teacher.objects.get(user=request.auth.user)
        assigned_student = Student.objects.get(pk=request.data["student"])

        new_assignment.teacher = logged_in_teacher
        new_assignment.student = assigned_student
        new_assignment.date_created = request.data["date_created"]
        new_assignment.fundamentals = request.data["fundamentals"]
        new_assignment.repertoire = request.data["repertoire"]
        new_assignment.comments = request.data["comments"]
        new_assignment.save()

        serializer = AssignmentSerializer(new_assignment)
        return Response(serializer.data)

    def destroy(self, request, pk):
        assignment = Assignment.objects.get(pk=pk)
        assignment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:

        model = Teacher
        fields = ('id', 'full_name', 'img')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:

        model = Student
        fields = ('id', 'full_name', 'img')


class AssignmentSerializer(serializers.ModelSerializer):

    teacher = TeacherSerializer(many=False)
    student = StudentSerializer(many=False)

    class Meta:
        model = Assignment
        fields = ('id', 'student', 'teacher', 'date_created',
                  'fundamentals', 'repertoire', 'comments')
