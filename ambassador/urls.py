from django.contrib import admin
from django.urls import path, include

from .views import ProductBackAPIView, ProductFontAPIView

urlpatterns = [

    path('auth/', include('common.urls')),
    path('products/front', ProductFontAPIView.as_view()),
    path('products/back', ProductBackAPIView.as_view() ),
    
]