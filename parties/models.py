from django.db import models


# Create your models here.
class Party(models.Model):
    name = models.CharField(max_length=50,  unique=True)
    hqAddress = models.CharField(max_length=100)
    logoUrl = models.CharField(max_length=150)

    def __str__(self):
        return self.name
