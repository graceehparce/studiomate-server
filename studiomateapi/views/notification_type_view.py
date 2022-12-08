from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Teacher, NotificationType


class NotificationTypeView(ViewSet):

    def retrieve(self, request, pk):

        notification_type = NotificationType.objects.get(pk=pk)
        serializer = NotificationTypeSerializer(notification_type)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationType
        fields = ('id', 'type')
