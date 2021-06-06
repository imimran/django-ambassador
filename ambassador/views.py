from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Product
from .serializers import ProductSerializer

class ProductFontAPIView(APIView):

    def get(self, _):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response({'error': False, 'data': serializer.data})

class ProductBackAPIView(APIView):

    def get(self, _):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response({'error': False, 'data': serializer.data})        


