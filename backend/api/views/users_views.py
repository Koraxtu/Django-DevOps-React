from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore


User = get_user_model()

@api_view(['POST'])
def registerUser(request):
    message = {"message": "User could not be registered"}

    if 'password' in request.data and 'email' in request.data and 'name' in request.data:
        try:
            user = User.objects.create_user(
                email=request.data['email'],
                name=request.data['name'],
                password=request.data['password'],
                is_active=False,
                is_staff=False,
                is_superuser=False,
                sent_verification_email=False,
                verified_email=False
            )
            return Response(status=status.HTTP_200_OK)
        except:
            message = {"message": "User could not be registered"}
    else:
        message = {"message": "User information missing"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)