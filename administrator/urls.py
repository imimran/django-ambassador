from django.contrib import admin
from django.urls import path, include

from .views import AmbassadorAPIView, ProductGenericAPIView

urlpatterns = [
    path('auth/', include('common.urls')),
    path('ambassadors/', AmbassadorAPIView.as_view()),
    path('products', ProductGenericAPIView.as_view()),
    path('products/<str:pk>', ProductGenericAPIView.as_view())
]