from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Product


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
