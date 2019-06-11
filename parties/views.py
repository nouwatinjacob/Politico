from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from .models import Party
from .serializers import PartySerializer

class PartyList(APIView):
    """
    List all parties, or create a new snippet.
    """
    def get(self, request, format=None):
        parties = Party.objects.all()
        serializer = PartySerializer(parties, many=True)
        return Response({ "status": 200, "data": serializer.data})

    def post(self, request, format=None):
        serializer = PartySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PartyDetail(APIView):
    """
    Retrieve, update or delete a party instance.
    """
    def get_object(self, pk):
        try:
            return Party.objects.get(pk=pk)
        except Party.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        parties = self.get_object(pk)
        serializer = PartySerializer(parties)
        return Response({"status": 200, "data": serializer.data})

    def put(self, request, pk, format=None):
        party = self.get_object(pk)
        serializer = PartySerializer(party, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "data": serializer.data})
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        party = self.get_object(pk)
        party.delete()
        return Response({"status": 200, "data": [{"message": "party successfully deleted"}]}, status=status.HTTP_200_OK)