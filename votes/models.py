from django.db import models

from offices.models import OfficeModel, Candidate
from authentication.models import CustomUser
# Create your models here.
class Vote(models.Model):
    office = models.ForeignKey(OfficeModel, on_delete=models.CASCADE, related_name='office')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate')
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='voter')

    class Meta:
        unique_together = (('office', 'voter'),)
        