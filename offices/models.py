from django.db import models

from authentication.models import CustomUser

# Create your models here.
class OfficeModel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    office = models.ForeignKey(OfficeModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('office', 'user'),)
