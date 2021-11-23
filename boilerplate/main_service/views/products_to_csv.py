import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request


class ProductToCSVView(APIView):
    """Class to handle HTTP request that should return all product informations as a CSV file / embedded as a clear text in the JSON response"""

    logger = logging.getLogger('mainLogger')
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        self.logger.info('Test log')
        data = {'csv': True}
        return Response(data)
