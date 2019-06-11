from django.shortcuts import render
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from rest_framework import permissions

from django.contrib.auth.models import User

from .serializers import UserSerializerWithToken, TokenSerializer


# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.

class UserCreate(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 201,
                "data": [serializer.data],
                }, status=status.HTTP_201_CREATED)
        return Response({
            "status":400, 
            "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response({
                "status": 200,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 400,
                "error": "Wrong credentials"
            }, status=status.HTTP_400_BAD_REQUEST)
