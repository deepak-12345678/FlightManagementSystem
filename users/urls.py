
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("login/", login, name="login"),
    path("register/", reqistration, name="register"),
]