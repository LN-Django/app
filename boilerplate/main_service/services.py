from rest_framework.utils.serializer_helpers import ReturnDict
from .exceptions import NotFoundError, NotUniqueError
from .models import Product


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

    def post_single_product(product_data: ReturnDict) -> dict:
        """Method to post / create a single product"""
        product: Product = Product.objects.create(name=product_data['name'], base_price=product_data['base_price'],
                                                  description=product_data['description'], weight=product_data['weight'], category=product_data['category'])

        response_data = product_data
        response_data['id'] = product.id
        return response_data

    def get_all_products():
        """Method to get all products from the database"""
        return Product.objects.all().values()

    def get_all_products_with_details():
        """Method to get all products from the database and its additional infos from external services"""

        # TODO: implement fetching data from external API
        return ProductService.get_all_products()
