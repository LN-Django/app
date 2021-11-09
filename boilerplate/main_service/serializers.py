from django.core.validators import MinValueValidator
from rest_framework import serializers
from restapi.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
