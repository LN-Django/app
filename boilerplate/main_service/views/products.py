import logging
from django.core.exceptions import ValidationError
from django.core import serializers
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .constants import product_properties
from ..serializers import ProductSerializer
from ..models import Product


class ProductsListView(APIView):
    logger = logging.getLogger('mainLogger')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    @swagger_auto_schema(responses={
        '200': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                 properties=product_properties),
            description='Array of product datas'),
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
        '201': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=product_properties),
        '400': openapi.Schema(
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
        new_product = ProductSerializer(data=request_data)

        if not new_product.is_valid():
            self.logger.info('Product data serializer error')
            return Response({'message': 'Bad request: invalid parameter', 'errors': new_product.errors}, status=400)

        # TODO: Integrate product ORM creation inside the `save` method on serializer
        product_data: Product = new_product.save()
        try:
            product: Product = Product.objects.create(name=product_data.name, base_price=product_data.base_price,
                                                      description=product_data.description, weight=product_data.weight, category=product_data.category)
            return_data = new_product.data
            return_data['id'] = product.id

            return Response(return_data, status=201)
        except ValidationError as error:
            self.logger.info('Validation error while creating product')
            return Response({'message': 'Bad request: validation error', 'errors': error}, status=400)
