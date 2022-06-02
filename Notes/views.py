from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from Notes.serializers import UserSerializer
from Notes.models import UserProfile

"""
{
"username": "user1",
"password": "gdsctask1"
}
"""


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        UserProfile.objects.create(user=serializer.instance)
        context = {
            "username": serializer.data['username'],
            "password": '*' * len(request.data['password']),
            "response": "USER CREATED",
        }
        return Response(context, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        content = {
            'response': 'ERROR! USERNAME OR PASSWORD NOT PROVIDED'
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    print(user)
    if not user:
        content = {
            'response': 'ERROR! INVALID CREDENTIALS'
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    content = {
        'token': token.key,
        'response': 'LOGIN AUTHORIZED, TOKEN GENERATED'
    }
    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_create(request):
    return Response({"lol"}, status=status.HTTP_200_OK)
