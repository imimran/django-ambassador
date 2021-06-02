from django.contrib import admin
from django.urls import path, include
from rest_framework import views

from .views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view() ),
    path('login', LoginAPIView.as_view()),
]