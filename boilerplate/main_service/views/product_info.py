import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request

from ..services import ProductService

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .constants import product_properties_info
from ..exceptions import NotFoundError, NotUniqueError


class ProductInfoView(APIView):
    """View class to handle product info HTTP Request. All external API calls should be done here
        - Calculator (Mehrwertsteuer)
        - Storage (Storage info -> location, delivery date, etc [WIP!])
        - External API [WIP!]
    """
    logger = logging.getLogger('mainLogger')
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={
        '200': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=product_properties_info),
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
        operation_description='Get datas incl. MwSt, storage info, and external API info of a single product with the provided `product_id`'
    )

    def get(self, request: Request, product_id):
        try:
            data = ProductService.get_product_info(product_id)
            return Response(data)
        except NotFoundError:
            self.logger.info('\nProduct {:d} not found'.format(product_id))
            return Response({'message': 'Product not found'}, status=404)
        except NotUniqueError:
            self.logger.critical(
                'Critical: Product with id of {:d} returned more than one product'.format(product_id))
            return Response({'message': 'Internal server error. Product with the id {:d} returned more than one product'.format(product_id)}, status=500)

