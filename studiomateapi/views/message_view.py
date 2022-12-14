from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Teacher, Message, Student
from django.contrib.auth.models import User
from datetime import datetime


class MessageView(ViewSet):

    def retrieve(self, request, pk):

        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        messages = []
        if "student" in request.query_params:
            student_id = request.query_params['student']
            student = Student.objects.get(pk=student_id)
            messages = Message.objects.filter(
                recipient=student.user) | Message.objects.filter(sender=student.user).order_by("date_time")

        else:
            messages = Message.objects.all()

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_message = Message()

        new_message.sender = request.auth.user
        needed_recipient = User.objects.get(pk=request.data["recipient"])
        new_message.recipient = needed_recipient
        new_message.date_time = datetime.today()
        new_message.content = request.data["content"]
        new_message.save()

        serializer = MessageSerializer(new_message)
        return Response(serializer.data)


class SenderSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ('id', 'first_name')


class MessageSerializer(serializers.ModelSerializer):

    sender = SenderSerializer(many=False)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'date_time',
                  'content')
