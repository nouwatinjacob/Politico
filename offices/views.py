from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from .models import Office
from .serializers import OfficeSerializer

# Create your views here.

class OfficeList(APIView):
    def post(self, request, format=None):
        serializer = OfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
