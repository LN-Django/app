import csv
import logging
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.request import Request

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..services import ProductService


class ProductToCSVView(APIView):
    """Class to handle HTTP request that should return all product informations as a CSV file / embedded as a clear text in the JSON response"""

    logger = logging.getLogger('mainLogger')
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={
        '200': openapi.Schema(
            type=openapi.TYPE_FILE
        )
    })
    def get(self, request: Request):
        """Service to export all product datas (including its additional informations) as a CSV file"""

        product_datas = ProductService.get_all_products_with_details()

        response = HttpResponse(content_type='text/csv', headers={
                                'Content-Disposition': 'attachment; filename="product_datas.csv"'})

        writer = csv.writer(response)

        sample_data_keys = product_datas.first().keys()
        writer.writerow(sample_data_keys)

        for product in product_datas:
            writer.writerow(product.values())

        return response
