from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import IntegrityError

from .models import Vote
from .serializers import VoteSerializer

# Create your views here.
class Voting(APIView):
    def post(self, request, format=None):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(voter=self.request.user)
                return Response({
                    "status": 200,
                    "data": serializer.data
                })
            except IntegrityError:
                return Response({
                    "status": 400,
                    "error": "You have voted this office, please vote another pollitical office"
                })
        return Response({"status":400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
