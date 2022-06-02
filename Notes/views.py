from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from Notes.serializers import UserSerializer, NoteSerializer
from Notes.models import UserProfile, Note

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


@api_view(['GET', 'POST'])
def list_create(request):
    context = {'request': request}
    if request.method == 'GET':
        user_profile = request.user.userprofile
        notes = user_profile.note_set.all()
        serializer = NoteSerializer(notes, context=context, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detail(request, note_id):
    user_profile = request.user.userprofile
    try:
        note = user_profile.note_set.get(id=note_id)
        serializer = NoteSerializer(note, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        content = {
            "response": "404 OBJECT DOES NOT EXIST"
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def delete(request, note_id):
    user_profile = request.user.userprofile
    try:
        note = user_profile.note_set.get(id=note_id)
        note.delete()
        content = {
            "response": "NOTE SUCCESSFULLY DELETED"
        }
        return Response(content, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        content = {
            "response": "404 OBJECT DOES NOT EXIST"
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update(request, note_id):
    user_profile = request.user.userprofile
    try:
        note = user_profile.note_set.get(id=note_id)
        serializer = NoteSerializer(note, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            note.title = serializer.instance.title
            note.content = serializer.instance.content
            note.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist:
        content = {
            "response": "404 OBJECT DOES NOT EXIST"
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
