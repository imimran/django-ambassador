from django.db.models import fields
from core.models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields= '__all__'