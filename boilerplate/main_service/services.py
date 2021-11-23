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
