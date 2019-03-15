from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User

from .serializers import UserSerializer

# Create your views here.

class UserCreate(APIView):
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
