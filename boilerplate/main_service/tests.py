from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls.base import resolve
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse
from rest_framework.utils import json

from .serializers import ProductSerializer

from .models import Product

client = APIClient()

"""Model tests"""


class ProductTest(TestCase):
    """Test module for `Product` model"""

    def setUp(self) -> None:
        Product.objects.create(name='Product 1', base_price=12,
                               description='Test desc', weight=5, category='Tech')
        Product.objects.create(name='Product 2', base_price=15,
                               description='Test desc 2', weight=1, category='Food')
        return super().setUp()

    def test_product_price(self):
        product_1 = Product.objects.get(name='Product 1')
        self.assertEqual(product_1.base_price, 12)

    def test_product_create_invalid(self):
        """Test for creating a Product object with an invalid parameter"""
        try:
            product = Product.objects.create(
                name='Product 3', base_price=0, description='asdsadsa', weight=-1, category='Mock')
            product.full_clean()

            self.fail('Object creation should throw an error')
        except ValidationError:
            pass


"""HTTP endpoint tests"""


class GetAllProductsTest(TestCase):
    """Test module to test get all products (`/products`) endpoint"""

    def setUp(self) -> None:
        Product.objects.create(name='Product 1', base_price=12,
                               description='Test desc', weight=5, category='Tech')
        Product.objects.create(name='Product 2', base_price=15,
                               description='Test desc 2', weight=1, category='Food')
        return super().setUp()

    def test_get_all_products(self):
        """It should return all products created in the database"""
        response: Response = client.get(
            reverse('get_post_products'))  # API response
        products = Product.objects.all()  # ORM Data from DB

        self.assertListEqual(list(response.data), list(products.values()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostProductTest(TestCase):
    """Test module to test a product creation endpoint"""

    def setUp(self) -> None:
        self.base_params = {
            'name': 'Test',
            'base_price': 4,
            'description': 'Sample',
            'weight': 12,
            'category': 'Tech'
        }
        return super().setUp()

    def test_post_product_valid_parameter(self):
        """It should return the status code 201 if the parameter passed is valid"""
        response = client.post(
            reverse('get_post_products'),
            data=json.dumps(self.base_params),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_product_invalid_base_price_parameter(self):
        """It should return the status code 500 if the base_price parameter is not bigger than zero"""
        parameter = self.base_params.copy()
        parameter['base_price'] = 0
        response = client.post(
            reverse('get_post_products'),
            data=json.dumps(parameter),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # TODO: Test the error message
        # self.assertContains(response.data.errors)

    def test_product_invalid_weight_parameter(self):
        """It should return the status code 500 if the weight parameter is not bigger than zero"""
        parameter = self.base_params.copy()
        parameter['weight'] = 0
        response = client.post(
            reverse('get_post_products'),
            data=json.dumps(parameter),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # TODO: Test the error message
        # self.assertContains(response.data.errors)
