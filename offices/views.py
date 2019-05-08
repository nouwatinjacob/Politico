from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status

import simplejson as json


from django.core import serializers

from django.db import IntegrityError

from .models import OfficeModel, Candidate
from votes.models import Vote
from .serializers import OfficeSerializer, CandidateSerializer
from votes.serializers import VoteSerializer

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
        user_id = self.request.user.id
        check_candidacy = Candidate.objects.filter(user_id=user_id)
        if check_candidacy:
            return Response({"status":400, "error":"You have either applied for this office or another office"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response({"status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VoteResultView(APIView):
    """
    Retrieve, update or delete a office instance.
    """

    def get(self, request, office_id, format=None):
        votes = Vote.objects.filter(office_id=office_id)
        serializer = VoteSerializer(votes, many=True)
        results = Vote.objects.filter(office_id=office_id).count()
        if not votes:
            return Response({"status":400, "error": "No record"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": 200, "data": serializer.data, "counts": results}, status=status.HTTP_200_OK)
