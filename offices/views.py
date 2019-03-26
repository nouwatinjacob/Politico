from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from django.db import IntegrityError

from .models import OfficeModel, Candidate
from .serializers import OfficeSerializer, CandidateSerializer

# Create your views here.

class OfficeList(APIView):
    def post(self, request, format=None):
        serializer = OfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        offices = OfficeModel.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response({"status": 200, "data": serializer.data})

class OfficeDetail(APIView):
    """
    Retrieve, update or delete a office instance.
    """
    def get_object(self, pk):
        try:
            return OfficeModel.objects.get(pk=pk)
        except OfficeModel.DoesNotExist:
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


class CandidateView(APIView):
    def post(self, request, **kwargs):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=self.request.user)
                return Response({"status": 201, "data": serializer.data})
            except IntegrityError:
                return Response({"status":400, "error": "You have applied for this office"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
