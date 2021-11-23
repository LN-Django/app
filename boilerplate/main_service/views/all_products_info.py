import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request


class AllProductsInfoView(APIView):
    logger = logging.getLogger('mainLogger')
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        self.logger.info('Test log')
        data = {'product_id': 'all'}
        return Response(data)
