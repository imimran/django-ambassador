from administrator.serializers import ProductSerializer
from rest_framework import generics, mixins
from rest_framework.response import Response
from common.serializers import UserSerializer
from core.models import User
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
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuth]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        return self.partial_update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)
