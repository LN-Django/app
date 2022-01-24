import logging
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from .constants import product_properties, post_product_properties
from ..services import ProductService
from ..serializers import ProductSerializer


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
        return_data = ProductService.get_all_products()
        return Response(return_data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=post_product_properties,

    ), responses={
        '201': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=product_properties),
        '400': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Bad request'),
                'errors': openapi.Schema(type=openapi.TYPE_OBJECT, description='Bad request: Invalid parameter(s)')
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

        try:
            return_data = ProductService.post_single_product(
                new_product.data, request_data)

            """Handle external API calls not successful"""
            if not (return_data.get('errors') is None):
                return Response(return_data, status=400)

            return Response(return_data, status=201)
        except ValidationError as error:
            self.logger.info('Validation error while creating product')
            return Response({'message': 'Bad request: validation error', 'errors': error}, status=400)
        except KeyError as error:
            self.logger.info('Request body validation error')
            return Response({'message': 'Bad request: {:s}'.format(str(error))}, status=400)
