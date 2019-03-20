from django.urls import path
from .views import UserCreate, LoginView

urlpatterns = [
    path("auth/signup/", UserCreate.as_view(), name="user_create"),
    path("auth/login/", LoginView.as_view(), name="user_login")
]