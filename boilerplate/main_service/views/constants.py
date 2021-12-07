from drf_yasg import openapi

product_properties = {
    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product (max length: 64 characters.)'),
    'base_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Base price of the product'),
    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product description (max length: 128 characters)'),
    'weight': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product weight'),
    'category': openapi.Schema(type=openapi.TYPE_STRING, description='Product category')
}

storage_information = {
    'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the product'),
    'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='Remaining amount of the product'),
    'delivery_time': openapi.Schema(type=openapi.TYPE_INTEGER, description='Estimated delivery time of the product'),
}

post_product_properties = {
    **product_properties,
    **storage_information
}

product_properties_info = {
    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product (max length: 64 characters.)'),
    'base_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Base price of the product'),
    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product description (max length: 128 characters)'),
    'weight': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product weight'),
    'category': openapi.Schema(type=openapi.TYPE_STRING, description='Product category'),
    'taxed_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product price inclusive tax')
}
