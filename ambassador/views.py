from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

from core.models import Product
from .serializers import ProductSerializer
from django.core.cache import cache 
import time, math


class ProductFontAPIView(APIView):

    def get(self, _):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response({'error': False, 'data': serializer.data})

class ProductBackAPIView(APIView):

    def get(self, request):
        # products = cache.get('product_backend')

        # if not products:
        #     #time.sleep(2)
        #     products = list(Product.objects.all())
        #     cache.set('product_backend', products, timeout= 60 * 30) #30 min

        products = Product.objects.all()

        keyword = request.query_params.get('keyword', '')

        if keyword:
            products= list({
                p for p in products
                if (keyword.lower() in p.title.lower()) or (keyword.lower() in p.description.lower())
            })

        total = len(products)    

        # sort = request.query_params.get('sort', None)
        # if sort == 'asc':
        #     products.sort(key=lambda p: p.price)
        # elif sort == 'desc':
        #     products.sort(key=lambda p: p.price, reverse=True)



        per_page = 2
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page * per_page

        data = ProductSerializer(products[start:end], many=True).data
        return Response({
            'data': data,
            'meta': {
                'total': total,
                'current_page': page,
                'total_page': math.ceil(total / per_page)
            }
        })      


