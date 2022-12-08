from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from studiomateapi.models import Student, Teacher


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'is_staff': authenticated_user.is_staff

        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):

    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['firstName'],
        last_name=request.data['lastName'],
        email=request.data['email']
    )

    if "teacher" in request.data:
        student = Student.objects.create(
            phone_number=request.data['phoneNumber'],
            teacher=request.data['teacher'],
            img=request.data['img'],
            user=new_user
        )
        token = Token.objects.create(user=student.user)

    else:
        new_user.is_staff = True
        new_user.save()
        teacher = Teacher.objects.create(
            phone_number=request.data['phoneNumber'],
            img=request.data['img'],
            user=new_user
        )
        token = Token.objects.create(user=teacher.user)

    data = {
        'valid': True,
        'token': token.key,
        'is_staff': new_user.is_staff}
    return Response(data)
