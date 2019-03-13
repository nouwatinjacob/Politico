from django.urls import path

from .views import OfficeList, OfficeDetail

urlpatterns = [
    path("offices/", OfficeList.as_view(), name="office_create"),
    path("offices/<int:pk>", OfficeDetail.as_view(), name="offices_details")
]