from os import environ

from requests.models import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from .exceptions import NotFoundError, NotUniqueError
from .models import Product
import requests

TEST = int(environ.get('TEST', default=0))


class ENDPOINTS:
    calculator_service = 'https://cryptic-wildwood-57466.herokuapp.com/api/calculator'
    storage_service = 'https://peaceful-wave-28166.herokuapp.com/api/storage'

    storage_code = {'post': 201, 'get': 200}
    calculator_code = {'get': 200}


class ProductService:

    def get_single_product(product_id: int) -> Product:
        """Method to get a single product from the database"""
        queryset = Product.objects.filter(id=product_id)
        product_count = queryset.count()
        if product_count == 0:
            raise NotFoundError()
        elif product_count > 1:
            raise NotUniqueError()

        return queryset.values()[0]

    def post_single_product(product_data: ReturnDict, additional_data: dict) -> dict:
        """Method to post / create a single product"""

        if TEST:
            print(
                "\n!! Running in test environment. API calls to external API won't be executed")

        """Check that the request body/payload is valid for external APIs"""
        storage_info_keys = ['location', 'amount', 'delivery_time']
        for key in storage_info_keys:
            if not TEST and additional_data.get(key) is None:
                raise KeyError(
                    'Attribute `{:s}` not found in request body'.format(key))

        """Create product object in database"""
        product: Product = Product.objects.create(name=product_data['name'], base_price=product_data['base_price'],
                                                  description=product_data['description'], weight=product_data['weight'], category=product_data['category'])

        if not TEST:
            """Create entry on storage service"""
            storage_response = ProductService.post_product_storage_information(
                additional_data, product.id)

            """Handle if external API request is not successful"""
            if storage_response.status_code != ENDPOINTS.storage_code['post']:
                Product.objects.filter(id=product.id).delete()
                return storage_response.json()

        response_data = {**product_data, **additional_data}
        response_data['id'] = product.id
        return response_data

    def post_product_storage_information(product_data: dict, id: int) -> Response:
        """Method to post product storage information on the storage service"""
        storage_response = requests.post(ENDPOINTS.storage_service, json={
                                         'location': product_data['location'], 'amount': product_data['amount'],
                                         'delivery_time': product_data['delivery_time'], 'product_id': id})
        return storage_response

    def get_product_storage_information(product_id: int) -> Response:
        """Method to fetch product storage information"""
        storage_response = requests.get(
            ENDPOINTS.storage_service + '/' + str(product_id))
        return storage_response

    def get_all_products():
        """Method to get all products from the database"""
        return Product.objects.all().values()

    def get_product_info(product_id: int):
        """Method to get info of a product from the database"""

        product = ProductService.get_single_product(product_id)

        """Fetch storage informations"""
        storage_response = ProductService.get_product_storage_information(
            product_id)
        storage_data = storage_response.json()

        if storage_response.status_code != ENDPOINTS.storage_code['get']:
            return storage_data

        calculator_response = requests.post(
            ENDPOINTS.calculator_service, json={'base_price': product['base_price']})
        calculator_data = calculator_response.json()

        if calculator_response.status_code != ENDPOINTS.calculator_code['get']:
            return calculator_data

        product['taxed_price'] = calculator_data['taxed_price']
        del storage_data['product_id']

        return {**product, **storage_data}

    def get_all_products_with_details():
        """Method to get all products from the database and its additional infos from external services"""

        # TODO: implement fetching data from external API
        return ProductService.get_all_products()
