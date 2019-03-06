from django.urls import path
from .views import PartyList

urlpatterns = [
    path("parties/", PartyList.as_view(), name="parties_create"),
    # path("parties/<int:pk>", PartyDetail.as_view(), name="parties_detail")
]