from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from studiomateapi.models import Teacher, Request, Student, Notification, NotificationType
from django.contrib.auth.models import User
from datetime import datetime


class NotificationView(ViewSet):

    def list(self, request):

        logged_in_user = User.objects.get(pk=request.auth.user.id)

        notifications = Notification.objects.filter(
            receiver=logged_in_user.pk, viewed=False
        ).order_by("date_created")

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        notification = Notification()

        if "student" in request.query_params:
            needed_student = Student.objects.get(
                pk=request.query_params['student'])
            needed_user = User.objects.get(pk=needed_student.user.id)
            notification.receiver = needed_user
            sender = User.objects.get(pk=request.auth.user.id)
            notification.sender = sender
            notification.date_created = datetime.today()
            notification.viewed = False
            needed_type = NotificationType.objects.get(
                pk=request.data["notification_type"])
            notification.notification_type = needed_type
            notification.save()

        if "teacher" in request.query_params:
            needed_teacher = Teacher.objects.get(
                pk=request.query_params['teacher'])
            needed_user = User.objects.get(pk=needed_teacher.user.id)
            notification.receiver = needed_user
            sender = User.objects.get(pk=request.auth.user.id)
            notification.sender = sender
            notification.user = needed_user
            notification.date_created = datetime.today()
            notification.viewed = False
            needed_type = NotificationType.objects.get(
                pk=request.data["notification_type"])
            notification.notification_type = needed_type
            notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def update(self, request, pk):
        needed_notification = Notification.objects.get(pk=pk)
        needed_notification.viewed = request.data["viewed"]
        needed_notification.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        notification.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ('id', 'first_name')


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:

        model = NotificationType
        fields = ('id', 'type')


class NotificationSerializer(serializers.ModelSerializer):

    sender = UserSerializer(many=False)
    receiver = UserSerializer(many=False)

    notification_type = NotificationTypeSerializer(many=False)

    class Meta:
        model = Notification
        fields = ('id', 'receiver', 'sender', 'date_created', 'viewed',
                  'notification_type')
