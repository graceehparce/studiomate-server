
from studiomateapi.views import TeacherView, StudentView, AssignmentView, RequestView, ResourceView, InvoiceView, MessageView, NotificationTypeView, NotificationView
from rest_framework import routers
from studiomateapi.views import register_user, login_user
from django.conf.urls import include
from django.contrib import admin
from django.urls import path


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'teachers', TeacherView, 'teacher')
router.register(r'students', StudentView, 'student')
router.register(r'assignments', AssignmentView, 'assignment')
router.register(r'requests', RequestView, 'request')
router.register(r'resources', ResourceView, 'resource')
router.register(r'invoices', InvoiceView, 'invoice')
router.register(r'messages', MessageView, 'message')
router.register(r'notifications', NotificationView, 'notification')


router.register(r'notificationTypes', NotificationTypeView, 'notificationType')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
