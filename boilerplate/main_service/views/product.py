import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from .constants import product_properties
from ..exceptions import NotFoundError, NotUniqueError
from ..serializers import ProductSerializer
from ..services import ProductService


class ProductView(APIView):
    logger = logging.getLogger('mainLogger')

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
        try:
            product = ProductService.get_single_product(
                product_id=product_id)
            return Response(product)
        except NotFoundError:
            self.logger.info('\nProduct {:d} not found'.format(product_id))
            return Response({'message': 'Product not found'}, status=404)
        except NotUniqueError:
            self.logger.critical(
                'Critical: Product with id of {:d} returned more than one product'.format(product_id))
            return Response({'message': 'Internal server error. Product with the id {:d} returned more than one product'.format(product_id)}, status=500)
