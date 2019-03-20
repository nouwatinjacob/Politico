from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User

from .serializers import UserSerializer

# Create your views here.

class UserCreate(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 201,
                "data": [serializer.data]
                }, status=status.HTTP_201_CREATED)
        return Response({
            "status":400, 
            "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = ()
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({
                "status": 200,
                "data": {
                    "token": user.auth_token.key
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 400,
                "error": "Wrong credentials"
            }, status=status.HTTP_400_BAD_REQUEST)
