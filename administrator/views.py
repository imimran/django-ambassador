from administrator.serializers import LinkSerializer, OrderSerializer, ProductSerializer
from rest_framework import generics, mixins
from rest_framework.response import Response
from common.serializers import UserSerializer
from core.models import Link, Order, User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from common.auth import JWTAuth

from core.models import Product

# Create your views here.


class AmbassadorAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuth]

    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)
        serializer = UserSerializer(ambassadors, many=True)

        return Response({'error': False, 'data': serializer.data})


class ProductGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuth]
    print('permission_classes', permission_classes)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        return self.partial_update(request, pk )

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class LinkAPIView(APIView):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuth]

    def get(self, request, pk):
        link = Link.objects.filter(user_id=pk)
        serializer =LinkSerializer(link, many=True)
        return Response({
            'error': False, 'data': serializer.data
        })


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuth]

    def get(self, request):
        orders = Order.objects.filter(complete=True)
        serializer = OrderSerializer(orders, many=True)
        return Response({ 'error': False, 'data': serializer.data })