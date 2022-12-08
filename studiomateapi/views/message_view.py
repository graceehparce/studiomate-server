from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Teacher, Request, Message
from django.contrib.auth.models import User
from datetime import date, time


class MessageView(ViewSet):

    def retrieve(self, request, pk):

        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        logged_in_user = User.objects.get(request.auth.user)
        messages = Message.objects.filter(recipient=logged_in_user.pk)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_message = Message()

        logged_in_user = User.objects.get(request.auth.user)

        new_message.sender = logged_in_user.pk
        new_message.recipient = request.data["recipientId"]
        new_message.date = date
        new_message.time = time
        new_message.content = request.data["content"]
        new_message.save()

        serializer = MessageSerializer(new_message)
        return Response(MessageSerializer.data)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'date',
                  'time', 'content')
