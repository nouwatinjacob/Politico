from django.urls import path
from .views import Voting

urlpatterns = [
    path("votes/", Voting.as_view(), name="voting"),
]