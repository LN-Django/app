from drf_yasg import openapi

product_properties = {
    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product (max length: 64 characters.)'),
    'base_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Base price of the product'),
    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product description (max length: 128 characters)'),
    'weight': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product weight'),
    'category': openapi.Schema(type=openapi.TYPE_STRING, description='Product category')
}