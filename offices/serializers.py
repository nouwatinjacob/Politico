from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from .models import OfficeModel, Candidate

class OfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeModel
        fields = '__all__'
        extra_kwargs = {
            "name": {"required": True, "allow_null": False }
        }

class CandidateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Candidate
        fields = ('office', 'user')
