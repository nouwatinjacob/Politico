from django.urls import path

from .views import OfficeList, OfficeDetail, CandidateView, VoteResultView

urlpatterns = [
    path("offices/", OfficeList.as_view(), name="office_create"),
    path("offices/<int:pk>", OfficeDetail.as_view(), name="offices_details"),
    path("office/register", CandidateView.as_view(), name="register_candidate"),
    path("office/<int:office_id>/result", VoteResultView.as_view(), name="vote_result"),
]
