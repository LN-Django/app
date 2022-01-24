from django.conf.urls import url
from django.urls import path


from .views.products_to_csv import ProductToCSVView
from .views.product import ProductView
from .views.products import ProductsListView
from .views.product_info import ProductInfoView

urlpatterns = [
    path('api/products/csv', ProductToCSVView.as_view(),
         name='get_products_as_csv'),
    url('api/products', ProductsListView.as_view(), name='get_post_products'),
    path('api/product/<int:product_id>',
         ProductView.as_view(), name='get_single_product'),
    path('api/product/<int:product_id>/info',
         ProductInfoView.as_view(), name='get_single_product_info'),
]
