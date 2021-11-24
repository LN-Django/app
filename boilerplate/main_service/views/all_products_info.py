import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request


class AllProductsInfoView(APIView):
    """Class to handle HTTP request to get informations on ALL products. Has almost the same function as the `ProductInfoView` class,
    but this class gets the information for all products rather than just a single product."""

    logger = logging.getLogger('mainLogger')
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        self.logger.info('Test log')
        data = {'product_id': 'all'}
        return Response(data)
