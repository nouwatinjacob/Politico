from django.urls import path

from .views import OfficeList

urlpatterns = [
    path("offices/", OfficeList.as_view(), name="office_create")
]