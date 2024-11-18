from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()

@api_view(['POST'])
def registerUser(request):
    message = {"message": "User could not be registered"}

    if 'password' in request.data and 'email' in request.data and 'name' in request.data:
        try:
            user = User.objects.create_user(
                email=request.data['email'],
                name=request.data['name'],
                password=make_password(request.data['password']),
                is_active=False,
                is_staff=False,
                is_superuser=False,
                sent_verification_email=False,
                verified_email=False
            )

        except IntegrityError:
            return Response({'message': 'User already exists'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'user could not be registered'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            send_mail(
                f'Verify your user acount for {settings.WEB_SITE_NAME}',
                F'To verify your user account for {settings.WEB_SITE_NAME}, please go to {settings.VERIFICATION_URL}',
                settings.SENDER_EMAIL,
                [request.data['email']],
                fail_silently=False,
                html_message=f'Please <a href="{settings.VERIFICATION_URL}">click this link</a> to verify your user account for {settings.WEB_SITE_NAME}.',
            )
            user.sent_verification_email=True
            user.save()
        except:
            message={'message': 'Verification email could not be sent.'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'user registered'},status=status.HTTP_200_OK)
    return Response({"message": "User information missing"}, status=status.HTTP_400_BAD_REQUEST)