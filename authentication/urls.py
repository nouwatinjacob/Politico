from django.urls import path
from .views import UserCreate

urlpatterns = [
    path("auth/signup/", UserCreate.as_view(), name="user_create")
]