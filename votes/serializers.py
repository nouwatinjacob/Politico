from rest_framework import serializers

from .models import Vote

class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Vote
        fields = '__all__'
