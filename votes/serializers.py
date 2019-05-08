from rest_framework import serializers

from .models import Vote

from offices.serializers import OfficeSerializer, CandidateSerializer

class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Vote
        fields = ('id', 'office', 'candidate', 'voter_id', 'voter')
