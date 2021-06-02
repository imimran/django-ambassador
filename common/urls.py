from django.contrib import admin
from django.urls import path, include
from rest_framework import views

from .views import (RegisterAPIView, LoginAPIView, UserAPIView,
 ProfileInfoAPIView, ProfilePasswordAPIView)

urlpatterns = [
    path('register', RegisterAPIView.as_view() ),
    path('login', LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('user/info', ProfileInfoAPIView.as_view()),
    path('user/change-password', ProfilePasswordAPIView.as_view()),
]