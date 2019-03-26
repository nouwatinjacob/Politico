from django.contrib import admin
from .models import OfficeModel, Candidate

# Register your models here.
admin.site.register(OfficeModel)
admin.site.register(Candidate)