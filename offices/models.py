from django.db import models

# Create your models here.
class Office(models.Model):
    name = models.CharField(max_length=30, unique=True)
    office_type = models.CharField(max_length=30)

    def __str__(self):
        return self.name
