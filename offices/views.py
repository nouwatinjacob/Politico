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

    def get(self, request, format=None):
        offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response({"status": 200, "data": serializer.data})

class OfficeDetail(APIView):
    """
    Retrieve, update or delete a office instance.
    """
    def get_object(self, pk):
        try:
            return Office.objects.get(pk=pk)
        except Office.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        office = self.get_object(pk)
        serializer = OfficeSerializer(office)
        return Response({"status": 200, "data": serializer.data})

    def patch(self, request, pk, format=None):
        office = self.get_object(pk)
        serializer = OfficeSerializer(office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "data": serializer.data})
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        office = self.get_object(pk)
        office.delete()
        return Response({"status": 200, "data": [{"message": "office successfully deleted"}]}, status=status.HTTP_200_OK)
