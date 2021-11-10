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


class ProductView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    @swagger_auto_schema(responses={
        '200': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=product_properties),
        '404': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            },
            description='Resource not found'
        ),
        '500': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            },
            description='Internal server error'
        )
    },
        operation_description='Get datas of a single product with the provided `product_id`'
    )
    def get(self, request: Request, product_id):
        queryset = Product.objects.filter(id=product_id)
        product_count = queryset.count()

        if product_count == 0:
            return Response({'message': 'Product not found'}, status=404)
        elif product_count > 1:
            return Response({'message': 'Internal server error. Product with the id ' + product_id + ' returned more than one product'}, status=500)

        return Response(queryset.values()[0])
