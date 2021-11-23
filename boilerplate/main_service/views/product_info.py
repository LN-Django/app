import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request


class ProductInfoView(APIView):
    logger = logging.getLogger('mainLogger')
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request, product_id):
        self.logger.info('Test log')
        data = {'product_id': product_id}
        return Response(data)
