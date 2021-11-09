from django.core import serializers
from django.db.models import query
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..serializers import ProductSerializer
from ..models import Product

product_properties = {
    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product (max length: 64 characters.)'),
    'base_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Base price of the product'),
    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product description (max length: 128 characters)'),
    'weight': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product weight'),
    'category': openapi.Schema(type=openapi.TYPE_STRING, description='Product category')
}


class ProductsListView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    @swagger_auto_schema(responses={
        '200': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=product_properties),

    },
        operation_description='Retrieve a list of all products'
    )
    def get(self, request, format=None):
        queryset = Product.objects.all()
        return Response(queryset.values())

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=product_properties,

    ), responses={
        '200': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=product_properties),
        '500': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                'errors': openapi.Schema(type=openapi.TYPE_OBJECT, description='Django auto-generated errors via serializer')
            },
            description='Invalid parameter'
        )
    },
        operation_description='Create a new product'
    )
    def post(self, request: Request, format=None):
        request_data = JSONParser().parse(request)

        if request_data['base_price'] <= 0:
            return Response({'message': 'Bad request: base_price property should be higher than 0'}, status=500)
        if request_data['weight'] <= 0:
            return Response({'message': 'Bad request: weight property should be higher than 0'}, status=500)

        new_product = ProductSerializer(data=request_data)
        if not new_product.is_valid():
            return Response({'message': 'Bad request: invalid parameter', 'errors': new_product.errors}, status=500)

        product: Product = new_product.save()
        Product.objects.create(name=product.name, base_price=product.base_price,
                               description=product.description, weight=product.weight, category=product.category)
        return Response(new_product.data)
